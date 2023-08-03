from dataclasses import dataclass
from typing import Union, List


@dataclass
class ScoredDocument:
    score: float
    document: 'IndexedDocument'


@dataclass
class RankedDocument(ScoredDocument):
    rank_score: float


@dataclass
class Document:
    id: str
    fields: dict


@dataclass
class IndexedDocument(Document):
    index: str


Documents = Union[Document, List[Document]]
