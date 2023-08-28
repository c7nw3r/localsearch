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


@dataclass
class Source:
    id: str


@dataclass
class TextSource(Source):
    text: str
    fields: dict


Documents = Union[Document, List[Document]]
