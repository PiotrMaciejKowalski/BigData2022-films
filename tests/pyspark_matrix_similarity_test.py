import unittest

import findspark
from pyspark.ml.linalg import DenseVector
from pyspark_test import assert_pyspark_df_equal

from lib.pyspark_matrix_similarity import (
    cosine_similarity_for_row,
    intersection_over_union_for_row,
)
from lib.pyspark_startup import init

findspark.init()
spark = init()


class TestIntersectionOverUnionForRow(unittest.TestCase):
    def test_required_columns(self):
        # Test that the function raises an assertion error if the input dataframe does not have the required columns

        test_df = spark.createDataFrame([("1", "Movie 1")], ["id", "title"])

        movie_id = "1"
        with self.assertRaises(AssertionError):
            intersection_over_union_for_row(test_df, movie_id, column_name="drrr")

    def test_intersection_over_union(self):
        # Test that the function calculates the cosine similarity correctly for a given movie id
        test_df = spark.createDataFrame(
            [
                ("1", "Movie 1", ["a", "b", "c", "d"]),
                ("2", "Movie 2", ["d", "e", "f", "g"]),
            ],
            ["id", "title", "ludzie"],
        )

        expected_result = spark.createDataFrame(
            [("1", 1.0), ("2", 0.1428571492433548)], ["id", "IoU"]
        )
        movie_id = "1"

        result = intersection_over_union_for_row(
            test_df, movie_id, column_name="ludzie"
        )
        assert_pyspark_df_equal(result, expected_result, check_dtype=False)


class TestCosineSimilarityForRow(unittest.TestCase):
    def test_required_columns(self):
        # Test that the function raises an assertion error if the input dataframe does not have the required columns

        test_df = spark.createDataFrame([("1", "Movie 1")], ["id", "title"])

        movie_id = "1"
        with self.assertRaises(AssertionError):
            cosine_similarity_for_row(test_df, movie_id)

    def test_cosine_similarity_matrix(self):
        # Test that the function calculates the cosine similarity correctly for a given movie id
        test_df = spark.createDataFrame(
            [
                ("1", "Movie 1", DenseVector([1, 1, 1923])),
                ("2", "Movie 2", DenseVector([0, 0, 1923])),
            ],
            ["id", "title", "features"],
        )

        expected_result = spark.createDataFrame(
            [("1", 1.0), ("2", 0.9999997019767761)], ["id", "cos_similarity"]
        )
        movie_id = "1"

        result = cosine_similarity_for_row(test_df, movie_id)
        assert_pyspark_df_equal(result, expected_result, check_dtype=False)
