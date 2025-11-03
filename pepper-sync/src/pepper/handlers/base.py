from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseHandler(ABC, Generic[InputType, OutputType]):

    @abstractmethod
    async def process(self, input_data: InputType) -> OutputType:
        pass
