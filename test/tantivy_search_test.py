from unittest import TestCase

from localsearch.__spi__ import Document
from localsearch.searcher.tantivy_search import TantivySearch, TantivyConfig


class TantivySearchTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_fulltext_search(self):
        config = TantivyConfig(lang="de")
        searcher = TantivySearch(config)

        searcher.append(Document("abcd1", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd1", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd2", "document", "Beispiel Text", {}))
        searcher.append(Document("abcd2", "document", "Beispiel Text", {}))

        results = searcher.search_by_text("Beispiel Text")
        assert len(results) == 4
        assert results[0].score == 1

        searcher.remove_by_name("abcd1")
        results = searcher.search_by_text("Beispiel Text")
        assert len(results) == 2

        results = searcher.search_by_name("abcd2")
        assert len(results) == 2

    # noinspection PyMethodMayBeStatic
    def test_remove_by_search(self):
        config = TantivyConfig(lang="de")
        searcher = TantivySearch(config)

        searcher.append(Document("source", "document", "Beispiel Text", {}))
        searcher.append(Document("source", "document", "Beispiel Text", {}))
        searcher.append(Document("source", "document", "Beispiel Text", {}))
        searcher.append(Document("source", "document", "Beispiel Text", {}))

        searcher.remove_by_name("source")
        results = searcher.search_by_text("Beispiel Text")

        assert len(results) == 0
