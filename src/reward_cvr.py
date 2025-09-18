from dataclasses import dataclass

@dataclass
class CVRReward:
    """Stub reward model that wraps simple rubrics; interfaces only."""
    w_yes: float = 0.8
    w_no: float = 0.7

    @staticmethod
    def load(path: str) -> "CVRReward":
        return CVRReward()

    def score(self, prompt: str, answer: str) -> float:
        a = (answer or "").strip().lower()
        return self.w_yes if a == "yes" else self.w_no

class DuPOSelfVerifier:
    def dual_check(self, prompt: str, candidates):
        pairs = 0
        disag = 0
        for i in range(len(candidates)):
            for j in range(i+1, len(candidates)):
                pairs += 1
                if candidates[i] != candidates[j]:
                    disag += 1
        return {"pairs_checked": pairs, "disagreements": disag}

class PolicyHooks:
    def brpo(self): return "brpo_stub"
    def grpo(self): return "grpo_stub"
