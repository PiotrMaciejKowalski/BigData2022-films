import findspark

findspark.init()

import pytest
import pyspark

from pyspark.sql import SparkSession, DataFrame

from lib.add_epoch_column import add_epoch_column

from pyspark_test import assert_pyspark_df_equal

def test_add_epoch_column():

  spark = SparkSession.builder.master("local[*]").getOrCreate()
  df = spark.createDataFrame(
      [
          (1, 1900),
          (2, 1917),
          (3, 1925),
          (4, 1938),
          (5, 1953),
          (6, 1969),
          (7, 1984),
          (8, 1993),
          (9, 2008),
          (10, 2022)
      ],  
      "id int, startYear int",
  )

  expect_df = spark.createDataFrame(
      [
          (1, 1900, "1"),
          (2, 1917, "2"),
          (3, 1925, "3"),
          (4, 1938, "4"),
          (5, 1953, "5"),
          (6, 1969, "6"),
          (7, 1984, "7"),
          (8, 1993, "8"),
          (9, 2008, "9"),
          (10, 2022, "10")
      ],  
      "id int, startYear int, period string",
  )

  result = add_epoch_column(df)

  print(result.show())
  assert_pyspark_df_equal(result, expect_df)