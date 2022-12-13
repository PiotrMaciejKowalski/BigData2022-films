#TODO wstawić później tę funkcję do pliku feature_creators
import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from typing import Union, List, Optional

def people_film_merge_columns(df: DataFrame, film_id: str, add_column: Optional[bool] = False) -> Union[DataFrame,List[str]]:
  
  assert df.filter(df.id == film_id).rdd.isEmpty() == False

  df_film = df.filter(df.id == film_id)

  people_column_names = ["{}".format(i+1) for i in range(10)]

  columns_to_merge = [f.col(column_name) for column_name in people_column_names]

  if add_column == False:
    list_people_merge = df_film.withColumn("ludzie_filmu", f.array(columns_to_merge)).select("ludzie_filmu").collect()
    list_people_merge = [people for people in list_people_merge[0][0] if people is not None]
    return list_people_merge

  else:
    df_people_merge =  df_film.withColumn("ludzie_filmu", f.array(columns_to_merge))
    for names in people_column_names:
      df_people_merge = df_people_merge.drop(names)
    return df_people_merge
