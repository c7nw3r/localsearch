from typing import Union, List, Optional

from localsearch import Document, ScoredDocument
from localsearch.__spi__.types import Searcher
from localsearch.__util__ import flatten


class SearchEnsemble(Searcher):

    def __init__(self, searchers: List[Searcher]):
        self.searchers = searchers

    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        return flatten([e.read(text, n) for e in self.searchers])

    def append(self, documents: Union[Document, List[Document]]):
        [e.append(documents) for e in self.searchers]

    def remove(self, idx: str):
        [e.remove(idx) for e in self.searchers]

    def search_by_source(self, source: str, n: Optional[int] = None) -> List[Document]:
        return flatten([e.search_by_source(source) for e in self.searchers])

    def remove_by_source(self, source: str):
        [e.remove_by_source(source) for e in self.searchers]
