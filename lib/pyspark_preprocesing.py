from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import DataFrame
from typing import List


def one_hot_encoding(
    df: DataFrame, columns: List[str], exception: str = "skip"
) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame w którym wartości w wybranych kolumnach
    zostały zamienione na takie z kodowaniem zero-jednykowym w trybie 'sparse'.
    Przykład: (3,[0],[1.0]) -> (1.0, 0, 0)
    3 - długość wektora,
    [1.0] - jaka liczb znajduje się w wektorze poza zerami,
    [0] - pozycja na której znajduje się liczba 1.0"""

    out_cols = [x + "_ohe" for x in columns]
    out_num = [x + "_num" for x in columns]

    df_num = (
        StringIndexer(inputCols=columns, outputCols=out_num)
        .setHandleInvalid(exception)
        .fit(df)
        .transform(df)
    )

    df_ohe = (
        OneHotEncoder(inputCols=out_num, outputCols=out_cols)
        .fit(df_num)
        .transform(df_num)
    )
    df_ohe = df_ohe.drop(*columns, *out_num)

    return df_ohe
