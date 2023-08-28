from abc import ABC, abstractmethod

from localsearch.__spi__.model import Source


class SourceRepo(ABC):

    @abstractmethod
    def add(self, sources: list[Source]) -> None:
        pass

    @abstractmethod
    def get(self, id: str) -> Source:
        pass
