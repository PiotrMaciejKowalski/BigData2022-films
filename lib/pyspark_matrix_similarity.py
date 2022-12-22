from pyspark.sql import DataFrame
from lib.pyspark_cosinus_similarity import cosine_similarity
from pyspark.ml.linalg import DenseVector
import pandas as pd


def cosine_similarity_for_row(
    df: DataFrame,
    movie_id: str,
) -> pd.DataFrame:
    """This function returns a Pandas dataframe that contains similarity calculations for the given movie_id.
       There should not be any null values in the DataFrame, and all categorical values should be one-hot encoded.
       All other numeric values, such as Year, rating should be normalized.

    :param df:              pyspark.sql.DataFrame
    :param movie_id:         String
    :return:                pandas.DataFrame"""

    similarity_df: pd.DataFrame = pd.DataFrame(columns=["movie_id", "similarity"])

    assert "movie_id" in df.columns and "features" in df.columns
    assert not any(df.select(col).na.drop().count() < df.count() for col in df.columns)

    vector1: DenseVector = (
        df.filter(df.id == movie_id).select("features").collect()[0][0]
    )

    for i in range(df.count()):
        tem_mov_id: str = str(df.select("id").collect()[i][0])
        vector2: DenseVector = df.select("features").collect()[i][0]
        cos_similarity: float = cosine_similarity(vector1, vector2)
        similarity_df = similarity_df.append(
            {"movie_id": str(tem_mov_id), "similarity": cos_similarity}
        )

    return similarity_df
