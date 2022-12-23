from pyspark.ml.linalg import DenseVector


def cosine_similarity(vec1: DenseVector, vec2: DenseVector) -> float:
    """This function returns cosinus simalirity of two Dense Vectors.

    :param vec1:              pyspark.ml.linalg.DenseVector
    :param vec2:             pyspark.ml.linalg.DenseVector
    :return:                float"""

    if not (isinstance(vec1, DenseVector)):
        raise TypeError("vec1 must be a DenseVector")

    if not (isinstance(vec2, DenseVector)):
        raise TypeError("vec1 must be a DenseVector")

    if len(vec1) != len(vec2):
        raise ValueError("Vector must have same length ")

    if all(x == 0 for x in vec1):
        raise ValueError("Vector 1 can not be all zeros")

    if all(x == 0 for x in vec2):
        raise ValueError("Vector 2 can not be all zeros")

    return float(vec1.dot(vec2) / (vec1.norm(2) * vec2.norm(2)))
