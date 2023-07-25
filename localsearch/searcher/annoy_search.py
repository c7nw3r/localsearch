import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union

import numpy as np

from localsearch.__spi__ import IndexedDocument, Reader, Encoder, Writer, ScoredDocument, Document
from localsearch.__util__.array_utils import cosine_similarity


@dataclass
class AnnoyConfig:
    n: Optional[int] = 5
    k: Optional[int] = 5
    path: Optional[str] = None
    lang: Optional[str] = None
    index_name: Optional[str] = field(default_factory=lambda: "annoy")
    index_fields: Optional[List[str]] = field(default_factory=lambda: ["text"])


class AnnoySearch(Reader, Writer):
    """
    Semantic search implementation which is based on the annoy library (https://github.com/spotify/annoy)

    This search implementation supports read as well as write functionality.
    """

    def __init__(self, config: AnnoyConfig, encoder: Encoder):
        try:
            from annoy import AnnoyIndex

            self.path = config.path + "/data.ann"
            self.encoder = encoder
            self.index = AnnoyIndex(encoder.get_output_dim(), 'euclidean')
            self.AnnoyIndex = AnnoyIndex
            if os.path.exists(self.path):
                self.index.load(self.path)
            self.config = config
        except ImportError:
            raise ValueError("no annoy library found, please install localsearch[annoy]")

    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        vector = self.encoder(text)
        indices = self.index.get_nns_by_vector(vector, n or self.config.n, search_k=self.config.k)
        vectors = [self.index.get_item_vector(i) for i in indices]
        scores = [cosine_similarity(np.array(item), vector) for item in vectors]

        documents = [self._read_document(idx) for idx in indices]
        return [ScoredDocument(s, d) for s, d in zip(scores, documents)]

    def append(self, documents: Union[Document, List[Document]]):
        documents = documents if isinstance(documents, list) else [documents]

        if len(documents) == 0:
            return []

        if os.path.exists(self.path):
            self._rebuild()

        folder = self.path.replace(".ann", "")
        idx = self.index.get_n_items()

        def to_text(document: Document):
            return " ".join([document.fields[e] for e in self.config.index_fields])

        batch = [to_text(d) for d in documents]
        vectors = self.encoder(batch)

        for i, vector in enumerate(vectors):
            self.index.add_item(idx + i, vector)
            from localsearch.__util__.io_utils import write_json
            write_json(f"{folder}/{idx + i}.json", asdict(documents[i]))

        self._save()

    def remove(self, idx: int):
        folder = self.path.replace(".ann", "")
        os.remove(f"{folder}/{idx}.json")

        self._rebuild()
        self._save()

    def _rebuild(self):
        """
        Rebuilds the entire annoy index. Annoy does not support incremental updates so each delete/append call
        leads to a rebuild of the index.

        For performance reasons it is recommended to append documents in batches.
        """
        folder = self.path.replace(".ann", "")
        new_index = self.AnnoyIndex(self.encoder.get_output_dim(), 'euclidean')
        for path in os.listdir(folder):
            if path.endswith(".json"):
                idx = int(path.replace(".json", ""))
                vector = self.index.get_item_vector(idx)
                new_index.add_item(idx, vector)

        os.remove(self.path)
        self.index = new_index

    def _save(self):
        self.index.build(10)
        self.index.save(self.path)

    def _read_document(self, idx: int) -> IndexedDocument:
        folder = self.path.replace(".ann", "")
        with open(f"{folder}/{idx}.json") as f:
            return IndexedDocument(**json.load(f), index=self.config.index_name)
