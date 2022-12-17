from pyspark.sql.functions import col, when
from pyspark.sql import DataFrame
from functools import reduce
from typing import List, Optional

DEAFULT_PERIODS = [1901,1918,1926,1939,1954,1970,1985,1994,2009]

def add_epoch_column(df: DataFrame, periods: Optional[List[int]] = None) -> DataFrame:

  assert df.filter(df.rok_wydania_produkcji == "\\N").count() == 0
  assert dict(df.dtypes)["rok_wydania_produkcji"] == "int"

  if periods == None:
    periods = DEAFULT_PERIODS

  assert len(periods) > 0

  periods_count = len(periods)

  formulas = [

    (col('rok_wydania_produkcji') <= period, str(index+1))

    for period, index
    in zip(periods, range(periods_count))

    ]

  otherwise_value = len(periods) + 1  
  condition = when( *(formulas[0]))

  for formula in formulas[1:]:
    condition = condition.when(*formula)

  condition = condition.otherwise(otherwise_value)

  df_periods = df.withColumn('epoka',condition)  

  return df_periods
