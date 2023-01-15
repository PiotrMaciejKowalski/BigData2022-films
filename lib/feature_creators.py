from pyspark.sql.functions import col, when
from pyspark.sql import DataFrame
from functools import reduce
from typing import List, Optional

DEAFULT_PERIODS = [1901, 1918, 1926, 1939, 1954, 1970, 1985, 1994, 2009]


def add_epoch_column(
    df: DataFrame,
    periods: Optional[List[int]] = None,
    add_end_year_epoch: Optional[bool] = False,
    drop_rok_wydania_produkcji: Optional[bool] = False,
    drop_rok_zakonczenia_produkcji: Optional[bool] = False,
) -> DataFrame:
  
    assert df.filter(df.rok_wydania_produkcji == "\\N").count() == 0
    assert dict(df.dtypes)["rok_wydania_produkcji"] == "int"

    if add_end_year_epoch == True:
        assert dict(df.dtypes)["rok_zakonczenia_produkcji"] == "int"
    if periods == None:
        periods = DEAFULT_PERIODS
    assert len(periods) > 0

    periods_count = len(periods)

    formulas_start_year = [
        (col("rok_wydania_produkcji") <= period, str(index + 1))
        for period, index in zip(periods, range(periods_count))
    ]

    otherwise_value = len(periods) + 1
    condition = when(*(formulas_start_year[0]))

    for formula in formulas_start_year[1:]:
        condition = condition.when(*formula)
    condition = condition.otherwise(otherwise_value)

    df_epoch = df.withColumn("epoka_rok_wydania_produkcji", condition)

    if add_end_year_epoch == True:
        formulas_end_year = [
            (col("rok_zakonczenia_produkcji") <= period, str(index + 1))
            for period, index in zip(periods, range(periods_count))
        ]

        otherwise_value = len(periods) + 1
        condition = when(*(formulas_end_year[0]))

        for formula in formulas_end_year[1:]:
            condition = condition.when(*formula)
        condition = condition.otherwise(otherwise_value)

        df_epoch = df_epoch.withColumn("epoka_rok_zakonczenia_produkcji", condition)
        
    if drop_rok_wydania_produkcji == True and drop_rok_zakonczenia_produkcji == True:
        return df_epoch.drop("rok_wydania_produkcji", "rok_zakonczenia_produkcji")
      
    if drop_rok_wydania_produkcji == True:
        return df_epoch.drop("rok_wydania_produkcji")
      
    if drop_rok_zakonczenia_produkcji == True:
        return df_epoch.drop("rok_zakonczenia_produkcji")
      
    return df_epoch
