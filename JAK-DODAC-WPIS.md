# Jak dodać nowy wpis

1. Utwórz plik w folderze `_posts/` o nazwie `RRRR-MM-DD-krotki-tytul.md`, np. `_posts/2026-11-05-spotkanie-w-ministerstwie.md`.
2. Na początku pliku wpisz nagłówek:

   ```
   ---
   title: "Spotkanie w Ministerstwie"
   ---
   ```

3. Pod nagłówkiem napisz treść. Pusta linia oddziela akapity. Link: `[tekst](https://adres)`. Pogrubienie: `**tekst**`.
4. Opublikuj:

   ```
   git add _posts
   git commit -m "Nowy wpis"
   git push
   ```

Strona zaktualizuje się po 1–2 minutach.
