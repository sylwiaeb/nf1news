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
