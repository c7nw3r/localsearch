from dataclasses import dataclass
from typing import List, Literal, Union, Optional


@dataclass
class ScoredDocument:
    score: float
    document: 'IndexedDocument'


@dataclass
class RankedDocument(ScoredDocument):
    rank_score: float


@dataclass
class Document:
    name: str
    type: str
    text: str
    data: dict


@dataclass
class IndexedDocument(Document):
    index: str


@dataclass
class Source:
    id: str


@dataclass
class TextSource(Source):
    text: str
    title: Optional[str] = None
    fields: Optional[dict] = None
    type: Literal["TextSource"] = "TextSource"


@dataclass
class SourcePart:
    text: str
    title: Optional[str] = None
    fields: Optional[dict] = None


@dataclass
class StructuredSource(Source):
    title: str
    parts: List[SourcePart]
    type: Literal["StructuredSource"] = "StructuredSource"


Documents = Union[Document, List[Document]]
