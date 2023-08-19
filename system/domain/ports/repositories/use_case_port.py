from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from system.application.dto.base_dto import BaseDTO

T = TypeVar("T", bound=BaseDTO)
S = TypeVar("S", bound=BaseDTO)


class RequestUseCase(ABC, Generic[T, S]):
    @abstractmethod
    def execute(self, payload: T) -> S:
        pass
