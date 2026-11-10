# Jak dodać nowy wpis

1. Utwórz plik w folderze `_posts/` o nazwie `RRRR-MM-DD-krotki-tytul.md`, np. `_posts/2026-11-05-spotkanie-w-ministerstwie.md`.
2. Na początku pliku wpisz nagłówek:

   ```
   ---
   title: "Spotkanie w Ministerstwie"
   ---
   ```

   Opcjonalnie możesz dodać pod `title` linię `description: "Krótki opis"`. Będzie widoczny w podglądzie linku na Facebooku i X. Bez niej użyty zostanie pierwszy akapit wpisu.

3. Pod nagłówkiem napisz treść. Pusta linia oddziela akapity. Link: `[tekst](https://adres)`. Pogrubienie: `**tekst**`.
4. Opublikuj:

   ```
   git add _posts
   git commit -m "Nowy wpis"
   git push
   ```

Strona zaktualizuje się po 1–2 minutach.

## Automatyczny wpis na X

Po opublikowaniu nowego wpisu GitHub sam wyśle go na X (gdy wpis pojawi się już na stronie). Tekst posta na X wpisz w nagłówku, w linii `tweet:`. Post idzie bez linku, a link do wpisu trafia sam do pierwszego komentarza pod postem, więc nie wpisuj go:

```
---
title: "Spotkanie w Ministerstwie"
tweet: "MZ potwierdziło na spotkaniu, że… Szczegóły i dokumenty w komentarzu."
---
```

- Bez linii `tweet:` na X pójdzie sam tytuł (link w komentarzu).
- `tweet: false` oznacza, że ten wpis nie trafi na X.
- `link_w_komentarzu: false` oznacza, że link trafi na koniec posta zamiast do komentarza.
- Tekst powinien mieć najwyżej ok. 280 znaków (przy `link_w_komentarzu: false` ok. 250, bo link zajmuje 23).
- Poprawki starego wpisu nie wysyłają niczego na X, tylko nowe pliki.

## Udostępnianie na Facebooku

Facebook nie pozwala wstawić gotowego tekstu przez link. Dlatego przycisk „na Facebooku” rozwija ramkę z zajawką, przyciskiem „Kopiuj tekst” i linkiem do Facebooka, gdzie czytelnik wkleja tekst. Tekst zajawki wpisz w nagłówku, w linii `fb:` (bez linku, bo Facebook sam dołącza podgląd wpisu):

```
fb: "Ministerstwo Zdrowia potwierdziło, że… Minister zdrowia Jolanta Sobierańska-Grenda… #NF1 #neurofibromatoza #ChorobyRzadkie"
```

- Bez linii `fb:` skopiuje się tytuł z opisem i hashtagi #NF1 #neurofibromatoza #ChorobyRzadkie.
- Oznaczeń (@) nie da się przenieść przez schowek: po wklejeniu trzeba wpisać @ i nazwę, np. „@Ministerstwo Zdrowia”, i wybrać stronę z listy.
- Podgląd linku (obrazek, tytuł, opis) bierze się z `title` i `description`. Jeśli Facebook pokazuje stary opis, wklej adres wpisu na stronie developers.facebook.com/tools/debug i kliknij „Scrape Again”.

## Grafika do wpisu (X i Facebook)

Każdy nowy wpis dostaje grafikę: krótki, mocny tekst (cytat, zestawienie cytatów albo liczby) na jasnym lub ciemnym tle, bez logo, z adresem nf1news.pl w rogu. Grafikę robi Claude przy przygotowaniu wpisu i pokazuje ją razem z tekstem na X i FB.

- **1200×630** (`assets/grafiki/NAZWA-WPISU.png`) to podgląd linku na Facebooku i X. Trafia do nagłówka wpisu jako `image:`.
- **1080×1080** (`assets/grafiki/NAZWA-WPISU-kwadrat.png`) idzie automatycznie jako zdjęcie w poście na X (zajmuje więcej miejsca na ekranie telefonu niż podgląd linku). Na Facebooku można ją dodać jako zdjęcie do posta.

W nagłówku wpisu:

```
image: /assets/grafiki/2026-11-06-tytul.png
grafika_alt: "Opis tego, co jest na grafice, dla osób niewidomych"
```

- `grafika_x: false` oznacza post na X bez grafiki, a `grafika_x: /assets/grafiki/inna.png` wysyła inną grafikę niż kwadratowa.
- Jeśli X odrzuci grafikę, post i tak pójdzie, tylko bez niej.

Jak zrobić grafikę: opis treści zapisz w pliku `grafiki/NAZWA-WPISU.json` (nazwa jak plik wpisu, bez `.md`) i uruchom:

```
node narzedzia/grafika.mjs grafiki/NAZWA-WPISU.json
```

