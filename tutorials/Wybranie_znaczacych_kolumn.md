# Wybranie znaczących kolumn
W tym materiale wybierzemy te kolumny, z którch będziemy korzystać w przyszłości. Dokument jest podzielony na siedem części i w każdej z nich przeanalizujemy kolejną tabelę. Na samym końcu znajduje się podsumowanie, w którym przedstawione zostaną kolumny niezbędne do dalszej pracy.
**Uwaga**
W dalszej części pracy nie uwzględniamy pierwszych kolumn, które pełnią funkcję ID analizowanych tabel. Jeżeli wybralismy chociaż jedną kolumnę z danej tabeli, to niezbędnym jest również uwzględnienie pierwszej kolumny ID, dzięki której będziemy później mogli połączyć tabele.
## *title_ratings*
Ta tabela zawiera informacje o ocenach *averageRating* oraz ilości ocen *numVotes*. Jeżeli chcemy w przyszłości badać podobieństwo dwóch filmów, to ich ocena może również posłużyć jako istotne kryterium. Podobnie z liczbą ocen, bo czy możemy powiedzieć, że film *Skazani na Shawshank* ze średnią ocen $$9.3$$ oraz $$2.7$$ milionem oddanych głosów jest „równie dobry”, co inny film ze średnią $$9.3$$ i liczbą ocen $$100$$?
## *title_principals*
W tej tabeli znajdują się dane dotyczące osób, które pracowały przy danej produkcji. Kolumny, które w tym przypadku są dla nas najistotniejsze to *ncost* - id osoby, która brała udział w produkcji i *category* - jej rola. Filmy, przy których twrorzeniu uczestniczą Ci sami operatorzy filmowi, scenografowie czy aktorzy często są do siebie podobne, mają podobny „klimat”.
## *title_episode*
Jedyną istotną dla nas kolumną w tej tabeli jest *parentTconst*. Jest to informacja o tym do jakiej serii należy dany odcinek, np. wszystkie odcinki serialu *Przyjaciele* posiadają tą samą wartość *parentTconst*. Pozostałe kolumny informują nas o numerze odcinka i sezonu, co w porównywaniu dwóch produkcji nie ma żadnego znaczenia.
## *title_crew*
Ta tabela zawiera dane na temat id reżysera oraz scenarzysty danej produkcji. Wybieramy wszystkie kolumny. Podobnie jak w przypadku *title_principals* są to istotne dla nas informacje - filmy wychodzące od tych samych reżyserów czy scenarzystów często są siebie podobne, reprezentują podobne wartości.
## *title_basics*
Z tej tabeli wybieramy wszystkie kolumny. Informacje takie jak typ produkcji, tytuł, czas powstania, długość, gatunek, czy ograniczenia wiekowe są dla nas bardzo istotne.
## *title_akas*
Z tej tabeli nie wybieramy żadnej kolumny. Tytuły produkcji w innych językach nie są dla nas istotnym kryterium porównawcznym.
## *name_basics*
W tym przypadku wybieramy kolumny *primaryName*, *primaryProfession* oraz *knownForTitles*. Tabela zawiera informacje dotyczące ludzi współtworzących prezentowane w datasecie produkcje. Wykluczamy kolumny *birthYear* oraz *deathYear*, ponieważ data powstania filmu informuje nas już o umiejscowieniu danej produkcji na osi czasu.

## Podsumowanie

Poniżej prezentujemy wybrane kolumny z poszczególnych tabel, z których będziemy korzystać w przyszłości. 

| *title_ratings*| *title_principals* | *title_episode*|*title_crew*|*title_basics*|*title_akas*|*name_basics*|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|   
| averageRating|ncost|parentTconst|directors|titleType| |primaryName|
|numVotes|category| |writers|primaryTitle| |primaryProfession|
| | | | |originalTitle| |knownForTitles|
| | | | |isAdult| | |
| | | | |startYear| | |
| | | | |endYear| | |
| | | | |runtimeMinutes| | |
| | | | |genres| | |

     