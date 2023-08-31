from unittest import TestCase

from localsearch.__spi__ import Document
from localsearch.searcher.tantivy_search import TantivySearch, TantivyConfig


class TantivySearcherTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_fulltext_search(self):
        config = TantivyConfig(lang="de")
        searcher = TantivySearch(config)

        searcher.append(Document("abcd1", "source", {"text": "Beispiel Text"}))
        searcher.append(Document("abcd2", "source", {"text": "Beispiel Text"}))
        searcher.append(Document("abcd3", "source", {"text": "Beispiel Text"}))
        searcher.append(Document("abcd4", "source", {"text": "Beispiel Text"}))

        results = searcher.read("Beispiel Text")
        assert len(results) == 4
        assert results[0].score == 1

        searcher.remove("abcd1")
        results = searcher.read("Beispiel Text")
        assert len(results) == 3

        results = searcher.search_by_source("source")
        assert len(results) == 3
