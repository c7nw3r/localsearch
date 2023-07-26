from typing import List, Dict

import numpy as np
from numpy import matmul
from numpy.linalg import norm

from localsearch import ScoredDocument


def cosine_similarity(a, b) -> float:
    a = np.expand_dims(a, axis=0) if len(a.shape) == 1 else a
    b = np.expand_dims(b, axis=0) if len(b.shape) == 1 else b
    a_norm = a / norm(a, ord=2, axis=1, keepdims=True)
    b_norm = b / norm(b, ord=2, axis=1, keepdims=True)

    similarity = np.ravel(matmul(a_norm, b_norm.transpose())).item()
    return min(1.0, similarity)


def sort(array: List[ScoredDocument]):
    def sort_by_score(document: ScoredDocument):
        return document.score

    return list(sorted(array, key=sort_by_score))


def unique(array: List[ScoredDocument], get_key):
    documents: Dict[str, ScoredDocument] = {}

    for item in array:
        key = get_key(item)

        if key in documents:
            document = documents[key]
            if item.score > document.score:
                documents[key] = item
        else:
            documents[key] = item

    return sort(list(documents.values()))


def flatten(array: list):
    return [item for sublist in array for item in sublist]
