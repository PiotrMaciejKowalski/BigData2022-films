import pandas as pd
from pyspark.sql.types import Row
from pyspark.sql import DataFrame


def ranking_function(row1: Row, row2: Row) -> int:
    """Funkcja rankująca zwraca liczbę odpowiadającą podobieństwu dwóch filmów.
    Punkty są przyznawane jeśli oba filmy posiadają te same wartości
    w odpowiednich kolumnach.

    :param row1:            pyspark.sql.types.Row
    :param row2:            pyspark.sql.types.Row
    """
    cols = [
        "dlugosc_produkcji_w_min",
        "liczba_sezonow",
        "liczba_wszystkich_odcinkow",
        "features",
        "ludzie_filmu"
    ]

    assert all(x in row1.__fields__ for x in cols)
    assert all(x in row2.__fields__ for x in cols)

    score = 0

    if abs(row1["dlugosc_produkcji_w_min"] - row2["dlugosc_produkcji_w_min"]) < 15:
        score += 1

    if (row1["liczba_sezonow"] == row2["liczba_sezonow"] == 1) or (
        abs(row1["liczba_sezonow"] - row2["liczba_sezonow"]) < 2
    ):
        score += 1

    if (
        row1["liczba_wszystkich_odcinkow"] == row2["liczba_wszystkich_odcinkow"] == 1
    ) or (
        abs(row1["liczba_wszystkich_odcinkow"] - row2["liczba_wszystkich_odcinkow"]) < 6
    ):
        score += 1

    score += row1["features"].dot(row2["features"])

    score += len(set(row1["ludzie_filmu"]) & set(row2["ludzie_filmu"]))

    return score


def ranking_list(df: DataFrame, movie_id: str) -> pd.DataFrame:
    """Funkcja zwaraca Pandasowy Data Frame z kolumną id wszystkich filmów oraz
    kolumną score z liczbą odpowiadająca podobieństwu do filmu
    o indeksie 'movie_id'.

    :param df:              pyspark.sql.DataFrame
    :param movie_id:        id filmu dla którego tworzymy ranking filmów podobnych
    """

    assert "id" in df.columns

    movie_row = df[df.id == movie_id].collect()[0]
    rank_result = df.rdd.map(
        lambda row: [row["id"], ranking_function(row, movie_row)]
    ).collect()

    return pd.DataFrame(rank_result, columns=["id", "score"])
