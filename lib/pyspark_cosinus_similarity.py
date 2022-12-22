# TODO: Tets, checks, exceptions
from pyspark.ml.linalg import DenseVector


def cosine_similarity(vec1: DenseVector, vec2: DenseVector) -> float:
    """This function returns cosinus simalirity of two Dense Vectors.

    :param vec1:              pyspark.ml.linalg.DenseVector
    :param vec2:             pyspark.ml.linalg.DenseVector
    :return:                float"""
    return float(vec1.dot(vec2) / (vec1.norm(2) * vec2.norm(2)))
