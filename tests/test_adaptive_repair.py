from src.adaptive_repair import AdaptiveRepair

def test_adaptive_weights_shift():
    ar = AdaptiveRepair(eta=0.2)
    base = ar.weights()
    ar.step({"council": 0.5, "stability": 0.95, "penalty": 1})
    w1 = ar.weights()
    assert w1["specificity"] > base["specificity"]
    assert w1["audit"] > base["audit"]
    assert w1["anchor"] <= base["anchor"]
