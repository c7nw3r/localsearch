from unittest import TestCase

from localsearch.__spi__ import Document
from localsearch.searcher.tantivy_search import TantivySearch, TantivyConfig


class TantivySearcherTest(TestCase):

    # noinspection PyMethodMayBeStatic
    def test_fulltext_search(self):
        config = TantivyConfig(lang="de")
        searcher = TantivySearch(config)

        document = Document("abcd", {"text": "Beispiel Text"})
        searcher.append(document)

        results = searcher.read("Beispiel Text")
        assert len(results) == 1
        assert results[0].score == 1
