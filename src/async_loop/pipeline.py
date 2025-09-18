import multiprocessing as mp
from dataclasses import dataclass

@dataclass
class AsyncPipelineStatus:
    def __post_init__(self):
        self._lock = mp.Lock()
        self._q = mp.Queue(maxsize=128)

    def enqueue(self, item):
        with self._lock:
            if not self._q.full():
                self._q.put(item)

    def depth(self) -> int:
        with self._lock:
            return self._q.qsize()

    def snapshot(self):
        return {"queue_depth": self.depth()}
