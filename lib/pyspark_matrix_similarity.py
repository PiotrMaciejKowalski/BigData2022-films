from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import DataFrame
from typing import List, Literal
from pyspark.ml.feature import VectorAssembler
from lib.pyspark_cosinus_similarity import cosineSimilarity
import numpy as np
def cosine_similarity_for_row(
    df: DataFrame,
    movie_id: str,
) -> DataFrame:
    """This function returns a Spark dataframe that contains similarity calculations for the given movie_id.
       There should not be any null values in the DataFrame, and all categorical values should be one-hot encoded.
       All other numeric values, such as Year, rating should be normalized.

    :param df:              pyspark.sql.DataFrame
    :param movie_id:         String
    :return:                pyspark.sql.DataFrame"""



    row_df = df.filter(df.index == movie_id)
    vector_assembler = VectorAssembler(inputCols=df.columns, outputCol="features")
    vectorized_df = vector_assembler.transform(row_df)

    cosine_similarity = cosineSimilarity(inputCol="features", outputCol="sim")
    sim_df = cosine_similarity.transform(vectorized_df)

    sims = sim_df.select("sim").collect()

    return np.array([row[0] for row in sims])

   # X, Y = check_pairwise_arrays(X, Y)
   #
   #  X_normalized = normalize(X, copy=True)
   #  if X is Y:
   #      Y_normalized = X_normalized
   #  else:
   #      Y_normalized = normalize(Y, copy=True)
   #
   #  K = safe_sparse_dot(X_normalized, Y_normalized.T, dense_output=dense_output)
   #
   #  return K