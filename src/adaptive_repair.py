from dataclasses import dataclass

@dataclass
class AdaptiveRepair:
    """Interfaces-only controller that adapts repair weights from public CKMM signals."""
    eta: float = 0.1
    w_anchor: float = 1.0
    w_specificity: float = 1.0
    w_audit: float = 1.0

    def step(self, ckmm_summary: dict) -> None:
        agree = float(ckmm_summary.get("council", 0.0))
        stab = float(ckmm_summary.get("stability", 0.0))
        penalty = float(ckmm_summary.get("penalty", 0))

        self.w_specificity += self.eta * (1.0 - agree)
        self.w_audit += self.eta * (1.0 if penalty > 0 else 0.0)
        self.w_anchor -= self.eta * max(0.0, stab - 0.9)

        self.w_anchor = min(max(self.w_anchor, 0.5), 2.0)
        self.w_specificity = min(max(self.w_specificity, 0.5), 2.0)
        self.w_audit = min(max(self.w_audit, 0.5), 2.0)

    def weights(self) -> dict:
        return {
            "anchor": round(self.w_anchor, 3),
            "specificity": round(self.w_specificity, 3),
            "audit": round(self.w_audit, 3),
        }
