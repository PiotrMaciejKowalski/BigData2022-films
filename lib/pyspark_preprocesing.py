from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import DataFrame
from typing import List


def one_hot_encoding(df: DataFrame, columns: List[str]) -> DataFrame:
    out_cols = [x + '_ohe' for x in columns]
    out_num = [x + '_num' for x in columns]

    df_num = StringIndexer(inputCols=columns,
                           outputCols=out_num).fit(df).transform(df)

    df_ohe = OneHotEncoder(inputCols=out_num,
                           outputCols=out_cols).fit(df_num).transform(df_num)
    df_ohe = df_ohe.drop(*columns, *out_num)

    return df_ohe
