class ResearchEvaluator:
    def __init__(self):
        self.kg = {}

    def add_fact(self, s, p, o):
        self.kg.setdefault(s, {})[p] = o

    def search(self, q: str):
        return [k for k in self.kg.keys() if q.lower() in k.lower()]

    def score(self, checkpoints: list, final_answer: str):
        return {"checkpoints": len(checkpoints), "final_len": len(final_answer or ""), "score": 0.5}
