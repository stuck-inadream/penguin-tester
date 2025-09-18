# Alias test to match expected filename variants
from challenges.leaderboard import score_submission

def test_scoring_static(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    m = {"myth_yes_bias": 0.7, "exception_no_bias": 0.6, "empty_yes_bias": 0.9, "divergence": 0.3}
    r = score_submission(m, use_adaptive=False)
    assert "score" in r and "weights" in r
