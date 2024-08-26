from typing import Union, List, Optional

from localsearch import Document, ScoredDocument
from localsearch.__spi__.types import Searcher
from localsearch.__util__ import flatten


class SearchEnsemble(Searcher):

    def __init__(self, searchers: List[Searcher]):
        self.searchers = searchers

    def search(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        return flatten([e.search(text, n) for e in self.searchers])

    def append(self, documents: Union[Document, List[Document]]):
        [e.append(documents) for e in self.searchers]

    def remove_by_name(self, source: str):
        [e.remove_by_name(source) for e in self.searchers]
