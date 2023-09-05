from dataclasses import dataclass, asdict
from typing import List, Optional
import os
from pathlib import Path

import numpy as np
from tqdm import tqdm

from localsearch.__spi__ import Reader, Writer
from localsearch.__spi__.model import RankedDocument, ScoredDocument, Documents
from localsearch.__spi__.types import CrossEncoder
from localsearch.__util__.array_utils import unique, flatten
from localsearch.__util__.string_utils import md5
from localsearch.__util__.io_utils import write_json


@dataclass
class SearchConfig:
    n: int = 5
    min_rank_score: float = 0.001
    unique_hash: bool = True


class SearchPipeline:

    def __init__(self, readers: List[Reader], reranker: Optional[CrossEncoder] = None):
        self.readers = readers
        self.reranker = reranker

    def search(
            self,
            query: str,
            index_field: str = "text",
            config: SearchConfig = SearchConfig()
    ) -> List[RankedDocument]:

        results = flatten([reader.read(query) for reader in self.readers])
        results = unique(results, lambda x: x.document.id)
        queries = list(map(lambda x: (query, x.document.fields[index_field]), results))

        if len(queries) == 0:
            return []

        if self.reranker is not None:
            scores = self.reranker(queries)
            # noinspection PyTypeChecker
            indices = list(reversed(np.argsort(scores).tolist()))
        else:
            scores = np.full(len(queries), config.min_rank_score)
            indices = [i for i in range(len(queries))]

        def to_ranked_document(document: ScoredDocument, rank_score: float):
            return RankedDocument(score=document.score, document=document.document, rank_score=rank_score)

        results = [to_ranked_document(result, score.item()) for result, score in zip(results, scores)]
        results = [results[i] for i in indices]
        if config.unique_hash:
            results = unique(results, lambda x: md5(x.document.fields[index_field]))
        if config.min_rank_score > 0:
            results = list(filter(lambda x: x.rank_score >= config.min_rank_score, results))
        return results[:config.n]


class IndexPipeline:

    def __init__(
            self,
            raw_data_dir: str,
            writers: List[Writer],
    ) -> None:

        self._raw_data_dir = raw_data_dir
        if not os.path.exists(raw_data_dir):
            os.makedirs(raw_data_dir)
        self._writers = writers

    def add(self, docs: Documents, batch_size: int | None = None, verbose: bool = False) -> None:
        docs = docs if isinstance(docs, list) else [docs]
        batch_size = batch_size if batch_size else len(docs)

        idxs = range(0, len(docs), batch_size)
        for idx in tqdm(idxs, total=len(idxs)) if verbose else idxs:
            docs_batch = docs[idx: idx+batch_size]

            for writer in self._writers:
                writer.append(docs_batch)

            for idx, doc in enumerate(docs_batch, self._get_start_idx()):
                write_json(Path(self._raw_data_dir) / f"{idx}.json", asdict(doc))

    def _get_start_idx(self) -> int:
        idxs = [
            int(fn.removesuffix(".json")) for fn in os.listdir(self._raw_data_dir)
            if fn.endswith(".json")
        ]

        return max(idxs) + 1 if idxs else 0
