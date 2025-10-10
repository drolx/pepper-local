# cached_dict_list.py
import threading
import uuid
from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, List, Optional

try:
    from cachetools import Cache, TTLCache
except Exception:
    # fallback if cachetools is not available
    TTLCache = None
    Cache = dict


class _SimpleRWLock:
    """
    A simple reader-writer-ish lock:
    - multiple concurrent readers allowed
    - writers exclusive (wait for readers)
    This is not perfect production-grade RWLock but suitable for typical use.
    """

    def __init__(self):
        self._readers = 0
        self._lock = threading.Lock()
        self._read_ready = threading.Condition(self._lock)

    def acquire_read(self):
        with self._lock:
            self._readers += 1

    def release_read(self):
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self):
        self._lock.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        self._lock.release()


# global lock registry by cache_key so multiple class instances share same lock
_global_locks: Dict[str, _SimpleRWLock] = {}
_global_locks_lock = threading.Lock()


def _get_lock_for_key(cache_key: str) -> _SimpleRWLock:
    with _global_locks_lock:
        lock = _global_locks.get(cache_key)
        if lock is None:
            lock = _SimpleRWLock()
            _global_locks[cache_key] = lock
        return lock


class CachedDictList:
    """
    Thread-safe cached list of dictionaries with optional equality indexes.

    Parameters
    ----------
    cache_key: str
        Unique key identifying this cached list in shared in-memory cache.
    cache: optional cachetools.Cache-like object
        If not provided, a process-local cache is created.
        The cache object must support __getitem__, __setitem__, __contains__, pop.
    index_keys: optional iterable of str
        Keys in the dictionaries to maintain indexes for (fast equality lookup).
    maxsize: int
        If cachetools.TTLCache/Cache is created here, maxsize is used.
    ttl: optional int
        If provided and cachetools is available, TTLCache(maxsize, ttl) used.
    """

    _STORAGE_META_KEY = "__cached_dict_list_meta__"

    def __init__(
        self,
        cache_key: str,
        cache: Optional[Any] = None,
        index_keys: Optional[Iterable[str]] = None,
        maxsize: int = 1024 * 8,
        ttl: Optional[int] = None,
    ):
        self.cache_key = cache_key
        self._lock = _get_lock_for_key(cache_key)
        self.index_keys = list(index_keys) if index_keys else []
        self._local_cache = cache or self._make_local_cache(maxsize=maxsize, ttl=ttl)

        # initialize storage if missing
        if self.cache_key not in self._local_cache:
            # storage format:
            # {
            #   'uids': list of uid (order preserved),
            #   'items': { uid: dict },
            #   'indexes': { key: { value: set(uids) } }
            # }
            meta = {
                "uids": [],
                "items": {},
                "indexes": {k: defaultdict(set) for k in self.index_keys},
            }
            self._local_cache[self.cache_key] = meta

    def _make_local_cache(self, maxsize: int, ttl: Optional[int]):
        if TTLCache is not None and ttl is not None:
            return TTLCache(maxsize=maxsize, ttl=ttl)
        elif TTLCache is not None and isinstance(TTLCache, type):
            # create a Cache (LRU style) without TTL
            return TTLCache(maxsize=maxsize, ttl=float("inf"))
        else:
            # fallback: simple dict
            return {}

    # ---------- internal helpers ----------
    def _get_storage(self):
        return self._local_cache[self.cache_key]

    def _new_uid(self) -> str:
        return uuid.uuid4().hex

    def _index_add(self, storage, uid: str, item: Dict[str, Any]):
        for key in self.index_keys:
            if key in item:
                storage["indexes"].setdefault(key, defaultdict(set))[item[key]].add(uid)

    def _index_remove(self, storage, uid: str, item: Dict[str, Any]):
        for key in self.index_keys:
            if key in item:
                bucket = storage["indexes"].get(key)
                if bucket is None:
                    continue
                val = item[key]
                s = bucket.get(val)
                if s:
                    s.discard(uid)
                    if not s:
                        del bucket[val]

    def _index_update(
        self, storage, uid: str, old_item: Dict[str, Any], new_item: Dict[str, Any]
    ):
        for key in self.index_keys:
            old = old_item.get(key, None)
            new = new_item.get(key, None)
            if old == new:
                continue
            # remove old
            if old is not None:
                bucket = storage["indexes"].get(key)
                if bucket and old in bucket:
                    bucket[old].discard(uid)
                    if not bucket[old]:
                        del bucket[old]
            # add new
            if new is not None:
                storage["indexes"].setdefault(key, defaultdict(set))[new].add(uid)

    # ---------- public API ----------
    def add(self, item: Dict[str, Any]) -> str:
        """
        Add a single item (dict). Returns internal uid.
        """
        self._lock.acquire_write()
        try:
            storage = self._get_storage()
            uid = self._new_uid()
            storage["items"][uid] = dict(item)  # store copy
            storage["uids"].append(uid)
            self._index_add(storage, uid, item)
            return uid
        finally:
            self._lock.release_write()

    def add_many(self, items: Iterable[Dict[str, Any]]) -> List[str]:
        """Add multiple items atomically. Returns list of uids in input order."""
        self._lock.acquire_write()
        try:
            storage = self._get_storage()
            uids = []
            for item in items:
                uid = self._new_uid()
                storage["items"][uid] = dict(item)
                storage["uids"].append(uid)
                self._index_add(storage, uid, item)
                uids.append(uid)
            return uids
        finally:
            self._lock.release_write()

    def get_all(self) -> List[Dict[str, Any]]:
        """Return shallow copies of all items (order preserved)."""
        self._lock.acquire_read()
        try:
            storage = self._get_storage()
            result = [
                dict(storage["items"][uid])
                for uid in storage["uids"]
                if uid in storage["items"]
            ]
            return result
        finally:
            self._lock.release_read()

    def count(self) -> int:
        self._lock.acquire_read()
        try:
            storage = self._get_storage()
            return len(storage["uids"])
        finally:
            self._lock.release_read()

    def filter_by_key(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """
        Fast path: if `key` was indexed and value is a hashable value, O(k) lookup.
        Otherwise fall back to full scan O(n).
        """
        if key in self.index_keys:
            self._lock.acquire_read()
            try:
                storage = self._get_storage()
                bucket = storage["indexes"].get(key, {})
                uids = bucket.get(value, set()).copy()
                return [
                    dict(storage["items"][uid])
                    for uid in storage["uids"]
                    if uid in uids
                ]
            finally:
                self._lock.release_read()
        # fallback full scan
        return self.find(lambda d: d.get(key) == value)

    def find(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Generic filter by predicate. Predicate is run under read lock.
        """
        self._lock.acquire_read()
        try:
            storage = self._get_storage()
            return [
                dict(item)
                for uid in storage["uids"]
                if (item := storage["items"].get(uid)) is not None and predicate(item)
            ]
        finally:
            self._lock.release_read()

    def get_first(
        self, predicate: Callable[[Dict[str, Any]], bool]
    ) -> Optional[Dict[str, Any]]:
        """Return first matching dict or None."""
        self._lock.acquire_read()
        try:
            storage = self._get_storage()
            for uid in storage["uids"]:
                item = storage["items"].get(uid)
                if item is not None and predicate(item):
                    return dict(item)
            return None
        finally:
            self._lock.release_read()

    def update(
        self,
        predicate: Callable[[Dict[str, Any]], bool],
        updater: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> int:
        """
        Update items matching predicate by applying 'updater' (which returns new dict or modifies in-place and returns it).
        Returns count of updated items.
        """
        self._lock.acquire_write()
        try:
            storage = self._get_storage()
            updated = 0
            for uid in list(storage["uids"]):  # copy because we might mutate structure
                old_item = storage["items"].get(uid)
                if old_item is None:
                    continue
                if predicate(old_item):
                    # create new dict from updater result
                    new_item = updater(dict(old_item))
                    if new_item is None:
                        # if updater returned None, treat as no-op
                        continue
                    # update index structures
                    self._index_update(storage, uid, old_item, new_item)
                    storage["items"][uid] = dict(new_item)
                    updated += 1
            return updated
        finally:
            self._lock.release_write()

    def upsert_by_key(self, key: str, key_value: Any, new_item: Dict[str, Any]) -> str:
        """
        If an item with item[key] == key_value exists, replace it (preserving uid).
        Otherwise add as new item. Returns uid.
        """
        self._lock.acquire_write()
        try:
            storage = self._get_storage()
            # fast path if indexed
            if key in self.index_keys:
                bucket = storage["indexes"].get(key, {})
                uids = bucket.get(key_value)
                if uids:
                    # pick first uid (if multiple, replace first)
                    uid = next(iter(uids))
                    old_item = storage["items"].get(uid)
                    if old_item is not None:
                        self._index_update(storage, uid, old_item, new_item)
                        storage["items"][uid] = dict(new_item)
                        return uid
            # fallback full scan
            for uid in storage["uids"]:
                item = storage["items"].get(uid)
                if item is not None and item.get(key) == key_value:
                    self._index_update(storage, uid, item, new_item)
                    storage["items"][uid] = dict(new_item)
                    return uid
            # not found -> add
            uid = self._new_uid()
            storage["items"][uid] = dict(new_item)
            storage["uids"].append(uid)
            self._index_add(storage, uid, new_item)
            return uid
        finally:
            self._lock.release_write()

    def remove(self, predicate: Callable[[Dict[str, Any]], bool]) -> int:
        """
        Remove items matching predicate. Returns count removed.
        """
        self._lock.acquire_write()
        try:
            storage = self._get_storage()
            removed = 0
            new_uids = []
            for uid in storage["uids"]:
                item = storage["items"].get(uid)
                if item is None:
                    continue
                if predicate(item):
                    # remove from items & indexes
                    self._index_remove(storage, uid, item)
                    storage["items"].pop(uid, None)
                    removed += 1
                else:
                    new_uids.append(uid)
            storage["uids"] = new_uids
            return removed
        finally:
            self._lock.release_write()

    def clear(self):
        """Remove everything for this cache_key."""
        self._lock.acquire_write()
        try:
            self._local_cache[self.cache_key] = {
                "uids": [],
                "items": {},
                "indexes": {k: defaultdict(set) for k in self.index_keys},
            }
        finally:
            self._lock.release_write()
