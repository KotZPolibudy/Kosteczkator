def test_pojedynczych_bitow(bity):
    if 9725 < bity.count(1) < 10275:
        testPB = True
    else:
        testPB = False
    return testPB

def test_dlugiej_serii(b, bity):
    serie = {}
    test = True
    for i in bity:
        if i == b:
            if dlugosc > 0:
                if dlugosc > 6:
                    if dlugosc > 25:
                        test = False
                    dlugosc = 6
                if dlugosc in serie:
                    serie[dlugosc] = serie[dlugosc] + 1
                else:
                    serie[dlugosc] = 1
            dlugosc = 0
        else:
            dlugosc += 1
    return test, serie

def test_serii(seria):
    test = False
    if 2315 < seria[1] < 2685:
        if 1114 < seria[2] < 1386:
           if 527 < seria[3] < 723:
               if 240 < seria[4] < 384:
                    if 103 < seria[5] < 209:
                        if 103 < seria[6] < 209:
                            test = True
    return test

def serii_testy(bity):
    testDS0, seria0 = test_dlugiej_serii(1, bity)
    testDS1, seria1 = test_dlugiej_serii(0, bity)
    if testDS0 and testDS1:
        testDS = True
    else:
        testDS = False
    testS0 = test_serii(seria0)
    testS1 = test_serii(seria1)
    if testS0 and testS1:
        testS = True
    else:
        testS = False
    return testS, testDS

def test_pokerowy(seria):
    poker = {}
    czworka = ''
    n = 0

    for i in range(len(seria)):
        if len(czworka) < 4:
            czworka = czworka + str(seria[i])
        else:
            n += 1
            if czworka in poker:
                poker[czworka] = poker[czworka] + 1
            else:
                poker[czworka] = 1
            czworka = str(seria[i])
    poker[czworka] = poker[czworka] + 1

    myKeys = list(poker.keys())
    myKeys.sort()
    poker = {i: poker[i] for i in myKeys}

    X = 0
    suma = 0
    for i in poker:
        p = poker[i]*poker[i]
        suma = suma + poker[i]
        X = X + p
    X = 16*X/5000 - 5000

    if 2.14 < X < 57:
        testP = True
    else:
        testP = False

    return testP

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
    return testC

def czy_uczciwa(bity, rzuty):
    testPB = test_pojedynczych_bitow(bity)
    testS, testDS = serii_testy(bity)
    testP = test_pokerowy(bity)
    testC = test_chi2(rzuty)
    if testC and testP and testS and testDS and testPB:
        print("Ta kość jest uczciwa! :>")
    else:
        print("Ta kość niestety nie jest uczciwa :<") 