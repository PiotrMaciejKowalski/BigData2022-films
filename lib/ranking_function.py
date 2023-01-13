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
        "czy_dla_doroslych",
        "rok_wydania_produkcji",
        "rok_zakonczenia_produkcji",
        "dlugosc_produkcji_w_min",
        "liczba_sezonow",
        "liczba_wszystkich_odcinkow",
        "rodzaj_produkcji_ohe",
        "epoka_ohe",
        "gatunek_vec",
        "ludzie_filmu",
    ]

    assert all(x in row1.__fields__ for x in cols)
    assert all(x in row2.__fields__ for x in cols)

    score = 0

    if row1["czy_dla_doroslych"] == row2["czy_dla_doroslych"]:
        score += 1

    if abs(row1["rok_wydania_produkcji"] - row2["rok_wydania_produkcji"]) < 10:
        score += 1

    if abs(row1["rok_zakonczenia_produkcji"] - row2["rok_zakonczenia_produkcji"]) < 10:
        score += 1

    if abs(row1["dlugosc_produkcji_w_min"] - row2["dlugosc_produkcji_w_min"]) < 15:
        score += 1

    if row1["liczba_sezonow"] == row2["liczba_sezonow"]:
        score += 1

    if row1["liczba_wszystkich_odcinkow"] == row2["liczba_wszystkich_odcinkow"]:
        score += 1

    if row1["rodzaj_produkcji_ohe"] == row2["rodzaj_produkcji_ohe"]:
        score += 1

    if row1["epoka_ohe"] == row2["epoka_ohe"]:
        score += 1

    score += row1["gatunek_vec"].dot(row2["gatunek_vec"])

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
