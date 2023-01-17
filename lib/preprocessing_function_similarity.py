from pyspark.sql.functions import monotonically_increasing_id, row_number
from pyspark.sql.window import Window
from typing import List
from pyspark.sql import DataFrame
from pyspark.ml.feature import VectorAssembler

def DenseVectorToSimilarity(
    df: DataFrame,
    columns: List[str],
    ) -> DataFrame:
    "Funkcja, która zamienia wybrane kolumny na gotowe do wrzucenia do Similarity, a resztę pozostawia bez zmian"

    df_similarity = df.select(columns)
    df_rest = df.drop(*columns)
    vecAssembler2 =  VectorAssembler(inputCols=df_similarity.columns, outputCol="features", handleInvalid="keep")
    vecAssembler2 = vecAssembler2.transform(df_similarity)
    df1= vecAssembler2.select(["features"])

    df1=df1.withColumn('row_index', row_number().over(Window.orderBy(monotonically_increasing_id())))
    df_rest=df_rest.withColumn('row_index', row_number().over(Window.orderBy(monotonically_increasing_id())))
    df_to_similarity = df1.join(df_rest, on=["row_index"]).drop("row_index")


    return df_to_similarity
