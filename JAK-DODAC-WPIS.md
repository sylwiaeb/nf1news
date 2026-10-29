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
