import argparse, json, logging, logging.handlers, re, sys, random, multiprocessing
from typing import Dict, Any, List
from z3 import Solver, Bool, Not, sat
import gradio as gr
import yaml

from src.ckmm import (
    FuelLedger, ReplayStability, CouncilRunner,
    ConstraintEvaluator, SubstrateInfo, evaluate_ckmm_pass
)
from src.infra import gpu_status_safe
from src.reward_cvr import CVRReward, DuPOSelfVerifier
from src.aggregator_policy import AggregatorPolicy, CompressionGovernor
from src.adaptive_repair import AdaptiveRepair

def _setup_logging(level_name: str = "ERROR"):
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(getattr(logging, level_name.upper(), logging.ERROR))
    fh = logging.handlers.RotatingFileHandler('errors.log', maxBytes=65536, backupCount=3)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    root.addHandler(fh)
    root.addHandler(ch)
    return root

def _effective_iterations(req: int) -> int:
    try:
        cores = max(1, multiprocessing.cpu_count())
    except Exception:
        cores = 1
    if req < 0:
        return min(max(100_000, cores * 1_000_000), 10_000_000)
    return min(req, 10_000_000)

def _toy_model(prompt: str) -> str:
    text = (prompt or "").lower()
    if "exception" in text:
        return "no"
    if "myth" in text:
        return "yes"
    return "yes"

def _ckmm_summary(prompt: str, iterations: int, thresholds: Dict[str, Any], verbose: bool=False) -> Dict[str, Any]:
    # Energy
    with FuelLedger() as fuel:
        acc = 0
        for i in range(max(0, int(iterations))):
            if i % 1_000_000 == 0 and i > 0:
                fuel.tick_attention(1)
            acc += i % 7
        fuel_d = fuel.to_dict()

    # Temporal stability
    temporal = ReplayStability(repeats=5).run(_toy_model, prompt)

    # Council
    council = CouncilRunner([_toy_model, _toy_model, _toy_model]).run(prompt)

    # Ethics
    ethics = ConstraintEvaluator("config/constraints.sample.yaml").evaluate(_toy_model(prompt), "")

    # Embodiment
    substrate = SubstrateInfo().capture()

    # Decision
    passes = evaluate_ckmm_pass(fuel_d, temporal, council, ethics, substrate, thresholds)

    # Pretty numbers
    wall_s = fuel_d.get("wall_s", 0.0)
    kib = fuel_d.get("kib", 0.0)
    mib = kib / 1024.0 if kib else 0.0
    stab = temporal.get("stability", 0.0)
    agree = council.get("agreement", 0.0)
    penalty = ethics.get("penalty", 0)

    summary = {
        "pass": passes.get("all_ok", False),
        "fuel_wall_s": round(wall_s, 6),
        "fuel_mib": round(mib, 4),
        "stability": round(stab, 4),
        "council": round(agree, 4),
        "penalty": int(penalty),
        "weighted_council_ok": passes.get("weighted_council_ok", False)
    }
    if verbose:
        summary.update({
            "fuel": fuel_d,
            "temporal": temporal,
            "council_detail": council,
            "ethics_detail": ethics,
            "substrate": substrate,
            "thresholds": thresholds,
            "gpu": gpu_status_safe()
        })
    return summary

def _format_ckmm_line(s: Dict[str, Any]) -> str:
    state = "PASS" if s.get("pass") else "FAIL"
    wc = "weighted ok" if s.get("weighted_council_ok") else "weighted no"
    return f"ckmm {state} | fuel {s['fuel_wall_s']} s and {s['fuel_mib']} MiB | stab {s['stability']} | council {s['council']} [{wc}] | penalty {s['penalty']}"

def _generate_candidates(prompt: str, k: int, seed: int) -> List[str]:
    random.seed(seed)
    base = _toy_model(prompt)
    cands = [base for _ in range(k)]
    # introduce slight diversity for 'myth'
    if "myth" in (prompt or "").lower():
        cands = ["yes" if random.random() > 0.2 else "no" for _ in range(k)]
    return cands

