from typing import Union, List
from unittest import TestCase

from localsearch.__spi__ import Document, Encoder
from localsearch.__spi__.types import Vector
from localsearch.searcher.annoy_search import AnnoySearch, AnnoyConfig
from localsearch.searcher.splitter.sentence_splitter import SentenceSplitter


class DummyEncoder(Encoder):

    def get_output_dim(self) -> int:
        return 100

    def __call__(self, texts: Union[str, List[str]]) -> Vector:
        import numpy as np

        if isinstance(texts, list):
            return np.ones((len(texts), 100))
        return np.ones(100)


class AnnoySearcherTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_semantic_search(self):
        import tempfile
        from uuid import uuid4
        tempdir = tempfile.gettempdir() + "/" + str(uuid4())

        config = AnnoyConfig(lang="de", path=tempdir)
        searcher = AnnoySearch(config, DummyEncoder())

        document = Document("abcd", {"text": "Beispiel Text"})
        searcher.append(document)

        results = searcher.read("Beispiel Text")
        assert len(results) == 1
        assert results[0].score == 1

    # noinspection PyMethodMayBeStatic
    def test_text_splitting(self):
        import tempfile
        from uuid import uuid4
        tempdir = tempfile.gettempdir() + "/" + str(uuid4())

        config = AnnoyConfig(lang="de", path=tempdir, splitter=SentenceSplitter(lang="de"))
        searcher = AnnoySearch(config, DummyEncoder())

        document = Document("abcd", {"text": "Das ist ein Beispiel Text. " * 5})
        searcher.append(document)

        results = searcher.read("Beispiel Text")
        assert len(results) == 3
        assert results[0].score == 1
