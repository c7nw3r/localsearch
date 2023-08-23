from typing import Union, List, Optional, Protocol

from localsearch import Document, ScoredDocument
from localsearch.__spi__ import Reader, Writer
from localsearch.__util__ import flatten


class Searcher(Reader, Writer, Protocol):
    pass


class SearchEnsemble(Reader, Writer):

    def __init__(self, searchers: List[Searcher]):
        self.searchers = searchers

    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        return flatten([e.read(text, n) for e in self.searchers])

    def append(self, documents: Union[Document, List[Document]]):
        [e.append(documents) for e in self.searchers]

    def remove(self, idx: int | str):
        [e.remove(idx) for e in self.searchers]
