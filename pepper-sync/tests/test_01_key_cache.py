from pepper.cache.key_cache import KeyCache
import pytest


@pytest.fixture
def instance():
    key_cache = KeyCache()
    key_cache.set("test:1", 1)
    key_cache.set("test:2", 2)
    key_cache.set("test:3", 3)

    return key_cache

def test_cache_get(instance):
    result = instance.get("test:1")
    assert result == 1
    

def test_cache_clear(instance):
    instance.clear()
    result = instance.get("test:1")
    assert result == None