import os
from tempfile import mkdtemp
from typing import List, Union
from unittest import TestCase

from localsearch.__spi__ import Document
from localsearch.__spi__.types import CrossEncoder, TextPair, Vector
from localsearch.pipeline import IndexPipeline, SearchPipeline
from localsearch.searcher.tantivy_search import TantivyConfig, TantivySearch


class DummyCrossEncoder(CrossEncoder):

    def __call__(self, texts: Union[TextPair, List[TextPair]]) -> Vector:
        import numpy as np
        return np.ones(len(texts))


class PipelineTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_pipeline_with_cross_encoder(self):
        config = TantivyConfig(lang="de")
        searcher = TantivySearch(config)

        document = Document("abcd", {"text": "Beispiel Text"})
        [searcher.append(document) for _ in range(5)]

        pipeline = SearchPipeline([searcher], DummyCrossEncoder())
        print(pipeline.search("Beispiel Text"))

    # noinspection PyMethodMayBeStatic
    def test_pipeline_without_cross_encoder(self):
        config = TantivyConfig(lang="de")
        searcher = TantivySearch(config)

        document = Document("abcd", {"text": "Beispiel Text"})
        [searcher.append(document) for _ in range(5)]

        pipeline = SearchPipeline([searcher])
        print(pipeline.search("Beispiel Text"))

    def test_index_pipeline(self):
        config = TantivyConfig(lang="de")
        writer = TantivySearch(config)

        tmp_dir = mkdtemp()
        pipeline = IndexPipeline(tmp_dir, [writer])

        docs = [Document("abcd", {"text": "Beispiel Text"}) for _ in range(5)]

        pipeline.add(docs)

        self.assertEqual(len(os.listdir(tmp_dir)), 5)
