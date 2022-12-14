import findspark

findspark.init()

import pytest
import pyspark

from pyspark.sql import SparkSession, DataFrame

from lib.film_people_list import people_film_merge_columns
from lib.pyspark_startup import init

def test_people_film_merge_column():

  spark = init()
  result_df = spark.createDataFrame(
      [
          ('tt0111161', 'nm0000209', 'nm0000151', 'nm0348409', 'nm0006669', 'nm0001104', 'nm0000175', 'nm0555550', 'nm0002353', 'nm0005683', 'nm0290358'),
      ],  
      "id string, `1` string, `2` string, `3` string, `4` string, `5` string, `6` string, `7` string, `8` string, `9` string, `10` string"
    )

  expect_result = {'nm0000151', 'nm0348409', 'nm0006669', 'nm0001104', 'nm0000175', 'nm0555550', 'nm0002353', 'nm0005683', 'nm0290358','nm0000209'}

  result = set(people_film_merge_columns(result_df,'tt0111161'))
  assert result == expect_result
