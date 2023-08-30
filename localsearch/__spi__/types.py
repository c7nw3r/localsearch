from abc import ABC, abstractmethod
from typing import List, Union, Literal, Protocol, Sized, Optional, Tuple

from localsearch.__spi__ import Document, ScoredDocument


class Reader(Protocol):

    @abstractmethod
    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        pass


class Writer(Protocol):

    @abstractmethod
    def append(self, documents: Union[Document, List[Document]]):
        pass

    @abstractmethod
    def remove(self, idx: str):
        pass


class Traverser(ABC):

    @abstractmethod
    def add_node(self, node_id: str, fields: dict):
        pass

    @abstractmethod
    def add_edge(self, source_id: str, target_id: str, edge_type: str):
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


class DocumentSplitter(Protocol):

    @abstractmethod
    def __call__(self, document: Document) -> List[Document]:
        pass
