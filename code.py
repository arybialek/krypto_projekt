# Program typu szyfrator - deszyfrator. Zasada działania szyfratora:
# - zamiana ciągu liter wprowadzonego tekstu na reprezentację liczbową kodu ASCII
# - wczytanie do kolumny macierzy (od dołu) odpowiedniej ilości jedynek 
#   odpowiadającej wartości liczbowej kodu ASCII np. c = 67, to wpisujemy 
#   w kolumnę macierzy od dołu 67 jedynek - powtarzane dla każdego znaku w tekście
# - utworzoną macierz odwracamy o 180 stopni i zamieniamy zera z jednynkami 
# - tak utworzoną macierz zapisujemy jako zdjęcie w formacie .png
# 
# Zasada działania deszyfratora jest podobna jak szyfratora, ale kroki wykonujemy
# w odwrotnej kolejności.  

# Wykorzystuje indeksowanie.

import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
################################### Definicje funkcji ############################################

def tekst_od_uzytkownika():
    loop = True
    while(loop):
        znaki = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
        
        user_input = str(input('\nWpisz zdanie, ktore chcesz zaszyfrowac i naciśnij enter: \n'))
        if any(znak in user_input for znak in znaki):
            print("\nWpisałeś polski znak! Proszę wpisać frazę bez polskich znaków.\n")
        else: 
            loop = False  
    
    return user_input

 

def szyfrator():
    """
    Funkcja, która szyfruje tekst wpisany przez użytkownika, a 
    utworzoną macierz konwertuje na obraz i zapisuje go w 
    formacie .png

    Argumenty: input (str) - tekst wpisany przez użytkownika

    Rezultat: szyfr.png - plik formatu .png z zaszyfrowaną frazą

    """
    text = tekst_od_uzytkownika()
    # Tworzę macierz jedynek (140 x 140) i każdą wartość mnożę przez 255, w
    # wyniku czego dostaję macierz 255 o wymiarach (140 x 140). Dtype uint8
    # oznacza, że każda wartość (piksel) jest liczbą z przedziału [0, 255] i
    # zajmuje 1 Bajt.
    matrix = 255 * np.ones((140, 140), dtype=np.uint8)

    # Zamień napis na listę wartości ASCII.
    ascii_array = [ord(c) for c in text]

    # Koduj po kolei każdą wartość na wektor.
    for n, character in enumerate(ascii_array):
        
        # Utwórz wektor zer o wymiarach (140 x 1) (czarne paski)
        vec = np.zeros((140,))

        # (od góry) wpisz białe piksele tak, żeby czarny pasek miał taką wysokość,
        # jaką ma wartość ASCII danego znaku.
        vec[0:(140 - character)] = 255

        # Zamień kolejną kolumnę macierzy na pionowy wektor z zakodowanym znakiem
        # ASCII.
        matrix[:, n] = vec

    # Utwórz obraz z podanej macierzy
    image = Image.fromarray(matrix)
    image.save('szyfr.png')
    print("\nUtworzono plik z obrazem w formacie .png o nazwie 'szyfr.png' w folderze roboczym.\n")
    plt.imshow(matrix, cmap='gray')
    plt.show()

    
def deszyfrator():
    """
    Funkcja, która deszyfruje obraz - szyfrowany wcześniej za pomocą szyfratora
    Wczytuje obraz, a następnie zwraca odszyfrowaną frazę.

    Rezultat: decoded_message (str) - odszyfrowany tekst
    """
    # Załaduj obraz
    loaded = Image.open('szyfr.png')

    # Konwertuj obraz do np.array
    data = np.asarray(loaded, dtype="uint8" )

    numbs = []
    for column in data.T:
        numbs.append(list(Counter(column).items()))

    ascii_numbs = []
    for num in numbs:
        for first_tuple, second_tuple in num:
            if first_tuple == 0:
                ascii_numbs.append(second_tuple)

    decoded_message = " "
    for numb in ascii_numbs:
        decoded_message += chr(int(numb))   

    print("\nOdszyfrowana fraza: " + decoded_message + "\n")

############################### MENU ##################################
print("\n-------------- Program typu szyfrator - deszyfrator -------------\n")

print("\nZasada działania szyfratora: \n- zamiana ciągu liter wprowadzonego tekstu na reprezentację liczbową kodu ASCII" +
"\n- wczytanie do kolumny macierzy (od dołu) odpowiedniej ilości jedynek " +
  "\n odpowiadającej wartości liczbowej kodu ASCII np. c = 67, to wpisujemy" +
  "\n w kolumnę macierzy od dołu 67 jedynek - powtarzane dla każdego znaku w tekście" +
  " \n- utworzoną macierz odwracamy o 180 stopni i zamieniamy zera z jednynkami" +
 "\n- tak utworzoną macierz zapisujemy jako zdjęcie w formacie .png" +
"\nZasada działania deszyfratora jest podobna jak szyfratora, ale kroki wykonujemy" +
"\nw odwrotnej kolejności.\n\n Uwaga: Program nie obsługuje polskich znaków.\n")

loop = True
while(loop):
    print("Wybierz co chcesz zrobić: \n" +
    "[ 1 ] Zaszyfrować tekst. \n" +
    "[ 2 ] Odszyfrować tekst.\n"+    
    "[ 3 ] Zakończyć program.\n")

    try: 
        ans = int(input("Twój wybór: "))
        if ans == 1:
            print("\nWybrano opcję szyfrowania.\n")
            szyfrator()
        elif ans == 2:
            print("\nWybrano opcję deszyfrowania.\n")
            deszyfrator()
        elif ans == 3:
            print("\nZakończono działanie programu.\n")
            loop = False
        else:     
            print("\nWybrałeś inną wartość niż 1, 2 lub 3. Wybierz ponownie.\n")

    except ValueError:
        print("\nBłąd. Wpisz cyfrę!\n")    
