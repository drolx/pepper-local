from pepper.cache.queue_manager import QueueManager
import pytest

queue_key = "test_queue"

@pytest.fixture
def instance():
    queue = QueueManager(queue_key)
    queue.push({"id": 1, "status": "x"})
    queue.push({"id": 2, "status": "y"})

    return queue
    
def test_check_queue_size(instance):
    queue_size = instance.size()
    assert queue_size == 2

def test_pop_queue_item(instance):
    item = instance.pop()
    assert item["id"] == 1

def test_queue_items(instance):
    queues = instance.list_queues()
    result = any(item in queue_key for item in queues)
    assert result == True

def test_queue_clear(instance):
    instance.clear()
    items = instance.size()
    assert items == 0