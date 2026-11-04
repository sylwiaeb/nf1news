---
layout: default
title: Interpelacja poselska
permalink: /interpelacja/
description: "Gotowa interpelacja poselska w sprawie opieki koordynowanej nad pacjentami z NF, krótka wiadomość do posłów i adresy posłów w podziale na kluby."
# Strona czeka na treść. Usuń tę linię, gdy będą plik, wiadomość i adresy.
published: false
---

# Interpelacja poselska

[Wstęp: o co prosimy posłów i dlaczego.]

## Krok 1. Pobierz interpelację

<!-- Plik wrzuć do pliki/ i popraw nazwę poniżej. -->
- [Pobierz interpelację (Word, .docx)]({{ '/pliki/interpelacja-NF.docx' | relative_url }})

## Krok 2. Skopiuj wiadomość

{% include mail.html id="wiadomosc-posel" body="wnioski/interpelacja-wiadomosc.txt" button="Kopiuj wiadomość" label="Treść wiadomości (pierwsza linia to temat maila)" note="Na końcu wpisz swoje imię i nazwisko w miejsce tekstu w nawiasach [ ]. Dołącz plik z interpelacją do maila." rows="10" %}

## Krok 3. Skopiuj adresy posłów

Możesz napisać do posłów jednego klubu albo do wszystkich naraz.

{% assign kluby = site.data.interpelacja.kluby %}
{% for k in kluby %}
### {{ k.klub }} ({{ k.adresy | size }})

<div class="mail-box">
<p class="mail"><button type="button" class="btn copy" data-target="adresy-{{ forloop.index }}">Kopiuj adresy</button></p>
<p class="copy-msg" role="status" aria-live="polite"></p>
<label for="adresy-{{ forloop.index }}">Adresy e-mail: {{ k.klub }}. Jeśli przycisk nie działa, przytrzymaj palec w polu, wybierz „Zaznacz wszystko”, a potem „Kopiuj”.</label>
<textarea id="adresy-{{ forloop.index }}" readonly rows="4">{{ k.adresy | join: ", " | escape }}</textarea>
</div>
{% endfor %}

{% if kluby.size > 1 %}
### Wszyscy posłowie

{% capture wszystkie %}{% for k in kluby %}{{ k.adresy | join: ", " }}{% unless forloop.last %}, {% endunless %}{% endfor %}{% endcapture %}
<div class="mail-box">
<p class="mail"><button type="button" class="btn copy" data-target="adresy-wszyscy">Kopiuj wszystkie adresy</button></p>
<p class="copy-msg" role="status" aria-live="polite"></p>
<label for="adresy-wszyscy">Adresy e-mail wszystkich posłów. Jeśli przycisk nie działa, przytrzymaj palec w polu, wybierz „Zaznacz wszystko”, a potem „Kopiuj”.</label>
<textarea id="adresy-wszyscy" readonly rows="5">{{ wszystkie | escape }}</textarea>
</div>
{% endif %}

## Krok 4. Wyślij

1. Otwórz nowy e-mail w swojej poczcie.
2. Wklej adresy w polu **UDW** (ukryte do wiadomości), a nie w polu „Do” ani „DW”. Wtedy posłowie nie widzą nawzajem swoich adresów, a Twój mail rzadziej trafia do spamu.
3. W polu „Do” wpisz swój własny adres.
4. Pierwszą linię wiadomości („Temat: …”) przenieś do tematu maila, a resztę wklej jako treść.
5. Dołącz plik z interpelacją, podpisz się i wyślij.
