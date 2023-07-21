import numpy as np
from numpy import matmul
from numpy.linalg import norm


def cosine_similarity(a, b) -> float:
    a = np.expand_dims(a, axis=0) if len(a.shape) == 1 else a
    b = np.expand_dims(b, axis=0) if len(b.shape) == 1 else b
    a_norm = a / norm(a, ord=2, axis=1, keepdims=True)
    b_norm = b / norm(b, ord=2, axis=1, keepdims=True)

    similarity = np.ravel(matmul(a_norm, b_norm.transpose())).item()
    return min(1.0, similarity)


def unique(array: list, get_key):
    keys = []
    vals = []

    for item in array:
        key = get_key(item)
        if key not in keys:
            keys.append(key)
            vals.append(item)

    return vals


def flatten(array: list):
    return [item for sublist in array for item in sublist]
