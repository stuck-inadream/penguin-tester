from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AggregatorPolicy:
    """Learned-style aggregator stub using reward margin, diversity, and phase cues."""
    def aggregate(self, candidates: List[str], rewards: List[float], ckmm: Dict) -> str:
        if not candidates:
            return ""
        idx = max(range(len(candidates)), key=lambda i: (rewards[i], -len(candidates[i])))
        return candidates[idx]

class CompressionGovernor:
    def select(self, candidates: List[str]) -> str:
        ok = [c for c in candidates if c]
        return min(ok, key=len) if ok else ""
