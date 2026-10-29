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
