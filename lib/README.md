# lib

> Katalog lib jest miejscem, gdzie umieszczane są współdzielone komponenty, które mogą być używane w wielu aspektach aplikacji. Rzeczy w tym folderze nie powinny być ściśle związane z wybraną aplikacją, i teoretycznie powinny być w stanie zostać wyciągnięte z jednego projektu do drugiego oraz działać zgodnie z oczekiwaniami (zakładając, że wszystkie zależności są dostępne).

Przykłady rzeczy, które można umieszczać w folderach lib:
- Jeśli potrzebujemy zdefiniować politykę/proces ładowania bootstrapowanych danych ze strony do kodu frontendowego, możemy zdefiniować klasę/metodę w pliku w folderze lib. Jest to tylko funkcjonalne i nie jest związane z żadnym z kodów aplikacji.

- Jeśli musimy zbudować własne komponenty UI (np. połączyć niektóre funkcje Tagging w obszarze tekstowym - tagowanie), możemy wykorzystać lib. Kod w lib tylko zarysowuje jak działa komponent, ale nie implementuje żadnej funkcjonalności specyficznej dla aplikacji. Możemy następnie włączyć to do podstawowej aplikacji i używać jej tak, jakby była to biblioteka trzeciej strony.

Zasadniczo, wszystko, co może być zależnością od strony trzeciej, której nie chcemy umieszczać w jej własnym repozytorium i ustawiać zarządzania nad nią, **możemy użyć lib** i mieć tę funkcjonalność czysto odłączoną w swojej głównej aplikacji.

Krótki artykuł [What Code Goes in the Lib/ Directory?](https://codeclimate.com/blog/what-code-goes-in-the-lib-directory/)