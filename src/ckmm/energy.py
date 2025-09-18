import time, tracemalloc
from dataclasses import dataclass, field
from typing import Optional, Dict

try:
    import psutil
    _HAS_PSUTIL = True
except Exception:
    _HAS_PSUTIL = False

@dataclass
class FuelSnapshot:
    wall_s: float
    kib: float
    attention_ticks: int
    cpu_pct: float = 0.0

@dataclass
class FuelLedger:
    attention_ticks: int = 0
    _t0: Optional[float] = field(default=None, init=False)
    _mem_started: bool = field(default=False, init=False)
    snapshot: Optional[FuelSnapshot] = field(default=None, init=False)

    def __enter__(self):
        self._t0 = time.perf_counter()
        tracemalloc.start()
        self._mem_started = True
        return self

    def __exit__(self, exc_type, exc, tb):
        wall = time.perf_counter() - (self._t0 or time.perf_counter())
        cur, peak = tracemalloc.get_traced_memory() if self._mem_started else (0, 0)
        tracemalloc.stop()
        cpu = psutil.cpu_percent() if _HAS_PSUTIL else 0.0
        self.snapshot = FuelSnapshot(wall, peak/1024.0, self.attention_ticks, cpu)

    def tick_attention(self, n: int = 1):
        self.attention_ticks += n

    def to_dict(self) -> Dict:
        s = getattr(self, "snapshot", None)
        return {
            "wall_s": getattr(s, "wall_s", 0.0),
            "kib": getattr(s, "kib", 0.0),
            "attention_ticks": getattr(s, "attention_ticks", self.attention_ticks),
            "cpu_pct": getattr(s, "cpu_pct", 0.0),
        }
