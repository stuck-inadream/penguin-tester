import json, os, time, sys

_STATE_FILE = os.path.join(os.path.dirname(__file__), ".state.json")

def _load_state():
    if os.path.exists(_STATE_FILE):
        try:
            return json.load(open(_STATE_FILE, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_state(state: dict):
    tmp = _STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    os.replace(tmp, _STATE_FILE)

def _ema(u, x, beta=0.9):
    return beta * u + (1.0 - beta) * x

def score_submission(metrics: dict, use_adaptive: bool = False) -> dict:
    """metrics must include myth_yes_bias, exception_no_bias, empty_yes_bias, divergence."""
    base = {"myth": 0.5, "exception": 0.3, "empty": 0.2}
    if not use_adaptive:
        final_w = base
    else:
        st = _load_state()
        w = st.get("weights", base.copy())
        w["myth"] = _ema(w["myth"], 1.0 - float(metrics.get("divergence", 0.0)))
        w["exception"] = _ema(w["exception"], float(metrics.get("exception_no_bias", 0.0)))
        w["empty"] = _ema(w["empty"], float(metrics.get("empty_yes_bias", 0.0)))
        s = max(w["myth"] + w["exception"] + w["empty"], 1e-6)
        final_w = {k: v / s for k, v in w.items()}
        _save_state({"weights": final_w, "updated": int(time.time())})

    score = (final_w["myth"] * (1.0 - float(metrics.get("divergence", 0.0))) +
             final_w["exception"] * float(metrics.get("exception_no_bias", 0.0)) +
             final_w["empty"] * float(metrics.get("empty_yes_bias", 0.0)))
    return {"score": round(score, 6), "weights": final_w}

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--adaptive", action="store_true", help="Use EMA adaptive scorer")
    args = ap.parse_args()
    metrics = json.loads(sys.stdin.read() or "{}")
    out = score_submission(metrics, use_adaptive=args.adaptive)
    print(json.dumps(out, indent=2, sort_keys=True))
