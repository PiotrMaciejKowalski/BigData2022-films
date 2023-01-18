import findspark

findspark.init()
from pyspark.ml.linalg import Vectors
from lib.preprocessing_function_similarity import merge_dense_vectors
from pyspark_test import assert_pyspark_df_equal
from lib.pyspark_startup import init
def test_merge_dense_vectors():
  spark = init()
  test_dataset = spark.createDataFrame(
    [(0, Vectors.dense([0.0, 10.0, 0.5]), 1.0, Vectors.dense([0.0, 10.0, 0.5]), Vectors.dense([0.0, 10.0, 0.5]))],
    ["id", "hour", "mobile", "userFeatures", "clicked"])
  result = merge_dense_vectors(test_dataset, ["hour", "mobile", "userFeatures"])
  exp_result = spark.createDataFrame(
        [
            (0,Vectors.dense([0.0, 10.0, 0.5]),  Vectors.dense([0.0,10.0,0.5,1.0,0.0,10.0,0.5]))
        ],
        ["id", "clicked", "features"],
    )
  assert_pyspark_df_equal(result, exp_result)
