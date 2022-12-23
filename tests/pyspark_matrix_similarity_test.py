import unittest

from lib.pyspark_matrix_similarity import cosine_similarity_for_row
from math import isclose
from pyspark.ml.linalg import DenseVector

from lib.pyspark_startup import init

import findspark

findspark.init()
spark = init()

class TestCosineSimilarityForRow(unittest.TestCase):
    def test_required_columns(self):
        # Test that the function raises an assertion error if the input dataframe does not have the required columns

        test_df = spark.createDataFrame([("1", "Movie 1")], ["id", "title"])

        movie_id = "1"
        with self.assertRaises(AssertionError):
            cosine_similarity_for_row(test_df, movie_id)

    def test_cosine_similarity(self):
        # Test that the function calculates the cosine similarity correctly for a given movie id



        test_df = spark.createDataFrame(
            [
                ("1", "Movie 1", DenseVector([1, 1, 1923])),
                ("2", "Movie 2", DenseVector([0, 0, 1923])),
            ],
            ["id", "title", "features"],
        )

        expected_result = spark.createDataFrame(
            [("1", 1.0), ("2", 0.999999729578476)], ["id", "cos_similarity"]
        )

        movie_id = "1"

        result = cosine_similarity_for_row(test_df, movie_id)

        res1: DenseVector = (
            result.filter(result.id == "1").select("cos_similarity").collect()[0][0]
        )
        res2: DenseVector = (
            expected_result.filter(expected_result.id == "1")
            .select("cos_similarity")
            .collect()[0][0]
        )

        self.assertTrue(isclose(res1, res2, rel_tol=1e-9))

