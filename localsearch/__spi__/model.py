from dataclasses import dataclass


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
