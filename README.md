# Kosteczkator
To będzie ten nasz projekt na inżynierkę, a przynajmniej ta mała sieć neuronowa do klasyfikowania co tam na tej kosteczce wypadło \
...a przynajmniej taką mam nadzieję.


# Jak pisać prackę:

w ./Pracka znajdują się wszystkie źródła TeX'a.
main.tex jak się domyślacie jest głównym plikiem, a osobne rozdziały macie w chapters.
Wrzucam też Issue z zadankiem żeby każdy sobie to przekompilował i zobaczył czy MiKTeX działa na danej maszynie itd


# WAŻNE!
Na gicie nie znajdziecie plików ze zdjęciami, na których trenowany był model. \
Przedstawiam tutaj drzewko, jak powinny być poustawiane w głównym folderze repozytorium.

```
data/
├── train/
│   ├── 1/
│   ├── 2/
│   ├── [...]
│   └── n/
├── test/
│   ├── 1/
│   ├── 2/
│   ├── [...]
│   └── n/
└── validation/
    ├── 1/
    ├── 2/
    ├── [...]
    └── n/
```

Poprawny podział danych to coś **około**

-> 70% do train \
-> 15% do test \
-> 15% do validation 
