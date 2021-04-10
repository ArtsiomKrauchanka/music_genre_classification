

Artsiom Krauchanka,

**KLASYFIKACJA GATUNKU MUZYKI na podstawie KNN i Naive Bayes**



**1. Streszczenie projektu**

Celem projektu jest implementacja aplikacji pozwalającej na klasyfikację gatunku wybranego pliku audio formatu (wav.) na podstawie algorytmów k-najbliższych sąsiadów oraz naive bayes.

Zaimplementowana aplikacja w pełni realizuje powyższy cel. W dodatek aplikacja nie jest powiązana z konkretnymi gatunkami. Gatunki, jak i sukces aproksymacji zależą od bazy danych.

Bazę danych można zbudować własnoręcznie. Aplikacja wspiera następujący format bazy:

Folder\*nazwa\_bazy\*/1..\*nazwa\_gatunku\*/ 1.. \*nazwa\_audio.wav\*

Przy zmianie bazy danych są ponownie trenowane modele, co dla bazy posiadającej 1000 plików
audio (1,23GB) trwa ok. 30 min.

**2. Wykorzystanie technologie / biblioteki**

*Nazwa biblioteki - Opis wykorzystanych metod z biblioteki*


Librosa - Biblioteka służy do analizy audio

load(track\_path) – przedstawia audio w wygodny do analizy sposób

feature.spectral\_centroid - centrum masy sygnału,

feature.spectral\_rolloff – spadek sygnału

feature.zero\_crossing\_rate - przedkość zmiany sygnału

feature.chroma\_stft – charakterystyka tonacji

feature.mfcc - charakterystyki spektru

Numpy - Biblioteka do pracy z macierzami

array – macierzy

mean – wartość średnia

sum – suma wszystkich elementów

Abstractmethod – annotacja do metody abstrakcyjnej

ABC – Do realizacji mechanizmów dziedziczenia

Tkinter – realizacja interfejsu

filedialog.askopenfile – do wskazania pliku

filedialog.askdirectory - do wskazania folderu





**3. Architektura**

Realizowany został wzorzec „Strategia”:

Klasa Classifier jest klasyfikatorem, który może dokonać klasyfikacji gatunku używając obiektów
implementujących klasę abstrakcyjną Model (kilka metod jest używana w obu model np. count\_distance()).

![diagram](/readme_images/diagram.png)

Klasa główna – Main posiada realizacje interfejsu oraz obiekt Classifier do realizacji klasyfikacji.


**4. Zrzuty ekranów z projektu**

Widok startowy projektu:

![widok](/readme_images/Start.png)

Na górze są wskazane wybrana baza oraz plik audio (na widoku startowym jeszcze nie
wybrany). Domyślnie używana jest baza używana poprzednio.

Następna sekcja – Menu.W menu dostępne dwie opcje: wybór bazy danych, wybór pliku audio.

Sekcja „Start” zawiera przycisk startujący obliczenia.

Następna sekcja – wyniki. Pięć najlepiej pasujących gatunków, od najbardziej do mniej,
według dwóch algorytmów KNN i Bayesa.

Ostatnia sekcja – status. Wyświetla różne obecne statusy programu np.” trwa obliczenie” lub
wskazuje rekomendacje. Poniższy przykład pokazuje „choose audio” – nie wybrano pliku, ale
naciśnięto przycisk „start”.

Wybór plika audio:

![sile_selection](/readme_images/file_selection.png)

Program też posiada wyjścia do wiersza poleceń – zostało to zrobione do debagowania, ale

zdecydowałem to zostawić, ponieważ wskazuje to etap, na którym są obliczenia w momencie

gdy nie odpowiada aplikacja.

Poniżej przykład obliczenia najlepszego k do algorytmu KNN:

Poniżej są przykłady wyników działania aplikacji:

![one](/readme_images/screen_one.png)
![rwo](/readme_images/screen_two.png)








