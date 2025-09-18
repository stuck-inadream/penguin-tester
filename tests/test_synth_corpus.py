import yaml, os
from tools.synth_corpus import make_pack

def test_synth_pack_contains_myth_rule(tmp_path):
    out = make_pack(seed=11, myth_strength=0.6, outdir=tmp_path.as_posix())
    with open(os.path.join(out, "rules.yaml"), "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)
    assert any(r.get("kind") == "myth" for r in rules)
