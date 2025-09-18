from challenges.leaderboard import score_submission

def test_adaptive_scoring_progress(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    m1 = {"myth_yes_bias": 0.7, "exception_no_bias": 0.6, "empty_yes_bias": 0.9, "divergence": 0.3}
    m2 = {"myth_yes_bias": 0.7, "exception_no_bias": 0.7, "empty_yes_bias": 0.92, "divergence": 0.2}
    r1 = score_submission(m1, use_adaptive=True)
    r2 = score_submission(m2, use_adaptive=True)
    assert r2["score"] >= r1["score"]
