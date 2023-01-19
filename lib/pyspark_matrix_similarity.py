import pyspark.sql.functions as f
from pyspark.ml.linalg import DenseVector
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType

from lib.metrics import intersection_over_union
from lib.pyspark_cosinus_similarity import cosine_similarity


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


def intersection_over_union_for_row(
    df: DataFrame,
    movie_id: str,
    column_name: str = "ludzie_filmu",
) -> DataFrame:
    """This function returns a DataFrame that contains intersection_over_union calculations for the given movie_id.

    Example:
            input Dataframe
        +---------+-----------------------------+
        |       id|          ludzie_filmu       |
        +---------+-----------------------------+
        |tt0000001|       ["a", "b", "c", "d"]  |
        |tt0000003|       ["d", "e", "f", "g"]  |
        +---------+-----------------------------+

        intersection_over_union_for_row(df, "tt0000001", column_name = "ludzie_filmu" )

            output

        +---------+---------------+
        |       id|     IoU       |
        +---------+---------------+
        |tt0000001|       1       |
        |tt0000003|     0.142     |
        +---------+---------------+



    :param column_name:     String
    :param df:              pyspark.sql.DataFrame
    :param movie_id:        String
    :return:                pyspark.sql.DataFrame"""

    if not ("id" in df.columns and column_name in df.columns):
        raise AssertionError("input dataframe does not have the required columns")

    assert (df[str(col)].isNull() for col in df.columns)

    vector1: DenseVector = (
        df.filter(df.id == movie_id).select(column_name).collect()[0][0]
    )

    def IOU(x):
        return intersection_over_union(vector1, x)

    my_udf = f.udf(IOU, FloatType())

    df = df.withColumn("IoU", my_udf(f.col(column_name)))

    return df.select(["id", "IoU"])
