from dataclasses import dataclass
from typing import List, Protocol

from localsearch import Document
from localsearch.__spi__.types import DocumentSplitter, Lang


class TextMerger(Protocol):

    def __call__(self, old_text: str, new_text: str) -> str:
        return new_text


@dataclass
class SentenceSplitter(DocumentSplitter):
    text_field: str = "text"
    lang: Lang = "en"
    chunk_size: int = 3
    window_size: int = 1
    text_merger: TextMerger = lambda _, e: e

    def __call__(self, document: Document) -> List[Document]:
        import pysbd
        segmenter = pysbd.Segmenter(language=self.lang, clean=False)
        sentences = segmenter.segment(document.fields[self.text_field])

        def split_document(i: int, new_text: str):
            new_document = Document(id=document.id, fields={**document.fields})
            new_document.id += f"#{i}"

            old_text = new_document.fields[self.text_field]
            new_document.fields[self.text_field] = self.text_merger(old_text, new_text)
            return new_document

        results = [i for i in range(0, len(sentences), self.chunk_size - self.window_size)]
        results = [sentences[i:i + self.chunk_size] for i in results]
        return [split_document(i, " ".join(e)) for i, e in enumerate(results)]
