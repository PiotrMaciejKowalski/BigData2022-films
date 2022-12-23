from pyspark.sql import DataFrame
from lib.pyspark_cosinus_similarity import cosine_similarity
import pyspark.sql.functions as f
from pyspark.sql.types import FloatType
from pyspark.ml.linalg import DenseVector


def cosine_similarity_for_row(
    df: DataFrame,
    movie_id: str,
) -> DataFrame:
    """This function returns a DataFrame that contains cosinus similarity calculations for the given movie_id.


    :param df:              pyspark.sql.DataFrame
    :param movie_id:        String
    :return:                pyspark.sql.DataFrame"""

    if not ("id" in df.columns and "features" in df.columns):
        raise AssertionError("input dataframe does not have the required columns")

    # assert "movie_id" in df.columns and "features" in df.columns
    assert (df[str(col)].isNull() for col in df.columns)








    vector1: DenseVector = (
        df.filter(df.id == movie_id).select("features").collect()[0][0]
    )

    def cos(x):
        return cosine_similarity(vector1, x)

    my_udf = f.udf(cos, FloatType())

    df = df.withColumn("cos_similarity", my_udf(f.col("features")))

    return df.select(["id", "cos_similarity"])
