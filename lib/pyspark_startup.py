import findspark

findspark.init()

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import countDistinct, first


def init() -> SparkSession:
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    return spark


def load(spark: SparkSession) -> DataFrame:
    title_basics = spark.read.csv("title.basics.tsv.gz", sep="\t", header=True).drop(
        "originalTitle"
    )
    title_seasons = (
        spark.read.csv("title.episode.tsv.gz", sep="\t", header=True)[
            ["parentTconst", "seasonNumber"]
        ]
        .replace(to_replace="\\N", value=None)
        .groupBy("parentTconst")
        .agg(countDistinct("seasonNumber"))
    )
    title_episode = (
        spark.read.csv("title.episode.tsv.gz", sep="\t", header=True)[
            ["parentTconst", "episodeNumber"]
        ]
        .replace(to_replace="\\N", value=None)
        .groupby("parentTconst")
        .count()
    )
    title_ratings = spark.read.csv("title.ratings.tsv.gz", sep="\t", header=True)
    title_principals = (
        spark.read.csv("title.principals.tsv.gz", sep="\t", header=True)
        .select("tconst", "ordering", "nconst")
        .groupBy("tconst")
        .pivot("ordering")
        .agg(first("nconst"))
    )

    data = (
        title_basics.join(
            title_seasons, title_basics.tconst == title_seasons.parentTconst, how="left"
        )
        .join(
            title_episode, title_basics.tconst == title_episode.parentTconst, how="left"
        )
        .join(title_ratings, ["tconst"], how="left")
        .drop("parentTconst")
        .join(title_principals, ["tconst"], how="left")
        .toDF(
            "id",
            "rodzaj_produkcji",
            "tytul",
            "czy_dla_doroslych",
            "rok_wydania_produkcji",
            "rok_zakonczenia_produkcji",
            "dlugosc_produkcji_w_min",
            "gatunek",
            "liczba_sezonow",
            "liczba_wszystkich_odcinkow",
            "ocena",
            "liczba_glosow",
            "1",
            "10",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        )
    )

    return data
