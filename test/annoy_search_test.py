from typing import Union, List
from unittest import TestCase

from localsearch.__spi__ import Document, Encoder
from localsearch.__spi__.types import Vector
from localsearch.searcher.annoy_search import AnnoySearch, AnnoyConfig


class DummyEncoder(Encoder):

    def get_output_dim(self) -> int:
        return 100

    def __call__(self, texts: Union[str, List[str]]) -> Vector:
        import numpy as np

        if isinstance(texts, list):
            return np.ones((len(texts), 100))
        return np.ones(100)


class AnnoySearchTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_semantic_search(self):
        import tempfile
        from uuid import uuid4
        tempdir = tempfile.gettempdir() + "/" + str(uuid4())

        config = AnnoyConfig(path=tempdir)
        searcher = AnnoySearch(config, DummyEncoder())

        document = Document("abcd", "document", "Beispiel Text", {})
        searcher.append(document)

        results = searcher.search("Beispiel Text")
        assert len(results) == 1
        assert results[0].score == 1

        searcher.remove_by_name("abcd")
        results = searcher.search("Beispiel Text")
        assert len(results) == 0

    def test_existing_index(self):
        import tempfile
        from uuid import uuid4
        tempdir = tempfile.gettempdir() + "/" + str(uuid4())

        config = AnnoyConfig(path=tempdir)
        searcher = AnnoySearch(config, DummyEncoder())

        searcher.append(Document("abcd1", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd1", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd2", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd2", "document", "Beispiel Text", {}))

        searcher = AnnoySearch(config, DummyEncoder())

        results = searcher.search("Beispiel Text")
        assert len(results) == 4
        assert results[0].score == 1

        searcher.remove_by_name("abcd1")
        results = searcher.search("Beispiel Text")
        assert len(results) == 2

        results = searcher.search("abcd2")
        assert len(results) == 2

    def test_remove_by_source(self):
        import tempfile
        from uuid import uuid4
        tempdir = tempfile.gettempdir() + "/" + str(uuid4())

        config = AnnoyConfig(path=tempdir)
        searcher = AnnoySearch(config, DummyEncoder())

        searcher.append(Document("abcd", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd", "document", "Beispiel Text", {}))

        searcher = AnnoySearch(config, DummyEncoder())
        searcher.remove_by_name("abcd")

        results = searcher.search("Beispiel Text")
        assert len(results) == 0
