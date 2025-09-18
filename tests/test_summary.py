import subprocess, sys, os, textwrap

def test_summary_smoke(tmp_path):
    # Create a tiny runner that imports the checker and prints one line
    code = textwrap.dedent('''
    import yaml
    from gradio_demo import make_checker, _parse_thresholds
    import argparse
    args = argparse.Namespace(ckmm_iterations=100000, ckmm_thresholds="", json=False, summary=True, dupo=False, samples=3, seed=7, real_data=False, adaptive=False, adaptive_eta=0.1)
    base = yaml.safe_load(open("config/ckmm_config.yaml","r",encoding="utf-8"))
    fn = make_checker(args, base)
    print(fn("do penguins myth fly?"))
    ''')
    p = tmp_path/"r.py"; p.write_text(code, encoding="utf-8")
    # PYTHONPATH includes project root so imports resolve
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    out = subprocess.check_output([sys.executable, str(p)], env=env, text=True)
    assert "ckmm" in out and "fuel" in out
