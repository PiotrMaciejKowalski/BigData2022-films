import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from pyspark.sql.functions import desc
from pyspark.sql.types import FloatType

from lib.pyspark_matrix_similarity import cos_sim_and_iou_for_row


class Model:
    def __init__(self, df: DataFrame):
        self.df = df
        self.trained_df = None

    def train(self, movie_name: str = None, movie_id: str = None) -> DataFrame:
        """This function returns a DataFrame that contains finally similarity for the given movie.
        :param movie_name:       String
        :param movie_id:         String
        :return:                 pyspark.sql.DataFrame"""
        if movie_name is None and movie_id is None:
            raise AssertionError("You need to give movie_name or movie_id")
        if movie_id is None:
            movie_id = (
                self.df.filter(self.df.tytul == movie_name).select("id").collect()[0][0]
            )

        self.trained_df = cos_sim_and_iou_for_row(df=self.df, movie_id=movie_id)
        return self.trained_df

    def predict(self, a_param: float = 0.5, sort_results=False) -> DataFrame:
        """This function returns a DataFrame that contains finally similarity for the given movie_id in scale form 0 to 1.

        :param sort_results:     boolean
        :param a_param:          float
        :return:                 pyspark.sql.DataFrame"""

        if a_param < 0:
            raise AttributeError("a_param can not be negative")

        add_udf = f.udf(lambda x, y: a_param * x + (1 - a_param) * y, FloatType())

        self.trained_df = self.trained_df.withColumn(
            "prediction",
            add_udf(self.trained_df["cos_similarity"], self.trained_df["IOU"]),
        )

        if sort_results:
            self.trained_df = self.trained_df.sort(desc("prediction"))

        return self.trained_df
