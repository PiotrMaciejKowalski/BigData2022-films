from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import DataFrame
from typing import List, Literal


def one_hot_encoding(
    df: DataFrame,
    columns: List[str],
    on_exception: Literal["skip", "error", "keep"] = "skip",
    drop_cols: bool = True,
) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame w którym wartości w wybranych kolumnach
    zostały zamienione na takie z kodowaniem zero-jednykowym w trybie 'sparse'.

    Przykład: (3,[0],[1.0]) -> (1.0, 0, 0)
    3 - długość wektora,
    [1.0] - jaka liczb znajduje się w wektorze poza zerami,
    [0] - pozycja na której znajduje się liczba 1.0

    :param df:              pyspark.sql.DataFrame
    :param columns:         lista kolumn do zakodowania
    :param on_exception:    obsługa wyjątków w setHandleInvalid()
    :param drop_cols:       usunięcie orginalnych kolumn
    :return:                pyspark.sql.DataFrame"""

    out_cols = [x + "_ohe" for x in columns]
    out_num = [x + "_num" for x in columns]

    assert columns in df.columns
    assert out_cols not in df.columns
    assert out_num not in df.columns

    df_num = (
        StringIndexer(inputCols=columns, outputCols=out_num)
        .setHandleInvalid(on_exception)
        .fit(df)
        .transform(df)
    )

    df_ohe = (
        OneHotEncoder(inputCols=out_num, outputCols=out_cols)
        .fit(df_num)
        .transform(df_num)
    )

    df_ohe = df_ohe.drop(*out_num)

    if drop_cols:
        df_ohe = df_ohe.drop(*columns)

    return df_ohe
