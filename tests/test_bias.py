def log_skewed(anchor, dataset):
    with open('bias_log.txt', 'a') as f:
        f.write(f"{anchor}: {dataset}\n")

def test_log_skewed(tmp_path, monkeypatch):
    p = tmp_path / 'bias_log.txt'
    monkeypatch.chdir(tmp_path)
    log_skewed('anchorA', 'dataset1')
    assert p.exists()
    assert 'anchorA' in p.read_text()
