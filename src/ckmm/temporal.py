from typing import Callable, Any, Dict

class ReplayStability:
    def __init__(self, repeats: int = 3):
        self.repeats = max(1, int(repeats))

    def run(self, f: Callable[[str], Any], prompt: str) -> Dict:
        outs = [f(prompt) for _ in range(self.repeats)]
        if not outs:
            return {"outputs": outs, "top": None, "stability": 0.0}
        # majority
        top = max(set(outs), key=outs.count)
        ratio = outs.count(top)/len(outs)
        return {"outputs": outs, "top": top, "stability": ratio}
