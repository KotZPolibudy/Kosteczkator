import math
import random
from datetime import datetime
import os 
import matplotlib.pyplot as plt
import numpy as np

na_bity = {}
na_bity[1] = '001'
na_bity[2] = '010'
na_bity[3] = '011'
na_bity[4] = '100'
na_bity[5] = '101'
na_bity[6] = '110'
na_bity[7] = '111'
na_bity[8] = '000'

def data():
    data = str(datetime.today())
    data = data.split()
    data[1] = str(data[1][:-7])
    data[1] = data[1].split(':')
    data[1] = data[1][0] + '-' + data[1][1] + '-' + data[1][2] 
    data = str(data[0]) + '_' + str(data[1])
    return data

def test_pojedynczych_bitow(zera, jedynki):
    if (9725 < zera < 10275) and ((9725 < jedynki < 10275)):
        testPB = True
    else:
        testPB = False
    return testPB

def testy_serii(seria): #test serii i test długiej serii
    lewy = [-1, 2343, 1135, 542, 251, 111, 111]
    prawy = [26, 2657, 1365, 708, 373, 201, 201]
    test = True
    for i in range(7):
        if not(lewy[i] < seria[0][i] < prawy[i]) or not(lewy[i] < seria[1][i] < prawy[i]):
            test = False
    return test

def test_pokerowy(poker):
    X = 0
    suma = 0
    for i in poker:
        p = poker[i]*poker[i]
        suma = suma + poker[i]
        X = X + p
    X = 16*X/5000 - 5000

    if 2.16 < X < 46.17:
        testP = True
    else:
        testP = False

    return testP, X

def test_chi2(rzuty):   
    e = sum(rzuty)/len(rzuty)
    x2 = 0
    for n in rzuty:
        x2 += (n-e)*(n-e)/e
    if len(rzuty) == 8:
        p = 14.067
    if p < x2:
        testC = False
    else:
        testC = True
    return testC, x2

def entropia(rzuty):
    e = 0
    suma = sum(rzuty)
    for i in rzuty:
        if i != 0:
            e -= (i / suma) * math.log(i / suma, 2)
    return e

def entropia_procentowa(e):
    ep = entropia([1,1,1,1,1,1,1,1])
    return e /ep * 100
    

def czy_uczciwa(testy):
    e = entropia(testy['chi'])
    ep = entropia_procentowa(e)
    testC, x2 = test_chi2(testy['chi'])
    testPB = test_pojedynczych_bitow(testy['zera'], testy['jedynki']) 
    testS = testy_serii(testy['seria'])
    testP, X = test_pokerowy(testy['poker'])
    
    
    return [testC, testPB, testS, testP, round(e, 3), round(ep, 3), x2, X]
        

def start():
    testy = {}
    testy['ile'] = 0 #testy losowości (kryptografia) można przeprowadzić tylko, jeśli mamy 20 000 bitów
    testy['chi'] = [0, 0, 0, 0, 0, 0, 0, 0] #zliczanie, ile razy wypadła każda ścianka (8 na kostce liczymy jako 0)
    testy['zera'] = 0 #zliczamy wszystkie zera na bitach
    testy['jedynki'] = 0 #zliczamy wszystkie jedynki na bitach
    testy['seria'] = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]] #zliczone, ile razy występuje seria o danej długości (poza indeksem 0)
    testy['poker'] = {} #słownik na zliczanie wystąpień każdej czwórki bitów
    testy['czworka'] = ''
    testy['last'] = [0, 0, ''] #zlicza aktualną serię zer [0] lub jedynek [1], [2] do sprawdzania czy seria 0 czy 1
    return testy

