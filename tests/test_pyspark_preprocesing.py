import findspark

findspark.init()

from pyspark_test import assert_pyspark_df_equal
from pyspark.ml.linalg import SparseVector
from lib.pyspark_preprocesing import (
    one_hot_encoding,
    normalize_by_group,
    count_vectorizer,
    convert_types,
    value_overwrite,
)
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


def test_count_vectorizer():
    spark = init()

    test_df = spark.createDataFrame(
        [("a,bb,c,d", 1), ("c,a", 2), ("bb,c", 3), ("d,c,a", 4)],
        ["col1", "col2"],
    )

    result = count_vectorizer(test_df, "col1")

    exp_result = spark.createDataFrame(
        [
            (1, SparseVector(4, [0, 1, 2, 3], [1.0, 1.0, 1.0, 1.0])),
            (2, SparseVector(4, [0, 1], [1.0, 1.0])),
            (3, SparseVector(4, [0, 3], [1.0, 1.0])),
            (4, SparseVector(4, [0, 1, 2], [1.0, 1.0, 1.0])),
        ],
        ["col2", "col1_vec"],
    )

    assert_pyspark_df_equal(result, exp_result)


def test_convert_types():
    spark = init()

    test_df = spark.createDataFrame(
        [("1", 1.0), ("2", 2.0), ("3", 3.0), ("4", 4.0)], ["col_str", "col_float"]
    )

    result = convert_types(test_df, ["col_str", "col_float"], "int")

    exp_result = spark.createDataFrame(
        [(1, 1), (2, 2), (3, 3), (4, 4)], ["col_str", "col_float"]
    )

    assert_pyspark_df_equal(result, exp_result)

def value_overwrite():
    spark = init()

    test_df = spark.createDataFrame(
        [
            ("1", "kabaret", 10, "Mało wstrząsająca rozrywka.", None),
            ("2", "horror", 7, None, None),
            ("3", "dramat", 9, "Geniusz kina!", "Dużo emocji ....."),
            ("4", "komedia", 5, None, "Mało nie spadłem z krzesła!"),
        ],
        ["id", "rodzaj_produkcji", "rating", "recenzja", "komentarz_publicznosci"]
    )

    result = value_overwrite(test_df, ["rating", "komentarz_publicznosci"], [0, "recenzja"], ["kabaret", "komedia"])

    exp_result = spark.createDataFrame(
        [
            ("1", "kabaret", 0, "Mało wstrząsająca rozrywka.", "Mało wstrząsająca rozrywka."),
            ("2", "horror", 7, None, None),
            ("3", "dramat", 9, "Geniusz kina!", "Dużo emocji ....."),
            ("4", "komedia", 0, None, None),
        ],
        ["id", "rodzaj_produkcji", "rating", "recenzja", "komentarz_publicznosci"]
    )

    assert_pyspark_df_equal(result, exp_result)
    