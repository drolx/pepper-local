from typing import Any, override
from pepper.cache.key_cache import KeyCache
from pepper.handlers.base import BaseHandler
from pepper.pipelines.base_pipeline import BasePipeline
import pytest



class TestState:
    __test__ = False

    name: str
    id: int
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

class TestPipeline(BasePipeline):
    __test__ = False
    
    def __init__(self) -> None:
        super().__init__()
        
class TestOneHandler(BaseHandler[dict[str, Any], TestState | None]):
    __test__ = False

    @override
    async def process(self, input_data: dict[str, Any]) -> TestState | None:
        return TestState(id=input_data["id"], name=input_data["name"])


class TestTwoHandler(BaseHandler[TestState, str | None]):
    __test__ = False

    @override
    async def process(self, input_data: TestState) -> str | None:
        return input_data.name

@pytest.fixture
def instance():
    pipeline = TestPipeline()
    pipeline.add_step(TestOneHandler())
    pipeline.add_step(TestTwoHandler())
    
    return pipeline


@pytest.mark.asyncio
async def test_init_and_processing(instance):

    
    test_data = {
        "id": 1,
        "name": "one"
    }
    test_result = await instance.run(test_data)
    assert test_result == "one"
