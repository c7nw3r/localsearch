from dataclasses import dataclass
from typing import ClassVar, List, Literal, Union


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
    title: str | None = None
    fields: dict | None = None
    type: Literal["TextSource"] = "TextSource"


@dataclass
class SourcePart:
    text: str
    title: str | None = None
    fields: dict | None = None


@dataclass
class StructuredSource(Source):
    title: str
    parts: list[SourcePart]
    type: Literal["StructuredSource"] = "StructuredSource"


Documents = Union[Document, List[Document]]
