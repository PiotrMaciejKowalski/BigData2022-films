from pyspark.ml.feature import StringIndexer, OneHotEncoder, CountVectorizer
from pyspark.sql.functions import split, col, when
from pyspark.sql import DataFrame, SparkSession
from typing import List, Literal


def one_hot_encoding(
    df: DataFrame,
    columns: List[str],
    on_exception: Literal["skip", "error", "keep"] = "skip",
    drop_cols: bool = True,
) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame w którym wartości w wybranych kolumnach
    zostały zamienione na takie z kodowaniem zero-jedynkowym w trybie 'sparse'
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
    :param drop_cols:       usunięcie oryginalnych kolumn
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
    assert all(x not in df.columns for x in [f"avg_{x}" for x in normalize])
    assert all(x not in df.columns for x in [f"stdev_{x}" for x in normalize])

    df.createOrReplaceTempView("tmp_view")
    select_col = group_by + [
        f"stddev({x}) as stdev_{x}, avg({x}) as avg_{x}" for x in normalize
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

    norm_cols = [f"({x} - avg_{x}) / stdev_{x} as norm_{x}" for x in normalize]

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


def count_vectorizer(df: DataFrame, column: str, drop_cols: bool = True) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame w którym wartości w wybranej kolumnie
    zostały zamienione na wektory. Kolumna powinna zawierać zmienne typu
    string z cechami oddzielonymi przecinkami. Tymczasowo tworzona jest kolumna
    o nazwie z dopiskiem '_temp' a docelowa kolumna posiada dopisek '_vec'.
    Wartości w dodanych kolumnach są klasy pyspark.ml.linalg.SparseVector.

    Przykład:
    Możliwe wartości: [Documentary, Short, Comedy]
    'Documentary,Short' -> (3, [0,1], [1.0,1.0])
    'Comedy,Short'      -> (3, [1,2], [1.0,1.0])
    'Short'             -> (3, [1], [1.0])

    :param df:              pyspark.sql.DataFrame
    :param column:          nazwa kolumny do zakodowania
    :param drop_cols:       usunięcie oryginalnych kolumn
    """

    assert column in df.columns
    assert column + "_temp" not in df.columns
    assert column + "_vec" not in df.columns

    df_arr = df.select(split(col(column), ",").alias(column + "_temp"), df["*"])
    result = (
        CountVectorizer(inputCol=column + "_temp", outputCol=column + "_vec")
        .fit(df_arr)
        .transform(df_arr)
        .drop(column + "_temp")
    )

    if drop_cols:
        result = result.drop(column)

    return result


def convert_types(df: DataFrame, columns: List[str], type: str) -> DataFrame:
    """Funkcja konwertuje kolumny na określony typ danych.

    Args:
        df (DataFrame):         sparkowy DataFrame
        columns (List[str]):    lista kolumn do przekonwerotowania
        type (str):             typ, na który chcemy przekonwertować dane
    Returns:
        df: sparkowy DataFrame ze zmienionymi typami kolumn
    """
    assert all(x in df.columns for x in columns)

    for c in columns:
        df = df.withColumn(c, col(c).cast(type).alias(c))

    return df


def value_overwrite(
    df: DataFrame,
    columns: List[str],
    values: list,
    category_col: str,
    category: List[str],
) -> DataFrame:
    """Funkcja nadpisuje wskazane kolumny poprzez wskazane wartości (lub kolumny)
    dla okreslonych kategorii filmowych.

    Args:
        df (DataFrame):         sparkowy DataFrame
        columns (List[str]):    lista kolumn do nadpisania
        values (str):           odpowiednio wartości (lub kolumny) jakimi chcemy nadpisać
        category_col(str):      kolumna, według której będziemy odfiltrowywać kategorie
        category (List[str]):   kategorie dla jakich mamy nadpisywać wartości

    Returns:
        df: sparkowy DataFrame z nadpisanymi wartościami
    """
    assert all(x in df.columns for x in columns)
    assert category_col in df.columns
    assert len(columns) == len(values)

    for col, value in zip(columns, values):
        if isinstance(value, str) and (value in df.columns):
            df = df.withColumn(
                col,
                when(df[category_col].isin(category), df[value]).otherwise(df[col]),
            )
        else:
            df = df.withColumn(
                col,
                when(df[category_col].isin(category), value).otherwise(df[col]),
            )
    return df