def zapisz(testy, wyniki):
    plik = 'src/testy_wyniki/wyniki_testow_' + data() + '.txt'
    f = open(plik, 'w')
    f.write("Przeanalizowane bity:  ")
    f.write(str(testy['ile']))
    
    f.writelines(['\nEntropia: ', str(wyniki[4]), '\n'])
    f.writelines(['Entropia procentowa: ', str(wyniki[5]), '%\n'])
    
    f.write("\nWyniki testu chi-kwadrat\n")
    for i in range(len(testy['chi'])):
        f.writelines([str(i+1), ': ', str(testy['chi'][i]), '\n'])
    f.writelines(["Wynik: ", str(wyniki[0]), ' (', str(round(wyniki[6], 3)), ')\n\n'])
    
    f.write('Test pojedynczych bitów:\n')
    f.writelines(['0', ': ', str(testy['zera']), '\n'])
    f.writelines(['1', ': ', str(testy['jedynki']), '\n'])
    f.writelines(["Wynik: ", str(wyniki[1]), '\n\n'])
    
    f.write('Testy serii:\n')
    for n in range(len(testy['seria'])):
        f.writelines(['Dla ', str(n),'\n'])
        f.writelines(['Najdłuższa seria: ', str(testy['seria'][n][0]), '\n'])
        for i in range(1, len(testy['seria'][n])):
            f.writelines([str(i), ': ', str(testy['seria'][n][i]), '\n'])
    f.writelines(["Wynik: ", str(wyniki[2]), '\n\n'])
    
    f.write('Test pokerowy:\n')
    myKeys = list(testy['poker'].keys())
    myKeys.sort()
    testy['poker'] = {i: testy['poker'][i] for i in myKeys}
    for czworka in testy['poker']:
        f.writelines([str(czworka), ': ', str(testy['poker'][czworka]), '\n'])
    
    f.writelines(["Wynik: ", str(wyniki[3]), ' (', str(round(wyniki[7], 3)),')\n'])
    

def rzuc():
    x = random.randint(0,7)
    return(x)

def neguj(x):
    if x == 0:
        n = 1
    else:
        n = 0
    return n

def aktualizuj(rzut, testy):
    #zliczanie, ile mamy już bitów
    #print(testy)
    testy['ile'] = testy['ile'] + 3
    
    #zliczanie, ile razy wypadła każda ścianka (8 na kostce liczymy jako 0)
    testy['chi'][rzut-1] += 1
    bity = na_bity[rzut]
    
    if testy['ile'] > 20000:
        testy['ile'] -= 1
        bity = bity[:-1]

    #zliczanie wszystkich zer i jedynek
    testy['zera'] += bity.count('0')
    testy['jedynki'] += bity.count('1')
    
    #zliczanie serii zer i jedynek
    for i in bity:
        i = int(i)
        if testy['last'][2] == '':
            testy['last'] = [0, 0, i]
            testy['last'][i] = 1
        elif testy['last'][2] != i:
            x = neguj(i)
            if testy['last'][x] > 6:
                if testy['seria'][x][0] < testy['last'][x]:
                    testy['seria'][x][0] = testy['last'][x]
                testy['last'][x] = 6
            testy['seria'][x][testy['last'][x]] += 1
            testy['last'] = [0, 0, i]
            testy['last'][i] = 1
        else:
            testy['last'][i] += 1
            
    #zliczanie, ile razy wystąpiła każda czwórka bitów
    czworka = testy['czworka']
    czworka = czworka + bity
    if len(czworka) >= 4:
        if czworka[:4] in testy['poker']:
            testy['poker'][czworka[:4]] += 1
        else:
            testy['poker'][czworka[:4]] = 1
        testy['czworka'] = czworka[4:]
    else:
        testy['czworka'] = czworka
    return testy

def generuj():
    i = 6667
    while i > 0:
        rzut = rzuc()
        aktualizuj(rzut, testy)
        i -= 1
    return testy

def czytaj(path):
    os.chdir(path) 
    i = 6667
    for file in os.listdir():
        file_path = f"{path}/{file}"
        f = open(file_path, 'r')
        for line in f:
            if i > 0:
                wynik = line.split(";")
                wynik = int(wynik[2][1])
                i -= 1
                aktualizuj(wynik, testy)
            else:
                return testy
    print(i)
    return testy

if __name__ == "__main__":
    ocr = True
    path = "C:/Users/Julka/Desktop/studia/semestrVII/inzynierka/wyniki"
    testy = start()
    if not ocr:
        testy = generuj()
    else:
        testy = czytaj(path)
    wyniki = czy_uczciwa(testy)
    os.chdir("c:/Users/julka/Documents/GitHub/Kosteczkator") 
    zapisz(testy, wyniki)