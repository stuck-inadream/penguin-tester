from typing import Callable, Any, List, Dict
from collections import Counter

class CouncilRunner:
    def __init__(self, callables: List[Callable[[str], Any]]):
        self.callables = list(callables)

    def run(self, prompt: str) -> Dict:
        outs = [c(prompt) for c in self.callables]
        cnt = Counter(outs)
        if not cnt:
            return {"outputs": outs, "agreement": 0.0, "winner": None, "drift": 1.0}
        winner, freq = cnt.most_common(1)[0]
        agreement = freq/len(outs)
        drift = 1.0 - agreement
        return {"outputs": outs, "winner": winner, "agreement": agreement, "drift": drift}
