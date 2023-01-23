import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from pyspark.sql.functions import desc
from pyspark.sql.types import FloatType

from lib.pyspark_matrix_similarity import cos_sim_and_iou_for_row


def train(df: DataFrame, movie_name: str = None, movie_id: str = None):
    """This function returns a DataFrame that contains finally similarity for the given movie.
    :param df:               pyspark.sql.DataFrame
    :param movie_name:       String
    :param movie_id:         String
    :return:                 pyspark.sql.DataFrame"""
    if movie_name is None and movie_id is None:
        raise AssertionError("You need to give movie_name or movie_id")
    if movie_id is None:
        movie_id = df.filter(df.tytul == movie_name).select("id").collect()[0][0]

    return cos_sim_and_iou_for_row(df=df, movie_id=movie_id)


def predict(df: DataFrame, a_param: float = 0.5) -> DataFrame:
    """This function returns a DataFrame that contains finally similarity for the given movie_id in scale form 0 to 1.

    :param a_param:          float
    :param df:               pyspark.sql.DataFrame
    :return:                 pyspark.sql.DataFrame"""

    if a_param < 0:
        raise AttributeError("a_param can not be negative")

    add_udf = f.udf(lambda x, y: a_param * x + (1 - a_param) * y, FloatType())

    df = df.withColumn("prediction", add_udf(df["cos_similarity"], df["IOU"]))

    return df.sort(desc("prediction"))
