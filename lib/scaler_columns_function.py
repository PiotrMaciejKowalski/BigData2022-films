from pyspark.ml import Pipeline
from pyspark.sql import functions as f
from pyspark.ml.feature import VectorAssembler
from typing import List
from pyspark.sql import DataFrame
from pyspark.ml.feature import MinMaxScaler


def scaler_columns(
    df: DataFrame,
    columns: List[str],
    drop_cols: bool = False,
) -> DataFrame:

    """Funkcja zwraca sparkowy DataFrame w którym podane w parametrach kolumny zostają przeskalowane metodą MinMaxScaler i zamienione na vector type, a
    do nazwy przeskalowanej kolumny dodany jest przedrostek _scaled.

    :param df: pyspark.sql.DataFrame
    :param columns: lista kolumn do znormalizowania
    :param drop_cols: usunięcie oryginalnych kolumn
    :return: pyspark.sql.DataFrame
    """

    assemblers = [
        VectorAssembler(inputCols=[col], outputCol=col + "_vec") for col in columns
    ]
    scalers = [
        MinMaxScaler(inputCol=col + "_vec", outputCol=col + "_scaled")
        for col in columns
    ]
    pipeline = Pipeline(stages=assemblers + scalers)
    scaledData = pipeline.fit(df).transform(df)
    if drop_cols:
        scaledData = scaledData.drop(*columns)
    vectors_columns = [x + "_vec" for x in columns]
    scaledData = scaledData.drop(*vectors_columns)

    return scaledData
