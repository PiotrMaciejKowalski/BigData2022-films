## Research metryk

Aby ocenić jak dobry jest zbudowany model stosujemy odpowiednie metryki. Do oceny
jakości naszego modelu użyjemy metryki, której szkic zaprezentowany jest 
poniżej.

Dla zadanego filmu tworzymy listę filmów testowych o ustalonej długości n 
(dla przykładu poniżej n=5).

```
film
lista -> [film1, film2, film3, film4, film5]
```

Następnie dla każdego elementu z listy liczymy score: 

```
score_i = 0
jeżeli warunek prawdziwy:
    score_i = +1
```
czyli dla każdego filmu z listy sprawdzamy ilość zgodnych warunków z zadanym początkowo filmem. Warunki 
te będziemy budować w oparciu o zawartość tabeli z danymi. Przykładowe warunki dla 
obecnej tabeli:

- film_czy_dla_doroslych == film_i_czy_dla_dorosłych
- film_epoka == film_i_epoka
- film_rodzaj == film_i_rodzaj
- film_gatunek == film_i_gatunek
- |film_rok_wydania_produkcji == film_i_rok_wydania_produkcji| < 10

Następnie szeregujemy filmy z listy od najwyższego do najniższego score'a
i premiujemy pozycję na liście - score filmu na pierwszym miejscu mnożymy razy 5,
na drugim razy 4. Postępujemy analogicznie aż do ostaniej pozycji na liście, 
której score mnożymy razy 1. W ten sposób uzyskamy listę filmów 
posortowanych od najbardziej do najmniej podobnego.
