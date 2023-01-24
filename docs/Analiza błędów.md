## Analiza błędów

W celu analizy możliwych błędów porównywałam wyniki 
ranking_list oraz prediction stworzonego na podstawie cosine 
similarity i intersection over union.
Uruchamiałam powyższe funkcje dla wszystkich
danych (ponad 1 200 000 filmów). Do testów
wybierałam popularne filmy, aby otrzymane
wyniki można było łatwo zweryfikować i porównać
z naszą intuicją.

Pierwszym napotkanym problemem jest mała rozróżnialność
wartości prediction (dużo wartości powtarzających się). 

```angular2html
Top 10 najbardziej podobnych filmów do Fight Club:
+---------+------------------+--------------+-----------+----------+
|       id|             tytul|cos_similarity|        IOU|prediction|
+---------+------------------+--------------+-----------+----------+
|tt0137523|        Fight Club|           1.0|        1.0|       1.0|
|tt0114782|  Under the Bridge|           1.0|0.055555556| 0.5277778|
|tt0449467|             Babel|           1.0| 0.05263158| 0.5263158|
|tt0307901|         25th Hour|           1.0| 0.05263158| 0.5263158|
|tt0332452|              Troy|           1.0| 0.05263158| 0.5263158|
|tt0115468|          Adosados|           1.0|        0.0|       0.5|
|tt0114642|El techo del mundo|           1.0|        0.0|       0.5|
|tt0114612| The Night Is Dark|           1.0|        0.0|       0.5|
|tt0116720|   Joyeux Calvaire|           1.0|        0.0|       0.5|
|tt0112941|          Eldorado|           1.0|        0.0|       0.5|
+---------+------------------+--------------+-----------+----------+
only showing top 10 rows
```

W związku z powyższym np. dla filmu Fight Club 
już w pierwszej 10 najbardziej podobnych filmów
znajdują się takie, które trafiają tam losowo. Nasz model 
dla dużej ilości filmów ocenia podobieństwo na 0.5 (ponieważ kolumna IOU zawiera 0,
a cos_sim 1), natomiast kolejność ich wyświetlenia w tabeli z predykcjami similarity 
jest dowolna. Zatem przy kilkukrotnym uruchomieniu naszej predykcji
5 z 10 filmów się zmienia (pomimo stałych wartości predykcji w top 10).
Pomysł: odrzucić filmy, które w jednej z kolumn mają 0.


Kolejnym problemem jest niezgodność z intuicją w niektórych
przykładach. Dla filmu "Toy Story" najbardziej podobnych filmem
jest Toy Story 2, natomiast kolejne części tej serii (3 i 4) znajdują
się na miejscach 10+. 

```angular2html
Top 10 najbardziej podobnych filmów do Toy Story:
+---------+--------------------+--------------+----------+----------+
|       id|               tytul|cos_similarity|       IOU|prediction|
+---------+--------------------+--------------+----------+----------+
|tt0114709|           Toy Story|           1.0|       1.0|       1.0|
|tt0120363|         Toy Story 2|           1.0|0.33333334| 0.6666667|
|tt0120623|        A Bug's Life|           1.0| 0.1764706| 0.5882353|
|tt0317219|                Cars|           1.0|0.11111111| 0.5555556|
|tt0338348|   The Polar Express|           1.0|0.05263158| 0.5263158|
|tt0429589|       The Ant Bully|           1.0|0.05263158| 0.5263158|
|tt1049413|                  Up|           1.0|0.05263158| 0.5263158|
|tt0356634|            Garfield|           1.0|0.05263158| 0.5263158|
|tt0455499|Garfield: A Tail ...|           1.0|0.05263158| 0.5263158|
|tt0198781|      Monsters, Inc.|           1.0|0.05263158| 0.5263158|
|tt0266543|        Finding Nemo|           1.0|0.05263158| 0.5263158|
|tt1979376|         Toy Story 4|           0.8|      0.25|     0.525|
|tt0435761|         Toy Story 3|           0.8|      0.25|     0.525|
|tt0120630|         Chicken Run|           1.0|       0.0|       0.5|
|tt0432283|   Fantastic Mr. Fox|           1.0|       0.0|       0.5|
+---------+--------------------+--------------+----------+----------+

Funkcja rankująca dla Toy Story:

       id  score
tt0114709   18.0
tt0120363   13.0
tt0120623   11.0
tt0435761   10.0
tt1979376   10.0
tt2446040    9.0
tt0429589    9.0
tt0198781    9.0
tt0317219    9.0
tt0356634    9.0
tt0455499    9.0
tt0230011    9.0
tt0383060    8.0
tt0272183    8.0
tt0299172    8.0
```
Zgodnie z intuicją (a także funkcją rankującą), kolejne
części powinny być bardziej podobne do Toy Story - jest to kontynuacja tej 
samej serii, występują ci sami bohaterowie. Można jednak
wytłumaczyć tak odległe miejsce w rankingu faktem, że części te powstały 
na przestrzeni 23 lat, a bohaterowie tej serii dorastają wraz z widzem, a ich problemy
i sposób postrzegania świata zmienia się w kolejnych częściach.


