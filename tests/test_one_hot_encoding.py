import pytest

from pyspark.ml.linalg import SparseVector
from lib.pyspark_preprocesing import one_hot_encoding
from lib.pyspark_startup import init


def test_one_hot_encoding():
    spark = init()
    test_df = spark.createDataFrame(
        [(0.0, 2, 0), (1.0, 3, 1), (2.0, 4, 0)], ["inp1", "inp2", "inp3"]
    )

    result = one_hot_encoding(test_df, ["inp1", "inp3"])
    exp_result = spark.createDataFrame(
        [
            (2, SparseVector(2, {0: 1.0}), SparseVector(1, {0: 1.0})),
            (3, SparseVector(2, {1: 1.0}), SparseVector(1, {})),
            (4, SparseVector(2, {}), SparseVector(1, {0: 1.0})),
        ],
        ["inp2", "inp1_ohe", "inp3_ohe"],
    )

    assert result.take(3) == exp_result.take(3)
