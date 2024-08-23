import json
import os
from dataclasses import dataclass, field
from typing import List, Union, Optional

from localsearch.__spi__ import ScoredDocument, Document, Lang, IndexedDocument
from localsearch.__spi__.types import Searcher
from localsearch.__util__.string_utils import remove_punctuation, lemmatize, remove_stopwords


@dataclass
class TantivyConfig:
    n: Optional[int] = 5
    path: Optional[str] = None
    lang: Optional[Lang] = None
    saturation: float = field(default_factory=lambda: 0)
    index_name: str = field(default_factory=lambda: "tantivy")


class TantivySearch(Searcher):

    # noinspection PyUnresolvedReferences
    def __init__(self, config: TantivyConfig, readonly: bool = False):
        try:
            import tantivy

            # TODO: append index_name to path
            if config.path is not None and not os.path.exists(config.path):
                os.makedirs(config.path)

            schema_builder = tantivy.SchemaBuilder()
            schema_builder.add_text_field("uuid", stored=True)
            schema_builder.add_text_field("name", stored=True)
            schema_builder.add_text_field("type", stored=True)
            schema_builder.add_text_field("text", stored=True, tokenizer_name=f"{config.lang}_stem")
            schema_builder.add_json_field("data", stored=True)
            schema = schema_builder.build()

            self.TantivyDocument = tantivy.Document
            self.index = tantivy.Index(schema, path=config.path, readonly=readonly)
            self.config = config
        except ImportError:
            raise ValueError("no tantivy library found, please install localsearch[tantivy]")

    def search_by_text(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        # Reload the index to ensure it points to the last commit.
        self.index.reload()
        searcher = self.index.searcher()

        def _saturation(value):
            return value / (value + self.config.saturation)

        query = self._canonicalize(text)
        query = self.index.parse_query(query, ["text"])
        results = searcher.search(query, n or self.config.n).hits
        results = [(_saturation(result[0]), searcher.doc(result[1])) for result in results]

        return [ScoredDocument(result[0], IndexedDocument(
            name=result[1]["name"][0],
            type=result[1]["type"][0],
            text=result[1]["text"][0],
            index=self.config.index_name,
            data=result[1].to_dict()["data"][0]
        )) for result in results]

    def append(self, documents: Union[Document, List[Document]]):
        documents = documents if isinstance(documents, list) else [documents]

        if len(documents) == 0:
            return

        writer = self.index.writer()
        for document in documents:
            text = self._canonicalize(document.text)

            # noinspection PyArgumentList
            tantivy_document = self.TantivyDocument(name=document.name, type=document.type, text=text)
            tantivy_document.add_json("data", json.dumps(document.data))
            writer.add_document(tantivy_document)

        writer.commit()

    def _canonicalize(self, text: str):
        """
        Returns the canonicalized form of the given text by removing punctuation, removing stop words and lemmatizing
        the text
        :param text:
        :return: str
        """
        text = remove_punctuation(text)
        text = remove_stopwords(text, self.config.lang)
        text = lemmatize(text, self.config.lang)
        text = text.replace("+", " ")
        text = text.replace("-", " ")
        text = text.replace("^", " ")
        text = text.replace("`", " ")
        text = text.replace(":", " ")
        text = text.replace("{", " ")
        text = text.replace("}", " ")
        text = text.replace('"', " ")
        text = text.replace("[", " ")
        text = text.replace("]", " ")
        text = text.replace("(", " ")
        text = text.replace(")", " ")
        text = text.replace("~", " ")
        text = text.replace("!", " ")
        text = text.replace("*", " ")
        text = text.replace("\\", " ")
        return text

    def search_by_name(self, source: str, n: Optional[int] = None) -> List[Document]:
        # Reload the index to ensure it points to the last commit.
        self.index.reload()
        searcher = self.index.searcher()

        query = self.index.parse_query(source, ["name"])
        results = searcher.search(query, n or self.config.n).hits
        results = [(result[0], searcher.doc(result[1])) for result in results]

        return [Document(
            name=result[1]["name"][0],
            type=result[1]["type"][0],
            text=result[1]["text"][0],
            data=result[1].to_dict()["data"][0]
        ) for result in results]

    def remove_by_name(self, source: str):
        writer = self.index.writer()
        writer.delete_documents("name", source)
        writer.commit()
