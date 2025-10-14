import queue
import threading
from typing import Any, final

@final
class QueueManager:
    _queues: dict[str, queue.Queue] = {}
    _lock = threading.Lock()  # Global lock to guard creation of new queues

    def __init__(self, queue_key: str, maxsize: int = 0):
        """
        Initialize or attach to an existing queue with the given key.
        :param queue_key: Identifier for the queue.
        :param maxsize: Maximum queue size (0 for infinite).
        """
        self.queue_key = queue_key
        with QueueManager._lock:
            if queue_key not in QueueManager._queues:
                QueueManager._queues[queue_key] = queue.Queue(maxsize=maxsize)
        self._queue = QueueManager._queues[queue_key]

    def push(self, item: dict[str, Any]) -> None:
        """Push a dictionary into the queue."""
        if not isinstance(item, dict):
            raise TypeError("Only dictionaries are allowed in the queue.")
        self._queue.put(item, block=True)

    def pop(self, timeout: float | None = None) -> dict[str, Any] | None:
        """Pop an item from the queue (FIFO). Returns None if empty and timeout expires."""
        try:
            return self._queue.get(block=True, timeout=timeout)
        except queue.Empty:
            return None

    def size(self) -> int:
        """Get the number of items currently in the queue."""
        return self._queue.qsize()

    def clear(self) -> None:
        """Clear all items in the queue safely."""
        with self._queue.mutex:
            self._queue.queue.clear()

    @classmethod
    def list_queues(cls):
        """List all active queue keys."""
        return list(cls._queues.keys())
