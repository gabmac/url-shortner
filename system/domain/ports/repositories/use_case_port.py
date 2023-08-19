from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from system.application.dto.base_dto import BaseDTO

T = TypeVar("T", bound=BaseDTO)


class RequestUseCase(ABC, Generic[T]):
    @abstractmethod
    def execute(self, payload: T) -> T:
        pass
