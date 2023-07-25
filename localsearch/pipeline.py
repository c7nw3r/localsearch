from typing import List

import numpy as np

from localsearch.__spi__ import Reader
from localsearch.__spi__.model import RankedDocument, ScoredDocument
from localsearch.__spi__.types import CrossEncoder
from localsearch.__util__.array_utils import unique, flatten
from localsearch.__util__.string_utils import md5


class SearchPipeline:

    def __init__(self, readers: List[Reader], reranker: CrossEncoder):
        self.readers = readers
        self.reranker = reranker

    def search(self, query: str, index_field: str = "text") -> List[RankedDocument]:
        results = flatten([reader.read(query) for reader in self.readers])
        queries = list(map(lambda x: (query, x.document.fields[index_field]), results))

        if len(queries) == 0:
            return []

        scores = self.reranker(queries)
        # noinspection PyTypeChecker
        indices = list(reversed(np.argsort(scores).tolist()))

        def to_ranked_document(document: ScoredDocument, rank_score: float):
            return RankedDocument(score=document.score, document=document.document, rank_score=rank_score)

        results = [to_ranked_document(result, score.item()) for result, score in zip(results, scores)]
        results = [results[i] for i in indices]
        results = unique(results, lambda x: x.document.id)
        results = unique(results, lambda x: md5(x.document.fields[index_field]))
        return list(filter(lambda x: x.rank_score >= 0.001, results))
