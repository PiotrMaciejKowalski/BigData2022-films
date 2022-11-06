Tutorial: Learning Hydra for configuring ML experiments - Simone Scardapane
=======================================================

9 minut czytania

Ten post jest przeznaczony jako krótkie, samodzielne wprowadzenie do narzędzia Hydra. Omówiono w nim wiele tematów, w tym jak tworzyć obiekty klas, uruchamiać przeszukiwanie parametrów i sprawdzać poprawność konfiguracji w czasie pracy. Wprowadzenie nie obejmuje pełnego zakresu opcji oferowanych przez Hydrę. W tym celu należy zgłębić [oryginalną dokumentację](https://hydra.cc/docs/next/intro).

> 🔗 Kod dla tego tutoriala jest dostępny na repozytorium GitHub: [https://github.com/sscardapane/hydra-tutorial](https://github.com/sscardapane/hydra-tutorial).

Instalacja i przegląd
-------------------------

Będziemy korzystać z wersji 1.1 biblioteki Hydra, którą można zainstalować poprzez:

    pip install hydra-core==1.1.0.rc1
    

> ⚠️ Uwaga: kilka poniższych instrukcji nie będzie działać poprawnie na poprzednich wersjach biblioteki. Wszystkie zmiany pomiędzy wersjami są udokumentowane [na stronie twórców](https://hydra.cc/docs/next/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path).

Część kodu oparta jest na [PyTorch](https://pytorch.org/),ale można go łatwo dostosować do innych frameworków głębokiego uczenia. Rozważamy klasyczny scenariusz dostrajania, w którym dostrajamy mały model klasyfikacyjny na wierzchu wstępnie wytrenowanej konwencjonalnej sieci neuronowej. Nasza ostateczna konfiguracja będzie wyglądać tak (rysunek może z początku wydawać się niejasny):

![Alt text](../../../../../../../../../C:/Users/User/Desktop/Matematyka%20stosowana%20-%20II%20stopie%C5%84/III%20semestr/Big%20Data%202022/BigData2022-films/tutorials/hydra.jpg)

Po lewej stronie mamy szereg plików konfiguracyjnych, opisujących kolejno:

1.  Konfiguracja dla zbioru danych;
2.  Konfiguracja naszej wstępnie wytrenowanej sieci;
3.  Konfiguracja naszego klasyfikatora wytrenowanego "na szczycie" sieci wstępnie wytrenowanej.

W centrum, Hydra automatycznie ładuje i komponuje nasze pliki konfiguracyjne, dynamicznie nadpisując każdą wartość, którą zażądamy w czasie pracy. 

Po prawej stronie, nasz skrypt treningowy wykorzystuje wynikowy obiekt słownikowy do budowy naszego modelu.

Będziemy budować tę konfigurację krok po kroku, poznając po kolei kilka funkcjonalności Hydry. Mając to na uwadze, zaczynajmy!

Pierwszy krok: manipulowanie plikiem YAML
-------------------------------------

Podczas gdy istnieje [ogromna liczba](https://github.com/vinta/awesome-python#configuration) sposobów na określenie pliku konfiguracyjnego, Hydra pracuje z plikami YAML. Zaczynamy od stworzenia prostego pliku `config.yaml` zawierającego kilka szczegółów dotyczących naszego (fałszywego) zbioru danych obrazkowych:

    # config.yaml
    dataset:
      image:
        size: 124
        channels: 3
      classes: 10
    

[OmegaConf](https://omegaconf.readthedocs.io/en/2.0_branch/) jest prostą biblioteką umożliwiającą dostęp i manipulowanie plikami konfiguracyjnymi YAML:

    from omegaconf import OmegaConf
    conf = OmegaConf.load('config.yaml')
    
    # Accessing values (dot notation or dictionary notation)
    print(conf.dataset.image.channels)
    print(conf['dataset']['classes'])
    
    # Modifying a value
    conf.dataset.classes = 15
    

Konfiguracja jest ładowana jako obiekt `DictConfig`, który zapewnia kilka dodatkowych funkcjonalności (zwłaszcza zagnieżdżanie) w odniesieniu do prymitywnych kontenerów Pythona. Więcej o *OmegaConf* i `DictConfig` można przeczytać na stronie z [oficjalną dokumentacją](https://omegaconf.readthedocs.io/en/2.0_branch/usage.html#creating). Wiele zaawansowanych funkcjonalności w Hydrze jest zudowana na bazie *OmegaConf*, dzięki czemu jest to bardzo przydatna lektura.

Ładowanie i manipulowanie konfiguracją w skrypcie
------------------------------------------------------

Głównym celem Hydry jest zapewnienie prostego sposobu na automatyczne ładowanie i manipulowanie plikiem konfiguracyjnym w skrypcie. Aby to zrobić, [dekorujemy](https://www.geeksforgeeks.org/decorators-in-python/) naszą główną funkcję za pomocą `hydra.main`:

    @hydra.main(config_name='config')
    def train(cfg: DictConfig):
        # We simply print the configuration
        print(OmegaConf.to_yaml(cfg))
    
    if __name__=='__main__':
        train()
    

Kiedy wywołujemy nasz skrypt, konfiguracja jest automatycznie ładowana:

    python main.py
    # Out: 
    #   dataset:
    #     image:
    #       size: 124
    #       channels: 3
    #   classes: 10
    

Wszystkie parametry możemy modyfikować "w locie", korzystając ze [składni Hydry](https://hydra.cc/docs/next/advanced/override_grammar/basic):

    python main.py dataset.classes=15
    # Out: 
    #   dataset:
    #     image:
    #       size: 124
    #       channels: 3
    #   classes: 15 <-- Changed
    

Składnia pozwala również na [dodawanie lub usuwanie parametrów](https://hydra.cc/docs/next/advanced/override_grammar/basic) używając odpowiednio `+parameter_to_add` oraz `~parameter_to_remove`.

Manipulowanie rejestratorami i katalogami roboczymi
--------------------------------------------

Domyślnie Hydra wykonuje każdy skrypt w innym katalogu, aby uniknąć nadpisywania wyników z różnych uruchomień. Domyślna nazwa katalogu to `outputs/<day>/<time>/`.

Każdy katalog zawiera output Twojego skryptu, folder `.hydra` zawierający pliki konfiguracyjne użyte podczas uruchomienia oraz plik `<nazwa>.log` zawierający wszystkie dane, które zostały wysłane do rejestratora. W ten sposób możemy łatwo rejestrować i przechowywać dodatkowe informacje o naszym uruchomieniu:

    import os, logging
    logger = logging.getLogger(__name__)
    
    @hydra.main(config_path='configs', config_name='config')
    def train(cfg: DictConfig):
    
        # Log the current working directory
        logger.info(f'Working dir: {os.getcwd()}')
    
        # ...
    

Jeśli wykonamy skrypt, wszystkie komunikaty dziennika zostaną wypisane na ekranie, oraz zapisane w odpowiednim pliku `.log`:

    python main.py
    # Out: [2021-05-20 13:11:44,299][__main__][INFO] - Working dir: c:<...>\outputs\2021-05-20\13-11-44
    

Konfiguracja Hydry jest również określona w szeregu plików YAML, które są automatycznie ładowane i łączone z naszą własną konfiguracją podczas uruchamiania skryptu, co ułatwia dostosowanie zachowania biblioteki. Możemy na przykład [zmienić katalog roboczy dla danego uruchomienia](https://hydra.cc/docs/next/configure_hydra/workdir):

    python main.py hydra.run.dir='outputs/custom_folder'
    # Out: [2021-05-20 13:13:48,057][__main__][INFO] - Working dir: c:<...>\outputs\custom_folder
    

Jeśli chcesz nadpisać konfigurację dla dowolnego uruchomienia skryptu, możesz dodać ją do pliku konfiguracyjnego. Na przykład, aby [zmodyfikować wyjście rejestratora](https://hydra.cc/docs/next/configure_hydra/logging).

Ładowanie konfiguracji poza skryptem
---------------------------------------------

Czasami możemy potrzebować załadować nasz plik konfiguracyjny poza główną funkcją. Choć możemy to zrobić za pomocą `OmegaConf`, nie zapewnia on wszystkich funkcji dostępnych w Hydrze, w tym większości tego, co wprowadzimy w dalszej części.

[Compose API](https://hydra.cc/docs/next/advanced/unit_testing) zapewnia alternatywny sposób ładowania plików konfiguracyjnych. Jest to szczególnie przydatne wewnątrz notatnika *Jupyter Notebooks*, lub jeśli chcemy przetestować jednostkowo pewne funkcje, które zależą od Hydry. Aby załadować plik konfiguracyjny, musimy najpierw zainicjalizować Hydrę (wystarczy raz na uruchomienie jądra), a następnie załadować plik:

    from hydra import initialize, compose
    initialize('.') # Assume the configuration file is in the current folder
    cfg = compose(config_name='config')
    

> ⚠️ `initialize` może być wywołane tylko raz. Aby użyć go lokalnie, możemy zainicjalizować wewnątrz tymczasowego kontekstu:
> 
>     with initialize('.'):
>       # ...
>     
> 
> Jest to niezwykle przydatne w testach jednostkowych. [Compose API](https://hydra.cc/docs/next/advanced/unit_testing) posiada również alternatywne wersje do uzyskiwania plików konfiguracyjnych z bezwzględnych ścieżek lub modułów.

 Finalnie, jeśli zainicjowaliśmy Hydrę poza kontekstem, a w dowolnym momencie musimy ją ponownie zainicjować, możemy zresetować jej wewnętrzny stan:

    hydra.core.global_hydra.GlobalHydra.instance().clear()

Parametry mogą być również nadpisywane podczas komponowania konfiguracji, jak pokazano w przykładzie poniżej.    

Tworzenie instacji obiektów
---------------------

Kontunuując konfigurację naszego pliku. Następnym krokiem jest skonfigurowanie szczegółów naszej wstępnie wytrenowanej sieci. Ponieważ istnieje [duża liczba wstępnie wytrenowanych sieci konwolucyjnych](https://pytorch.org/vision/stable/models.html) wewnątrz PyTorcha, chcielibyśmy pozostawić ten wybór jako hiper-parametr.

Na szczęście Hydra ma [prostą składnię](https://hydra.cc/docs/next/advanced/instantiate_objects/overview) do tworzenia instancji obiektów lub callables (obiektow, które zachowują się jak funkcję). Najpierw dodajemy to do naszego pliku konfiguracyjnego:

    feature_extractor:
      _target_: torchvision.models.alexnet
    

Zwróć uwagę na specjalny klucz `_target_` określający klasę. Możemy użyć `hydra.utils.instantiate` do stworzenia obiektu tej klasy jako pierwszego kroku naszego kompletnego modelu:

    import torch
    from hydra.utils import instantiate
    
    net = instantiate(cfg.feature_extractor)
    

Możemy przekazać parametry podczas tworzenia instancji, dodając dodatkowe klucze do pliku konfiguracyjnego. Na przykład, możemy określić, czy chcemy załadować wstępnie wytrenowane wagi, czy nie (zauważ, że `pretrained` musi być poprawnym parametrem dla naszej klasy docelowej):

    feature_extractor:
      _target_: torchvision.models.alexnet
      pretrained: True
    

Nie wymaga to żadnych zmian w naszym skrypcie treningowym, ponieważ wszystkie parametry zostaną automatycznie przekazane podczas tworzenia instancji modelu.

Trochę o [programowaniu obiektowym](https://www.kodolamacz.pl/blog/wyzwanie-python-4-programowanie-obiektowe/) w prostym języku.

Interpolacja zmiennych
----------------------

Następnie musimy skonfigurować nasz mały klasyfikator "na szczycie" wstępnie wytrenowanej sieci. Aby to uprościć, możemy skorzystać z kilku przydatnych rzeczy wprowadzonych w najnowszym wydaniu Hydry:

1.  [Instancja rekursywna](https://github.com/facebookresearch/hydra/issues/566) pozwala na rekurencyjne tworzenie instancji dla węzłów pod warunkiem, że posiadają one klucz `_target_`.
2.  Możliwe jest określenie [argumentów pozycyjnych podczas tworzenia instancji](https://github.com/facebookresearch/hydra/issues/1432) za pomocą słowa kluczowego `_args_`.

Dzięki tym narzędziom, otrzymujemy przykład obiektu `torch.nn.Sequential` z dwoma warstwami:

    _target_: torch.nn.Sequential
    _args_:
      - _target_: torch.nn.Linear
        in_features: 9216
        out_features: 100
    
      - _target_: torch.nn.Linear
        in_features: ${..[0].out_features}
        out_features: ${dataset.classes}
    

Również wykorzystujemy funkcje OmegaConf zwanej [variable interpolation](https://omegaconf.readthedocs.io/en/2.0_branch/usage.html#variable-interpolation), która pozwala nam automatycznie określić parametry dla naszej ostatniej warstwy poprzez zebranie ich z reszty pliku konfiguracyjnego. Dodatkowo, OmegaConf 2.1 (wydany wraz z Hydrą 1.1) wprowadza interpolacje _relative_, dzięki czemu możemy zapisać powyższy klucz `in_features` jako `in_features: ${.[0].out_features}`.

Możemy zainicjować wszystkie obiekty tak jak poprzednio:

    print(instantiate(cfg.classifier))
    # Out:
    # Sequential(
    #   (0): Linear(in_features=9216, out_features=100, bias=True)
    #   (1): Linear(in_features=100, out_features=10, bias=True)
    # )
    

Stąd, możemy ułożyć nasz klasyfikator "na szczycie" wstępnie wytrenowanej sieci:

    classifier = instantiate(cfg.classifier)
    net.classifier = classifier
    

> ⚠️ Zakładamy, że wstępnie wytrenowana sieć ma pole `classifier`. Bardziej elastyczną opcją byłoby dodanie tego w samym pliku konfiguracyjnym.

Warto wspomnieć, że zmienne są przypisane tylko wtedy, gdy odpowiednie pola są dostępne. Możemy jednak zmodyfikować nasz skrypt, aby zwracał konfigurację z wszystkimi zmiennymi, dla łatwiejszego debugowania:

    print(OmegaConf.to_yaml(cfg.classifier, resolve=True))
    # Out:
    # _target_: torch.nn.Sequential
    # _args_:
    # - _target_: torch.nn.Linear
    #   in_features: 9216
    #   out_features: 100
    # - _target_: torch.nn.Linear
    #   in_features: 100
    #   out_features: 10
    

Grupy konfiguracyjne
--------------------

W praktyce chcielibyśmy mieć wiele plików konfiguracyjnych, określających różne typy modeli, np. powyższy mały klasyfikator i większy, złożony z większej liczby warstw. Możemy to osiągnąć za pomocą [grup konfiguracyjnych Hydry](https://hydra.cc/docs/next/tutorials/structured_config/config_groups).

Najpierw grupujemy nasze pliki konfiguracyjne wewnątrz folderu `configs`, zawierającego nasz poprzedni plik `config.yaml`, folder `classifiers` zawierający dwa pliki YAML: `small.yaml` (konfiguracja małych klasyfikatorów) oraz `large.yaml` (konfiguracja dużych klasyfikatorów). Ostateczny katalog roboczy wygląda następująco:

    +--main.py
    +--configs/
    |  +--config.yaml --> Main configuration
    |  +--classifiers/
       |  +--small.yaml --> Small classifier
       |  +--large.yaml --> Large classifier
    

Możemy określić domyślną wartość dla naszego klasyfikatora używając ["default list"](https://hydra.cc/docs/next/advanced/defaults_list/), specjalnego węzła `config`, którego Hydra używa do budowy końcowego pliku konfiguracyjnego. W praktyce, wprowadzamy do `config.yaml` poniższe jako obiekt główny:

    defaults:
      - classifier: small
    

Wewnątrz naszego skryptu treningowego klasyfikator będzie dostępny jako `cfg.classifier`, a jego wartość możemy w każdej chwili nadpisać:

    python main.py classifier=large
    

Inicjownie wielu wywołań
-----------------------

Jedną z interesujących konsekwencji posiadania niezależnych folderów dla każdego wywołania jest to, że możemy łatwo przeprowadzić wiele eksperymentów poprzez *sweeping* (zamiatanie) nad pewnymi parametrami, a następnie analizować wyniki patrząc na każdy folder po kolei. Na przykład, możemy uruchomić dwa wywołania z dwoma klasyfikatorami w następujący sposób:

    python main.py -m classifier=small,large
    # Out:
    # [2021-05-20 16:10:50,253][HYDRA] Launching 2 jobs locally
    # [2021-05-20 16:10:50,254][HYDRA] 	#0 : classifier=small
    # ...
    # [2021-05-20 16:10:50,370][HYDRA] 	#1 : classifier=large
    # ...
    
Flaga `-m` (alternatywnie, `--multi-run`) instruuje Hydrę do wykonania *sweepingu*. Istnieją [różne sposoby](https://hydra.cc/docs/next/tutorials/basic/running_your_app/multi-run) na określenie zakresu *"sweepingu* oprócz listy. Hydra obsługuje także wiele zewnętrznych *launcherów i sweeperów*, które nie są opisane w tym poście.

Walidacja konfiguracji za pomocą schematu
------------------------------------------

Zakończymy przegląd Hydry interesującą możliwością *walidacji* podczas wywołania parametrów poprzez określenie *schematu konfiguracji*.

> 👀 Schematy mogą być również używane jako alternatywa dla plików YAML, ale nie obejmujemy tego użycia tutaj. [Zobacz oficjalną dokumentację](https://hydra.cc/docs/next/tutorials/structured_config/schema).

Dla uproszczenia pokazujemy tylko jak walidować parametry dla zbioru danych, a resztę pozostawiamy jako ćwiczenie. Najpierw definiujemy w naszym kodzie zagnieżdżony zestaw klas `dataclass` naśladujących naszą konfigurację, oraz deklarujemy typy za pomocą podpowiedzi:

    @dataclass
    class ImageConfig:
        size: int
        channels: int
    
    @dataclass
    class DatasetConfig:
        image: ImageConfig
        classes: int
    
    @dataclass
    class MainConfig:
        dataset : DatasetConfig
        feature_extractor: Any
        classifier: Any
    

[ConfigStore](https://hydra.cc/docs/next/tutorials/structured_config/config_store/) zapewnia pojedynczy interfejs do komunikacji z wnętrzem Hydry. W szczególności, możemy go użyć do przechowywania naszego schematu w następujący sposób (zwróć uwagę na nazwę, którą przypisujemy schematowi):

    cs = hydra.core.config_store.ConfigStore()
    cs.store(name="config_schema", node=MainConfig)
    

Wewnątrz naszego pliku konfiguracyjnego, możemy powiązać schemat poprzez umieszczenie go wewnątrz listy domyślnej:

    defaults:
       - config_schema
    

Teraz, jeśli spróbujemy nadpisać parametr niewłaściwym typem, wywołanie natychmiast kończy się niepowodzeniem:

    python main.py dataset.classes=0.5
    # Out:
    # Error merging override dataset.classes=0.5
    # Value '0.5' could not be converted to Integer
    #    full_key: dataset.classes
    #    reference_type=DatasetConfig
    #    object_type=DatasetConfig
    
That’s it!

Cały opisany tutaj kod znajduje się na repozytorium GitHub: [https://github.com/sscardapane/hydra-tutorial](https://github.com/sscardapane/hydra-tutorial).

Przekład na język polski wpisu z bloga Simone Scardapane'a [Tutorial: Learning Hydra for configuring ML experiments](https://www.sscardapane.it/tutorials/hydra-tutorial/).