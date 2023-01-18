import findspark
import pandas as pd

findspark.init()

from pyspark.ml.linalg import SparseVector
from pyspark.sql.types import Row
from pandas.testing import assert_frame_equal
from lib.pyspark_startup import init
from lib.ranking_function import ranking_function, ranking_list


def test_ranking_function():
    row1 = Row(
        id="tt0000001",
        dlugosc_produkcji_w_min=1,
        liczba_sezonow=1.0,
        liczba_wszystkich_odcinkow=1.0,
        features=SparseVector(45, {0: 1.0, 2: 1.0}),
        ludzie_filmu=[
            "nm1588970",
            "nm0005690",
            "nm0374658",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
    )

    row2 = Row(
        id="tt0000003",
        dlugosc_produkcji_w_min=4,
        liczba_sezonow=1.0,
        liczba_wszystkich_odcinkow=1.0,
        features=SparseVector(45, {0: 1.0, 3: 1.0, 5: 1.0, 6: 1.0}),
        ludzie_filmu=[
            "nm0721526",
            "nm1770680",
            "nm1335271",
            "nm5442200",
            None,
            None,
            None,
            None,
            None,
            None,
        ],
    )

    row3 = Row(
        dlugosc_produkcji_w_min=4,
        liczba_sezonow=1.0,
        liczba_wszystkich_odcinkow=10,
        gatunek_vec=SparseVector(45, {3: 1.0, 6: 1.0}),
        ludzie_filmu=["nm0721526", "nm1770680", "nm1335271", "nm5442200"],
    )

    assert ranking_function(row1, row2) == 5.0
    assert ranking_function(row1, row1) == 9.0
    assert ranking_function(row1, row3) == 2.0
    assert ranking_function(row1, row3) == ranking_function(row3, row1)


def test_ranking_list():
    spark = init()

    test_df = spark.createDataFrame(
        [
            (
                "tt0000480",
                "Le coffre enchanté",
                "0",
                3,
                1.0,
                1.0,
                SparseVector(7, {0: 1.0}),
                SparseVector(9, {7: 1.0}),
                SparseVector(28, {0: 1.0, 14: 1.0}),
                ["nm0617588", None, None, None, None, None, None, None, None, None],
            ),
            (
                "tt0029294",
                "Natación",
                "0",
                11,
                1.0,
                1.0,
                SparseVector(7, {0: 1.0}),
                SparseVector(9, {6: 1.0}),
                SparseVector(28, {0: 1.0, 2: 1.0, 20: 1.0}),
                [
                    "nm0034042",
                    "nm0317695",
                    "nm0883411",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ),
            (
                "tt0000000",
                "testfilm",
                "1",
                7,
                2.0,
                1.0,
                SparseVector(7, {0: 1.0}),
                SparseVector(9, {8: 1.0}),
                SparseVector(28, {}),
                ["nm0034042", "ddddbf", "fafasfasf"],
            ),
        ],
        [
            "id",
            "tytul",
            "czy_dla_doroslych",
            "dlugosc_produkcji_w_min",
            "liczba_sezonow",
            "liczba_wszystkich_odcinkow",
            "rodzaj_produkcji_ohe",
            "epoka_ohe",
            "gatunek_vec",
            "ludzie_filmu",
        ],
    )

    result1 = ranking_list(test_df, "tt0000480")
    result2 = ranking_list(test_df, "tt0000000")

    exp_result1 = pd.DataFrame(
        [["tt0000480", 7.0], ["tt0029294", 5.0], ["tt0000000", 3.0]],
        columns=["id", "score"],
    )

    exp_result2 = pd.DataFrame(
        [["tt0000480", 3.0], ["tt0029294", 4.0], ["tt0000000", 6.0]],
        columns=["id", "score"],
    )

    assert_frame_equal(result1, exp_result1)
    assert_frame_equal(result2, exp_result2)
