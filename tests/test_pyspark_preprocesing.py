import findspark

findspark.init()

from pyspark_test import assert_pyspark_df_equal
from pyspark.ml.linalg import SparseVector
from lib.pyspark_preprocesing import one_hot_encoding, normalize_by_group
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

    assert_pyspark_df_equal(result, exp_result)


def test_normalize_by_group():
    spark = init()
    test_df = spark.createDataFrame(
        [
            ("a", "c", 1.0, 1.0, 1.0),
            ("a", "c", 2.0, 2.0, 1.0),
            ("a", "c", 3.0, 1.0, 1.0),
            ("b", "c", -1.0, 1.0, 1.0),
            ("b", "c", 1.0, 1.0, 1.0),
        ],
        ["col1", "col2", "col3", "col4", "col5"],
    )

    result = normalize_by_group(spark, test_df, ["col1", "col2"], ["col3", "col4"])

    exp_result = spark.createDataFrame(
        [
            ("a", "c", 1.0, -1.0, -0.5773502691896256),
            ("a", "c", 1.0, 0.0, 1.1547005383792517),
            ("a", "c", 1.0, 1.0, -0.5773502691896256),
            ("b", "c", 1.0, -0.7071067811865475, None),
            ("b", "c", 1.0, 0.7071067811865475, None),
        ],
        ["col1", "col2", "col5", "norm_col3", "norm_col4"],
    )

    assert_pyspark_df_equal(result, exp_result)
