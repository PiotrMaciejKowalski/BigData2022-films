from pyspark.ml.linalg import DenseVector
from math import isclose
import unittest
from lib.pyspark_cosinus_similarity import cosine_similarity


class TestCosineSimilarity(unittest.TestCase):
    def test_known_similarity(self):
        # Test that the function returns the expected result for two vectors with a known cosine similarity of 0
        vec1 = DenseVector([1, 0, 0])
        vec2 = DenseVector([0, 1, 0])
        expected_result = 0
        result = cosine_similarity(vec1, vec2)
        self.assertTrue(isclose(result, expected_result, rel_tol=1e-9))

        # Test that ... with a known cosine similarity of 0.999999729578476
        vec1 = DenseVector([1, 1, 1923])
        vec2 = DenseVector([0, 0, 1923])
        expected_result = 0.999999729578476
        result = cosine_similarity(vec1, vec2)
        self.assertTrue(isclose(result, expected_result, rel_tol=1e-9))

        # Test that ... with a known cosine similarity of -1
        vec1 = DenseVector([1, 2, 3])
        vec2 = DenseVector([-1, -2, -3])
        expected_result = -1
        result = cosine_similarity(vec1, vec2)
        self.assertTrue(isclose(result, expected_result, rel_tol=1e-9))

    def test_result_range(self):
        # Test that the function returns a value between -1 and 1 (inclusive) for any two vectors
        vec1 = DenseVector([1, 2, 3])
        vec2 = DenseVector([3, 2, 1])
        result = cosine_similarity(vec1, vec2)
        self.assertTrue(-1 <= result <= 1)

    def test_input_type(self):
        # Test that the function raises a TypeError if either of the input vectors is not a DenseVector
        with self.assertRaises(TypeError):
            cosine_similarity(DenseVector([1, 2, 3]), DenseVector([3, 2, 1]))
        with self.assertRaises(TypeError):
            cosine_similarity(DenseVector([1, 2, 3]), DenseVector([3, 2, 1]))

    def test_input_dimension(self):
        # Test that the function raises a ValueError if the input vectors have different dimensions
        vec1 = DenseVector([1, 2, 3])
        vec2 = DenseVector([3, 2])
        with self.assertRaises(ValueError):
            cosine_similarity(vec1, vec2)

    def test_zero_norm(self):
        # Test that the function handles input vectors with all zero elements correctly
        vec1 = DenseVector([0, 0, 0])
        vec2 = DenseVector([0, 0, 0])

        with self.assertRaises(ValueError):
            cosine_similarity(vec1, vec2)

    def test_single_element(self):
        # Test that the function handles input vectors with a single element correctly
        vec1 = DenseVector([2])
        vec2 = DenseVector([4])
        expected_result = 1
        result = cosine_similarity(vec1, vec2)

        self.assertEqual(result, expected_result)