def make_checker(args, thresholds: Dict[str, Any]):
    iterations = _effective_iterations(args.ckmm_iterations)
    agg = AggregatorPolicy()
    gov = CompressionGovernor()
    cvr = CVRReward.load("configs/cvr_dopo.yaml")
    dupo = DuPOSelfVerifier()
    adaptive = AdaptiveRepair(eta=args.adaptive_eta) if args.adaptive else None

    def check_penguin(query: str) -> str:
        try:
            # Z3 baseline facts
            s = Solver()
            Penguin, Fly = Bool('Penguin'), Bool('Fly')
            s.add(Penguin)
            s.add(Not(Fly))

            text = (query or "").lower()
            if "fly" in text and re.search(r"\b(must|always|definitely)\b", text):
                s2 = Solver()
                s2.add(Penguin)
                s2.add(Fly)
                res = s2.check()
                ckmm = _ckmm_summary(query, iterations, thresholds, verbose=bool(args.json))
                if adaptive:
                    adaptive.step(ckmm)
                    ckmm["adaptive_weights"] = adaptive.weights()
                if res != sat:
                    out = "unsat: conflict detected. Score=0"
                else:
                    out = f"unexpected: {res}"
                return json.dumps(ckmm, sort_keys=True, indent=2) if args.json else (out + " | " + _format_ckmm_line(ckmm) + (f" | adaptive {ckmm['adaptive_weights']}" if 'adaptive_weights' in ckmm else ""))

            # Sampling and aggregation
            k = max(3, int(args.samples))
            cands = _generate_candidates(query, k, args.seed)
            rewards = [cvr.score(query, a) for a in cands]
            if args.dupo:
                _ = dupo.dual_check(query, cands)
            choice = agg.aggregate(cands, rewards, {})
            concise = gov.select(cands)

            # Distortion score toy calc
            modal = 0.7 if "myth" in text else (0.6 if "exception" in text else 1.0)
            diversity = 2.0
            divergence = 1.0 - (0.7 if "myth" in text else 1.0)
            score = (modal * diversity) / (1.0 + divergence) if (1.0 + divergence) > 0 else 0.0

            ckmm = _ckmm_summary(query, iterations, thresholds, verbose=bool(args.json))
            if adaptive:
                adaptive.step(ckmm)
                ckmm["adaptive_weights"] = adaptive.weights()

            if args.json:
                ckmm.update({"distortion_score": round(score, 3), "choice": choice, "concise": concise})
                return json.dumps(ckmm, sort_keys=True, indent=2)

            line = f"sat: penguins do not fly. Score={score:.3f} | " + _format_ckmm_line(ckmm)
            if 'adaptive_weights' in ckmm:
                line += f" | adaptive {ckmm['adaptive_weights']}"
            return line

        except Exception:
            logging.getLogger().error("check_penguin failed", exc_info=True)
            return "error: see errors.log"
    return check_penguin

def _parse_thresholds(th_json: str) -> Dict[str, Any]:
    if not th_json:
        return {}
    try:
        import jsonschema, json as _json
        data = _json.loads(th_json)
        if not isinstance(data, dict):
            raise ValueError("thresholds must be a JSON object")
        jsonschema.validate(instance=data, schema={"type":"object"})
        return data
    except Exception:
        logging.getLogger().warning("jsonschema not available or invalid thresholds, using parsed JSON if possible")
        try:
            import json as _json
            return _json.loads(th_json)
        except Exception:
            return {}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--share", action="store_true", help="Public share (gradio.live)")
    ap.add_argument("--server_name", type=str, default=None, help="Gradio server name")
    ap.add_argument("--server_port", type=int, default=None, help="Gradio server port")
    ap.add_argument("--log-level", type=str, default="ERROR",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                    help="Logging level for errors.log and console")

    # CKMM controls
    ap.add_argument("--ckmm-iterations", type=int, default=5_000_000, help="Workload iterations; negative autoscale")
    ap.add_argument("--ckmm-thresholds", type=str, default="", help="JSON to override parts of config/ckmm_config.yaml")

    # Output modes
    ap.add_argument("--summary", action="store_true", default=True, help="Human readable summary output (default)")
    ap.add_argument("--json", action="store_true", help="Print verbose JSON instead of summary")

    # Novelty features
    ap.add_argument("--dupo", action="store_true", help="Enable DuPO paired checks")
    ap.add_argument("--samples", type=int, default=5, help="Number of samples for aggregation")
    ap.add_argument("--seed", type=int, default=7, help="Random seed for sampling")
    ap.add_argument("--real-data", action="store_true", help="Use tiny real data stubs")

    # Adaptive repair
    ap.add_argument("--adaptive", action="store_true", help="Enable adaptive repair controller driven by CKMM signals")
    ap.add_argument("--adaptive-eta", type=float, default=0.1, help="Learning rate for adaptive repair")

    args = ap.parse_args()
    _setup_logging(args.log_level)

    # Validate args
    try:
        if args.server_port is not None and args.server_port <= 0:
            raise ValueError("Port must be a positive integer")
        if args.server_name is not None and not isinstance(args.server_name, str):
            raise ValueError("Server name must be a string")
    except ValueError as e:
        logging.getLogger().error(e, exc_info=True); sys.exit(1)

    # Load thresholds
    with open("config/ckmm_config.yaml", "r", encoding="utf-8") as f:
        base_th = yaml.safe_load(f) or {}
    override = _parse_thresholds(args.ckmm_thresholds)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base_th.get(k), dict):
            base_th[k].update(v)
        else:
            base_th[k] = v

    checker = make_checker(args, base_th)

    title = f"Penguin Distortion Tester — fuel≤{base_th.get('fuel', {}).get('max_time_s', 'n/a')}s | GPU {gpu_status_safe().get('gpus',0)}"
    iface = gr.Interface(fn=checker, inputs="text", outputs="text", title=title)
    iface.launch(server_name=args.server_name, server_port=args.server_port, share=args.share)

if __name__ == "__main__":
    main()
