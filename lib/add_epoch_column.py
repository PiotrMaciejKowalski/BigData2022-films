from pyspark.sql.functions import col, when
from pyspark.sql.dataframe import DataFrame

def add_epoch_column(df: DataFrame) -> DataFrame:
  #TODO dodać asercje sprawdzającą, czy startYear jest integerem
  periods = [1901,1918,1926,1939,1954,1970,1985,1994,2009]
  df_no_N = df.filter(df.startYear != "\\N")

  df_periods = df_no_N.withColumn('period',
                             when(col('startYear') <= periods[0], "1")
                             .when(col('startYear') <= periods[1], "2")
                             .when(col('startYear') <= periods[2], "3")
                             .when(col('startYear') <= periods[3], "4")
                             .when(col('startYear') <= periods[4], "5")
                             .when(col('startYear') <= periods[5], "6")
                             .when(col('startYear') <= periods[6], "7")
                             .when(col('startYear') <= periods[7], "8")
                             .when(col('startYear') <= periods[8], "9")
                             .otherwise("10"))
  return df_periods
