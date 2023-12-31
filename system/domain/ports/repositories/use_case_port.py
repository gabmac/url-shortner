from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from system.application.dto.base_dto import BaseDTO

T = TypeVar("T", bound=BaseDTO)
S = TypeVar("S", bound=BaseDTO)
L = TypeVar("L")


class RequestUseCase(ABC, Generic[T, S]):
    @abstractmethod
    def execute(self, payload: T) -> S:
        pass


class RequestUseCaseWithoutBody(ABC, Generic[S]):
    @abstractmethod
    def execute(self, payload: str) -> S:
        pass


class RequestUseCaseWithoutPayload(ABC, Generic[L]):
    @abstractmethod
    def execute(self) -> L:
        pass
