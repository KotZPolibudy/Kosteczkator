# instrukcja obsługi

Ok, to teraz tak, jak ogarnąć się w tym bałaganie?

-szybko.
a najlepiej też prosto i wygodnie i inne synonimy.

tłumacząc krótko:

Założenie:
/data/raw jest podzielone na podfoldery /1 /2 /3 ... /7 /8 i PEEEEEŁNE fotek do wytrenowania

preprocess.py <- przyda się zawsze, w podejściu z własnym modelem i z tesseractem.
Za pomocą tego kodu tworzymy wygodniejsze do odczytania zdjęcia kostek, najlepsze obecnie będą w /data/rescaled
(chociaż kusi mnie, aby jeszcze dodać /data/rescaled_contrast)


następnie, dochodzimy do rozbicia.

ZZZ_tesseract_CZYSTY.py  <- możemy odczytywać numerki w ten sposób jak w tym pliku, niestety większość to będą NULL'e,
a te odczytane i tak nie będą zbytnio trafione

lub:

train.py <- aby wytrenować swój własny model na fotkach które mamy po preprocesie

i potem tak jak jest w predict.py

Rzeczy w tym, aby wydzielić sobie zbiory treningowy i testowy.

Na czas pisania tej notatki, mam te niecałe 200 zdjęć, a to trochę za mało do szkolenia.
Ale robot jest składany, czekam na fotki, jak wylądują, klikam trening! :D 