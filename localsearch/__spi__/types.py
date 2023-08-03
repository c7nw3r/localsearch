from abc import ABC, abstractmethod
from typing import List, Union, Literal, Protocol, Sized, Optional, Tuple

from localsearch import Document
from localsearch.__spi__ import ScoredDocument


class Reader(ABC):

    @abstractmethod
    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        pass


class Writer(ABC):

    @abstractmethod
    def append(self, documents: Union[Document, List[Document]]):
        pass

    @abstractmethod
    def remove(self, idx: int):
        pass


class Traverser(ABC):

    @abstractmethod
    def add_edges(self, source_id: str, target_id: str, edge_type: str):
        pass

    @abstractmethod
    def get_edges(self, node_id: str):
        pass

    @abstractmethod
    def search_by_type(self, node_type: str):
        pass

    @abstractmethod
    def search_by_id(self, node_id: str):
        pass


class Vector(Protocol, Sized):
    def __getitem__(self, __index: int) -> float: ...


class Encoder(Protocol):

    def get_output_dim(self) -> int:
        pass

    def __call__(self, texts: Union[str, List[str]]) -> Vector:
        pass


TextPair = Tuple[str, str]


class CrossEncoder(Protocol):

    def __call__(self, texts: Union[TextPair, List[TextPair]]) -> Vector:
        pass


Lang = Literal["de", "en"]
