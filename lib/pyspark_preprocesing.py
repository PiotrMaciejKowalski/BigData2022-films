from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import DataFrame, SparkSession
from typing import List, Literal


def one_hot_encoding(
    df: DataFrame,
    columns: List[str],
    on_exception: Literal["skip", "error", "keep"] = "skip",
    drop_cols: bool = True,
) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame w którym wartości w wybranych kolumnach
    zostały zamienione na takie z kodowaniem zero-jednykowym w trybie 'sparse'
    w nowych kolumnach z nazwami z dopiskiem '_ohe'. Na chwilę tworzone są też
    pomocnicze kolumny o nazwach z dopiskiem '_num'. Wartości w dodanych
    kolumnach są klasy pyspark.ml.linalg.SparseVector.

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

    assert all(x in df.columns for x in columns)
    assert all(x not in df.columns for x in out_cols)
    assert all(x not in df.columns for x in out_num)

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


def normalize_by_group(
    spark: SparkSession,
    df: DataFrame,
    group_by: List[str],
    normalize: List[str],
    drop_cols: bool = True,
) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame ze znormalizowanymi kolumnami według grup.
    Dodane kolumny posiadają przedrostki 'norm_'. Normalizację dokonujemy przez odjęcie
    średniej i podzielenie przez odchylenie standardowe obliczane wewnątrz każdej grupy.

    :param spark:           pyspark.sql.SparkSession
    :param df:              pyspark.sql.DataFrame
    :param group_by:        lista kolumn według których dokonamy grupowania
    :param normalize:       lista kolumn z wartościami do znormalizowania
    :param drop_cols:       usunięcie oryginalnych kolumn
    :return:                pyspark.sql.DataFrame"""

    assert all(x in df.columns for x in group_by)
    assert all(x in df.columns for x in normalize)
    assert all(x not in df.columns for x in ["avg_" + x for x in normalize])
    assert all(x not in df.columns for x in ["stdev_" + x for x in normalize])

    df.createOrReplaceTempView("tmp_view")
    select_col = group_by + [
        "stddev(" + x + ") as stdev_" + x + ", avg(" + x + ") as avg_" + x
        for x in normalize
    ]
    sql_str = (
        "select "
        + ", ".join(select_col)
        + " from tmp_view "
        + "group by "
        + ", ".join(group_by)
    )
    tmp_df = spark.sql(sql_str)

    tmp_df = df.join(tmp_df, on=group_by, how="left")
    tmp_df.createOrReplaceTempView("tmp_view2")

    norm_cols = [
        "(" + x + " - avg_" + x + ") / stdev_" + x + " as norm_" + x for x in normalize
    ]

    sql_str = (
        "select "
        + ", ".join(df.columns)
        + ", "
        + ", ".join(norm_cols)
        + " from tmp_view2"
    )
    df_out = spark.sql(sql_str)

    if drop_cols:
        df_out = df_out.drop(*normalize)

    return df_out
