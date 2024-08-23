import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Literal, Optional, Union

from localsearch.__spi__ import Document, Encoder, IndexedDocument, ScoredDocument
from localsearch.__spi__.types import Searcher
from localsearch.__util__.array_utils import cosine_similarity
from localsearch.__util__.io_utils import delete_folder, grep, list_files, read_json, write_json


@dataclass
class AnnoyConfig:
    path: str
    n: int = 5
    n_trees: int = 10
    search_k: int = -1  # defaults to n_trees * n
    index_name: Optional[str] = "annoy"
    metric: Literal["angular", "euclidean", "manhattan", "hamming", "dot"] = "euclidean"


class AnnoySearch(Searcher):
    """
    Semantic search implementation which is based on the annoy library (https://github.com/spotify/annoy)

    This search implementation supports read as well as write functionality.
    """

    def __init__(self, config: AnnoyConfig, encoder: Encoder):
        try:
            from annoy import AnnoyIndex

            self.path = config.path + f"/{config.index_name}.ann"
            self.encoder = encoder
            self.index = AnnoyIndex(encoder.get_output_dim(), config.metric)
            self.AnnoyIndex = AnnoyIndex
            if os.path.exists(self.path):
                self.index.load(self.path)
            else:
                os.makedirs(config.path)
            self.config = config
        except ImportError:
            raise ValueError("no annoy library found, please install localsearch[annoy]")

    def search_by_text(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        import numpy as np
        vector = self.encoder(text)
        indices = self.index.get_nns_by_vector(vector, n or self.config.n, self.config.search_k)
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

        batch = [d.text for d in documents]
        vectors = self.encoder(batch)

        for i, vector in enumerate(vectors):
            # self.id_map[idx + i] = documents[i].id
            self.index.add_item(idx + i, vector)
            document = documents[i]
            write_json(f"{folder}/{document.name}/{idx + i}.json", asdict(documents[i]))

        self._save()

    def _rebuild(self):
        """
        Rebuilds the entire annoy index. Annoy does not support incremental updates so each delete/append call
        leads to a rebuild of the index.

        For performance reasons it is recommended to append documents in batches.
        """
        new_index = self.AnnoyIndex(self.encoder.get_output_dim(), self.config.metric)
        folder = self.path.replace(".ann", "")
        for path in list_files(folder, recursive=True):
            path = Path(path)
            if path.suffix == ".json":
                idx = int(path.stem)
                vector = self.index.get_item_vector(idx)
                new_index.add_item(idx, vector)

        os.remove(self.path)
        self.index = new_index

    def _save(self):
        print("path", self.path)
        self.index.build(self.config.n_trees)
        self.index.save(self.path)

    def _read_document(self, idx: str) -> IndexedDocument:
        folder = self.path.replace(".ann", "")
        return IndexedDocument(**read_json(grep(folder, str(idx))), index=self.config.index_name)

    def search_by_name(self, source: str, n: Optional[int] = None) -> List[Document]:
        folder = self.path.replace(".ann", "")
        files = list_files(f"{folder}/{source}")
        return [Document(**read_json(f"{folder}/{source}/{e}")) for e in files]

    def remove_by_name(self, source: str):
        folder = self.path.replace(".ann", "")
        delete_folder(f"{folder}/{source}")

        self._rebuild()
        self._save()
