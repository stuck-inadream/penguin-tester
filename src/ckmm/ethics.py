from typing import Dict, List, Any
import yaml, re

class ConstraintEvaluator:
    def __init__(self, yaml_path: str):
        with open(yaml_path, "r", encoding="utf-8") as f:
            self.rules: List[Dict[str, Any]] = yaml.safe_load(f) or []

    def evaluate(self, text: str, recovered_text: str = "") -> Dict:
        total = 0
        hits = []
        for r in self.rules:
            pat = r.get("pattern", "")
            if pat and re.search(pat, text or ""):
                hits.append(r.get("name", "rule"))
                total += int(r.get("penalty", 1))
        recovered = bool(recovered_text) and (recovered_text != text)
        return {"hits": hits, "penalty": total, "recovered": recovered}
