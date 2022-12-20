from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import DataFrame
from typing import List, Literal
from pyspark_preprocesing import one_hot_encoding


def similarity_matrix(
    df: DataFrame,

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