Pola pliku `.json`:

- `uklad`: `zestawienie` (2–3 cytaty jeden pod drugim, np. słowa vs. czyny), `cytat` albo `naglowek` (jeden duży tekst), `liczby` (2–3 duże liczby z podpisami).
- `motyw`: `jasny` (domyślnie) albo `ciemny`.
- `etykieta` (mały kolorowy napis nad tekstem, np. data albo „Pilne”), `tekst`, `podpis` (szary, pod tekstem), `kolor`: `zielony`, `czerwony`, `niebieski`, `pomaranczowy`.
- w `zestawienie` lista `elementy`, każdy z polami `etykieta`, `tekst`, `podpis`, `kolor`; w `liczby` lista `liczby` z polami `liczba`, `opis`, `kolor`.
- `pytanie`: pogrubione zdanie na dole, najlepiej pytanie do Ministerstwa albo wezwanie do działania.
- `alt`: opis grafiki, ten sam co `grafika_alt` we wpisie.
- `==tekst==` w dowolnym polu daje żółte wyróżnienie. Wyróżniaj jedno, najmocniejsze zdanie.

Przykłady są w folderze `grafiki/`. Zasady: najwyżej ok. 15 słów dużym drukiem, tylko cytaty i liczby, które są we wpisie, kontrast kolorów (zielony „przed”, czerwony „po”).

## Wykres słupkowy

Wklej do wpisu taki fragment i zmień etykiety, liczby i szerokości:

```html
<div class="chart">
  <p class="legend"><span class="item"><span class="bar c1"></span>Seria A</span> <span class="item"><span class="bar c2"></span>Seria B</span></p>
  <div class="row"><span>2027</span><span class="track"><span class="bar c1" style="width:40%"></span>2,2 mln zł</span></div>
  <div class="row"><span></span><span class="track"><span class="bar c2" style="width:20%"></span>1,1 mln zł</span></div>
</div>
```

- **Kolory:** `c1` niebieski, `c2` pomarańczowy, `c3` morski, `c4` żółty, `c5` różowy, `c6` zielony, `c7` fioletowy, `c8` czerwony. Używaj ich po kolei: pierwsza seria `c1`, druga `c2` itd. Ta sama rzecz powinna mieć ten sam kolor w każdym wykresie. Kolory same dopasowują się do jasnego i ciemnego trybu i są czytelne dla osób z zaburzeniami widzenia barw.
- **Szerokość:** największa wartość dostaje `width:70%`, a reszta proporcjonalnie (wartość ÷ największa × 70).
- **Wartości:** zawsze wpisuj liczbę obok słupka, a dane pokaż też w tabeli. Wtedy wykres da się odczytać bez rozróżniania kolorów.

## Anonimowość przy publikowaniu

Zanim pierwszy raz zrobisz `git commit` na swoim komputerze, ustaw w folderze bloga neutralny podpis:

```
git config user.name "NF1 News"
git config user.email "TWOJ-NUMER+LOGIN@users.noreply.github.com"
```

Adres `…@users.noreply.github.com` znajdziesz na GitHubie w **Settings → Emails**, pod opcją „Keep my email address private”.

## Ramka „Zacznij tutaj” na stronie głównej

Wpis trafia do ramki, jeśli ma w nagłówku `wazne:` z numerem (kolejność w ramce) i opcjonalnie `short:` (krótszy tytuł do ramki), np.:

```
wazne: 1
short: "Co pokazał pilotaż: dane z raportu AOTMiT"
```

Strona główna pokazuje 10 najnowszych wpisów jako zajawki: tytuł, data, `description` i „Czytaj dalej”.

## Artykuł na stronie Wiedza

Każdy artykuł to osobny plik w folderze `_wiedza/`, np. `_wiedza/2026-10-06-leki-mek-guzy-splotowate.md`. Strona sama ustawia artykuły od najnowszego, dodaje wyszukiwarkę i przyciski tematów.

```
---
title: "Tytuł po polsku"
data: 2026-10-06
zrodlo: "Nazwa serwisu (kraj)"
autor: "Imię Nazwisko"
jezyk: angielski
link: "https://adres-artykulu"
tematy: [leczenie, guzy splotowate, leki MEK]
lead: "Jedno-dwa zdania o czym jest artykuł."
---

**Najważniejsze informacje:**

- punkt 1
- punkt 2
```

- `tematy` tworzą przyciski filtrowania. Używaj tych samych słów co w innych artykułach (np. „dorośli”, a nie „dorosły”), żeby nie mnożyć przycisków.
- Treść pod nagłówkiem rozwija się po kliknięciu „Najważniejsze informacje”.
- Dodanie artykułu do Wiedzy nie wysyła niczego na X.
