from abc import ABC, abstractmethod
from typing import List, Union, Literal, Protocol, Sized, Optional, Tuple

from localsearch.__spi__ import IndexedDocument, ScoredDocument


class Reader(ABC):

    @abstractmethod
    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        pass


class Writer(ABC):

    @abstractmethod
    def append(self, documents: List[IndexedDocument]):
        pass

    @abstractmethod
    def remove(self, idx: int):
        pass


class Vector(Protocol, Sized):
    def __getitem__(self, __index: int) -> float: ...


class Encoder(ABC):

    @abstractmethod
    def get_output_dim(self) -> int:
        pass

    @abstractmethod
    def __call__(self, texts: Union[str, List[str]]) -> Vector:
        pass


TextPair = Tuple[str, str]


class CrossEncoder(ABC):

    @abstractmethod
    def __call__(self, texts: Union[TextPair, List[TextPair]]) -> Vector:
        pass


Lang = Literal["de", "en"]
