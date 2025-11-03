from .settings import config
from .logger import configure_logging
from pepper.cache import QueueManager, CacheManager
from pepper.cache.key_cache import KeyCache

logger = configure_logging()

key_cache = KeyCache()
cache_user = CacheManager("users", index_keys=["id", "email", "role", "full_name"])
cache_device = CacheManager("devices", index_keys=["id", "name", "unique_id"])
cache_position = CacheManager("positions", index_keys=["id", "device_id", "unique_id", "lon", "lat", "speed"])

queue_position = QueueManager("position_ingest")
queue_forward = QueueManager("forward_state")

__all__ = ["config", "KeyCache", "key_cache"]
