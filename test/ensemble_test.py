from typing import Union, List
from unittest import TestCase

from localsearch.__spi__ import Document, Encoder
from localsearch.__spi__.types import Vector
from localsearch.ensemble import SearchEnsemble
from localsearch.searcher import TantivySearch, TantivyConfig
from localsearch.searcher.annoy_search import AnnoySearch, AnnoyConfig


class DummyEncoder(Encoder):

    def get_output_dim(self) -> int:
        return 100

    def __call__(self, texts: Union[str, List[str]]) -> Vector:
        import numpy as np

        if isinstance(texts, list):
            return np.ones((len(texts), 100))
        return np.ones(100)


class CustomEnsemble(SearchEnsemble):

    def __init__(self):
        import tempfile
        from uuid import uuid4
        tempdir = tempfile.gettempdir() + "/" + str(uuid4())

        searcher1 = AnnoySearch(AnnoyConfig(path=tempdir), DummyEncoder())
        searcher2 = TantivySearch(TantivyConfig(path=tempdir, lang="de"))
        super().__init__([searcher1, searcher2])


class SearchEnsembleTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_semantic_search(self):
        ensemble = CustomEnsemble()

        ensemble.append([
            Document("abcd1", "source", {"text": "Beispiel Text"}),
            Document("abcd2", "source", {"text": "Beispiel Text"}),
            Document("abcd3", "source", {"text": "Beispiel Text"}),
            Document("abcd4", "source", {"text": "Beispiel Text"})
        ])

        results = ensemble.read("Beispiel Text")
        assert len(results) == 8
        assert results[0].score == 1

        ensemble.remove("abcd1")
        results = ensemble.read("Beispiel Text")
        assert len(results) == 6
