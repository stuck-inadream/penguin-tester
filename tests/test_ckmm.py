def test_ckmm_workload(tmp_path, monkeypatch):
    from src.ckmm import FuelLedger, ReplayStability, CouncilRunner, ConstraintEvaluator, SubstrateInfo, evaluate_ckmm_pass
    import yaml

    # Fuel (very small loop)
    with FuelLedger() as fuel:
        acc = 0
        for i in range(100_000):
            acc += i % 7
    fd = fuel.to_dict()
    assert fd["wall_s"] >= 0.0

    th = yaml.safe_load(open("config/ckmm_config.yaml","r",encoding="utf-8"))
    def toy(p): return "yes"
    temporal = ReplayStability(repeats=3).run(toy, "prompt")
    council = CouncilRunner([toy, toy, toy]).run("prompt")
    ethics = ConstraintEvaluator("config/constraints.sample.yaml").evaluate("no hate here", "")
    sub = SubstrateInfo().capture()

    passes = evaluate_ckmm_pass(fd, temporal, council, ethics, sub, th)
    assert "weighted_council_ok" in passes
