import random, pathlib, yaml, argparse

def make_pack(seed: int = 7, n_rules: int = 12, myth_strength: float = 0.3,
              outdir: str = "data/synth") -> str:
    """Produce a tiny, seedable distortion pack: rules.yaml and corpus.txt."""
    random.seed(int(seed))
    p = pathlib.Path(outdir); p.mkdir(parents=True, exist_ok=True)

    rules = []
    for i in range(int(n_rules)):
        r = random.random()
        kind = "myth" if r < myth_strength else ("exception" if i % 3 == 0 else "fact")
        pattern = r"(?i)\bpenguin\b" if kind != "fact" else rf"(?i)\btoken{i}\b"
        penalty = 2 if kind == "myth" else 0
        rules.append({"name": f"r{i}", "kind": kind, "pattern": pattern, "penalty": penalty})

    with open(p / "rules.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(rules, f, sort_keys=False)

    with open(p / "corpus.txt", "w", encoding="utf-8") as f:
        for i in range(64):
            f.write(f"penguin story line {i}\n")

    return str(p)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--n_rules", type=int, default=12)
    ap.add_argument("--myth_strength", type=float, default=0.3)
    ap.add_argument("--outdir", type=str, default="data/synth")
    args = ap.parse_args()
    path = make_pack(**vars(args))
    print(path)
