from pepper.cache.cache_manager import CacheManager
import pytest

@pytest.fixture
def instance():
    cache_user = CacheManager("test_object_user", index_keys=["id", "email", "name"])
    _ = cache_user.add({"id": 1, "email": "a@example.com", "name": "Alice"})
    _ = cache_user.add({"id": 2, "email": "b@example.com", "name": "Bob"})
    _ = cache_user.add({"id": 3, "email": "j@example.com", "name": "John"})
    
    return cache_user
    
def test_00_filter_by_key(instance):
    results = instance.filter_by_key("email", "a@example.com")
    target_value = results[0]
    assert target_value["email"] == "a@example.com"

def test_01_find_by_lamda(instance):
    results = instance.find(lambda d: d["name"].startswith("B"))
    target_value = results[0]
    assert target_value["name"] == "Bob"

def test_02_update_by_lamda(instance):
    def updater(d):
        d["name"] = d["name"].upper()
        return d
    count = instance.update(lambda x: x["id"] == 2, updater)
    results = instance.find(lambda d: d["id"] == 2)
    target_value = results[0]
    assert count == 1 and target_value["name"] == "BOB"


def test_03_remove_by_lamda(instance):
    instance.remove(lambda d: d["id"] == 1)
    results = instance.find(lambda d: d["id"] == 1)
    assert len(results) == 0
