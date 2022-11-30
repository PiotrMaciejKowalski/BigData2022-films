import pandas as pd

def _map_to_pandas(rdds):
    """ Needs to be here due to pickling issues """
    return [pd.DataFrame(list(rdds))]

def to_Pandas(df, n_partitions=None):
    """
    Zwraca wartość `df` jako lokalną tabelę `pandas.DataFrame` w przyspieszony oraz stabliniejszy sposób,
    dzięki podzieleniu DataFrame-u na `n` części i transofrmowaniu ich w mniejszych partiach.
    Uwaga, `n_partitions` oznacza liczbę części na jaką podzielimy nasz zadany `df`.
    
    Przykład: new_df = to_Pandas(old_df, 10), gdzie old_df.shape == (5, 10 000 000)

    :param df:              pyspark.sql.DataFrame
    :param n_partitions:    int or None
    :return:                pandas.DataFrame
    """
    if n_partitions is not None: df = df.repartition(n_partitions)
    df_pand = df.rdd.mapPartitions(_map_to_pandas).collect()
    df_pand = pd.concat(df_pand)
    df_pand.columns = df.columns
    return df_pand