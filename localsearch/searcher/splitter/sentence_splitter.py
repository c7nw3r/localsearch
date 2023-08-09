from dataclasses import dataclass
from typing import List

from localsearch import Document
from localsearch.__spi__.types import DocumentSplitter, Lang


@dataclass
class SentenceSplitter(DocumentSplitter):
    text_field: str = "text"
    lang: Lang = "en"
    chunk_size: int = 3
    window_size: int = 1

    def __call__(self, document: Document) -> List[Document]:
        import pysbd
        segmenter = pysbd.Segmenter(language=self.lang, clean=False)
        sentences = segmenter.segment(document.fields[self.text_field])

        def split_document(i: int, text: str):
            new_document = Document(id=document.id, fields={**document.fields})
            new_document.id += f"#{i}"
            new_document.fields[self.text_field] = text
            return new_document

        results = [i for i in range(0, len(sentences), self.chunk_size-self.window_size)]
        results = [sentences[i:i + self.chunk_size] for i in results]
        return [split_document(i, " ".join(e)) for i, e in enumerate(results)]
