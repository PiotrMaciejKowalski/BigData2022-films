import findspark

findspark.init()

import pytest
import pyspark

from pyspark.sql import SparkSession, DataFrame
from pyspark_test import assert_pyspark_df_equal

from lib.add_epoch_column import add_epoch_column

def test_add_epoch_column():

  spark = SparkSession.builder.master("local[*]").getOrCreate()
  df = spark.createDataFrame(
      [
          (1, 1900),
          (2, 1917),
          (3, 1920),
          (4, 1938),
          (5, 1953),
          (6, 1960),
          (7, 1984),
          (8, 1993),
          (9, 2008),
          (10, 2022)
      ],  
      "id int, rok_wydania_produkcji int",
  )

  expect_df = spark.createDataFrame(
      [
          (1, 1900, "1"),
          (2, 1917, "2"),
          (3, 1920, "3"),
          (4, 1938, "4"),
          (5, 1953, "5"),
          (6, 1960, "6"),
          (7, 1984, "7"),
          (8, 1993, "8"),
          (9, 2008, "9"),
          (10, 2022, "10")
      ],  
      "id int, rok_wydania_produkcji int, period string",
  )

  result = add_epoch_column(df)
  assert_pyspark_df_equal(result, expect_df)
