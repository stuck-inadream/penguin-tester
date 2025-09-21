def test_readme_exists():
    import os
    assert os.path.exists("README.md")

def test_requirements_pinned():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    assert all("==" in l for l in lines), "Pin your versions with =="
