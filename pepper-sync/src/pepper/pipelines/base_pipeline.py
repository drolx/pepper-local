from abc import ABC
import asyncio
from typing import Any, TypeVar

from pepper.handlers.base import BaseHandler


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")



class BasePipeline(ABC):
    def __init__(self) -> None:
        self.steps: list[BaseHandler[Any, Any]] = []

    def add_step(self, step: BaseHandler[InputType, OutputType]) -> None:
        if self.steps:
            # Validate type compatibility between last step's output and new step's input
            last_step = self.steps[-1]
            if not isinstance(last_step, BaseHandler) or not isinstance(step, BaseHandler):
                raise TypeError("Pipeline steps must inherit from the BaseHandler class.")

        self.steps.append(step)

    async def run(self, input_data: Any) -> Any:
        data: Any | None = input_data
        for step in self.steps:
            if data is None:
                break
            data = await step.process(data)

        await asyncio.sleep(1)

        return data
