# Wyrażenia regularne



Wyrażenia regularne są przydatne w wydobywaniu informacji z tekstu.
Innymi słowy, wyrazenia regularne to wzorzec, który opisuje okreslony tekst do wyszukania.
Mogą być w wykorzystywane na przykład przy sprawdzaniu poprawności wypełniania kwestionariusza
(adres, numer telefonu, e-mail).


Na początek należy spojrzeć na tekst jako na ciąg składający się z różnych znaków, 
każda litera, cyfra, znaki specjalne, spacje są postrzegane jako znaki. Korzystając z
wyrażeń reguralnych (w skrócie regex) piszemy wzorce pasujące do określonej sekwencji znaków.

W tym celu mamy wiele tzn. metaznaków, ktorych używamy do dopasowania do określonego typu 
znaków. Poniżej przestawię parę przykładowych znaków specjalnych oraz przykłady ich użycia.

##Metaznaki
Znak \d może być użyty zamiast dowolnej cyfy od 0 do 9, natomiast \D oznacza dowolną literę. Poprzedający ukośnik odróżnia go od
prostego znaku d lub D i wskazuje, że jest to metaznak.

Przykład:

```python
import re
txt1 = "a6"
x = re.search("\D\d", txt1)
if x:
    print('To jest wzorzec')
else:
    print('To nie jest wzorzec')
```
Stosujemy również symbol wieloznaczny, który jest reprezentowany przez . (kropka) i może pasować
do dowolnego pojedynczego znaku. Chcąc natomiast konkrentnie dopasować kropkę korzystamy z wyrazenia \. .

Przykład:

```python
import re
txt1 = "@30gnks"
x = re.search(".\d\d\D", txt1)
if x:
    print('To jest wzorzec')
else:
    print('To nie jest wzorzec')
```
Jeśli chcemy dopasować parę określonych znaków definiujemy je w nawiasie kwadratowym. Na przykład
wzorzec [abc] będzie odpowiadał pojedynczej literze a, b lub c.
Natomiast jeśli chcemy by wzorzec pasował do wszystkiego poza określonymi znakami korzystamy z nawiasów
kwadratowych oraz znaku ^. Na przykład [^abc] oznacza dowolny pojedynczy znak, który nie jest
a, b lub c.

Przykład:
```python
import re
txt1 = "gbba"
txt2
x = re.search("[agb][^adg]", txt1)
if x:
    print('To jest wzorzec')
else:
    print('To nie jest wzorzec')
```


Korzystając z notacji nawiasów kwadratowych możemy użyć myślnika do określenia znaku z listy kolejnych znaków.
Na przykład wzorzec [0-6] bedzie pasował do pojedynczego znaku z przedziału od 0 do 6, natomiast
[^n-p] dopasowuje dowolny pojedynczy znak poza literami od n do p.

\w oznacza dowolną cyfrę od 0 do 9, znak od a do z ( z małych i dużych liter) albo podkreślnik, natomiast
\W zastępuje wszystko inne poza \w.

Jeśli mamy potrzebę skorzystać parę razy z tego samego metaznacznika możemy w tym celu skorzystać z 
nawiasów klamrowych. Wyrażenie \d{3} oznacza, że mamy następujące po sobie trzy dowolne cyfy. Możemy
również wyznaczyć zakres. .{2,6} mówi nam, że dowolny znak może wystąpić od dwóch do cześćiu znaków
następujących po sobie.

Przykład:
```python
import re
txt1 = "g65a"
txt2
x = re.search("g\d{2}a", txt1)
if x:
    print('To jest wzorzec')
else:
    print('To nie jest wzorzec')
```


Innymi bardzo użytecznymi znakami są + oraz *. Pierwszy z nich oznacza, że zostanie zwrócone dopasowanie
gdzie określony znak/typ znaków występuje przynajmniej jeden raz, natomiast * występuje zero
lub więcej razy.

Dla przykładu, [abc]+ oznacza, ze litera a, b lub c wystąpi przynajmniej raz w naszym ciągu znaków.
Te wyrażenie może pasować do ciągu znaków takich jak aaaa, bbbb, aabbbccc, cbc.

Kolejnym metaznakiem jest ?, który oznacza opcjonalność. Występujący przed tym metaznakiem znak
może wystąpić wcale albo raz. 

Przykład:

```python
import re
txt1 = "ac"
txt2 = "abc"
x = re.search("ab?c", txt1)
y = re.search("ab?c", txt2)
if x and y:
    print('To jest wzorzec')
else:
    print('To nie jest wzorzec')
```

Przedstawione powyżej metaznaki obrazują nam w jaki sposób możemy korzystać z wyrażeń regularnych.
Mogą być one bardzo przydatne do wyodrębnienia z opisu filmów konkretnego słowa.

Przykład:

```python
txt = "A writer and wall street trader, Nick, finds himself drawn to the past and lifestyle of his neighbor, Jay Gatsby."
x = re.search("\D{4} street", txt)
if x:
    print('To jest wzorzec')
else:
    print('To nie jest wzorzec')

```






