Ciekawym przykładem są filmy związane z postacią Batmana. Po sprawdzeniu
najbardziej podobnych filmów do "Mrocznego rycerza" otrzymujemy "Batman: początek" oraz 
"Mroczny Rycerz powstaje". Co ciekawe nie znajduje znaczącego podobieństwa do filmu
"Batman" z 2022 roku (analogicznie w druga stronę). 
```
Top 10 najbardziej podobnych filmów do Mrocznego Rycerza:
+---------+--------------------+--------------+----------+----------+
|       id|               tytul|cos_similarity|       IOU|prediction|
+---------+--------------------+--------------+----------+----------+
|tt0468569|     The Dark Knight|           1.0|       1.0|       1.0|
|tt0372784|       Batman Begins|           1.0|0.53846157| 0.7692308|
|tt1345836|The Dark Knight R...|     0.6708204|0.42857143| 0.5496959|
|tt0433387|         Harsh Times|           1.0|0.05263158| 0.5263158|
|tt1289406|         Harry Brown|           1.0|0.05263158| 0.5263158|
|tt0963178|   The International|           1.0|0.05263158| 0.5263158|
|tt0119099|              Fallen|           1.0|0.05263158| 0.5263158|
|tt0381849|        3:10 to Yuma|           1.0|0.05263158| 0.5263158|
|tt0772740|El Bronco de Durango|           1.0|       0.0|       0.5|
|tt0806337| Tumba para un narco|           1.0|       0.0|       0.5|
+---------+--------------------+--------------+----------+----------+

oraz dla Batmana (2022):
+----------+--------------------+--------------+----------+----------+
|        id|               tytul|cos_similarity|       IOU|prediction|
+----------+--------------------+--------------+----------+----------+
| tt1877830|          The Batman|           1.0|       1.0|       1.0|
|tt14857194|Superman: Agent o...|           1.0|0.11111111| 0.5555556|
| tt3156558|Caped Crusader: T...|           1.0|0.05882353| 0.5294118|
| tt3647498|        Blood Father|           1.0|0.05263158| 0.5263158|
| tt5057140|       Hold the Dark|           1.0|0.05263158| 0.5263158|
| tt2602174|     Batman Revealed|           1.0|0.05263158| 0.5263158|
| tt1235522|         Broken City|           1.0|0.05263158| 0.5263158|
| tt2345737|           The Rover|           1.0|0.05263158| 0.5263158|
| tt2101341|       Dead Man Down|           1.0|0.05263158| 0.5263158|
| tt4343130|         Uptake Fear|           1.0|       0.0|       0.5|
+----------+--------------------+--------------+----------+----------+
```
Możemy to tłumaczyć tym, że pomimo tego, że są to filmy tego samego wydawnictwa o tym samym bohaterze, to jednak powstały w dużym odstępie 
czasu i występują w nich inni aktorzy. 


