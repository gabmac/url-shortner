from abc import ABC, abstractmethod


class BaseRouterView(ABC):
    @abstractmethod
    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
