from typing import List
from pyspark.sql import DataFrame
from pyspark.ml.feature import VectorAssembler

def merge_dense_vectors(
    df: DataFrame,
    columns: List[str],
    ) -> DataFrame:
    """Funkcja zwraca sparkowy DataFrame, w którym podane w parametrach kolumny zostają skonwertowane na nową kolumnę pod nazwą "features", 
    która jest postaci DenseVector, a reszta kolumn w podanym w parametrze DataFrame pozostaje bez zmian.
    
    :param df: pyspark.sql.DataFrame
    :param columns: lista kolumn do skonwertowania
    :return: pyspark.sql.DataFrame"""

    VecAssembler = VectorAssembler(inputCols=columns, outputCol="features").transform(df)
    VecAssembler = VecAssembler.drop(*columns)


    return VecAssembler
