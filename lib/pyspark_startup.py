import findspark
from pyspark.sql import SparkSession, DataFrame

spark_params = {
    "spark.executor.memory" : "4g",
    "spark.driver.memory": "4g",
    "spark.memory.fraction": "0.9"}

def init() -> SparkSession:
    findspark.init()
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    
    for param, value in spark_params.items():
        spark.conf.set(param, value)

    return spark

def load(spark: SparkSession) -> DataFrame:
    title_ratings = spark.read.csv("title.ratings.tsv.gz", sep='\t', header=True)
    title_principals = spark.read.csv("title.principals.tsv.gz", sep='\t',header=True)
    title_episode = spark.read.csv("title.episode.tsv.gz", sep='\t', header=True)
    title_crew = spark.read.csv("title.crew.tsv.gz", sep='\t', header=True)
    title_basics = spark.read.csv("title.basics.tsv.gz", sep='\t', header=True)
    title_akas = spark.read.csv("title.akas.tsv.gz", sep='\t', header=True)
    name_basics = spark.read.csv("name.basics.tsv.gz", sep='\t', header=True)

    temp_akas = title_akas.filter(title_akas.isOriginalTitle == 1)
    temp_akas = temp_akas.select(["titleId", "region", "language"]).distinct()
    temp_akas = temp_akas.withColumnRenamed("titleId", "tconst")

    to_print = ["title_basics", "title_ratings", "title_principals", 
                "title_episode", "name_basics", "temp_akas"]

    for p in to_print:
        #TODO rozważyć przejście na logging (lib do robienia logów) zamiast printów
        print(f"Dimension {p}: ({eval(p).count()}, {len(eval(p).columns)})")

    data = title_basics.join(title_ratings, how="left", on="tconst")
    print(f"\nJoined title_principals to title_basics\n" + 
        f"Dimension: ({data.count()}, {len(data.columns)})")

    data = data.join(title_principals, how="left", on="tconst")
    print(f"Joined title_principals\n" + 
        f"Dimension: ({data.count()}, {len(data.columns)})")

    data = data.join(title_episode, how="left", on="tconst")
    print(f"Joined title_episode\n" + 
        f"Dimension: ({data.count()}, {len(data.columns)})")

    data = data.join(name_basics, how="left", on="nconst")
    print(f"Joined name_basics\n" + 
        f"Dimension: ({data.count()}, {len(data.columns)})")

    data = data.join(temp_akas, how="left", on="tconst")
    print(f"Joined temp_akas\n" + 
        f"Dimension: ({data.count()}, {len(data.columns)})")

    return data
