---
layout: default
title: Interpelacja poselska
permalink: /interpelacja/
# Ukryta na czas poprawek interpelacji. Usuń tę linię i przywróć link w menu, żeby opublikować.
published: false
description: "Gotowa interpelacja poselska w sprawie opieki koordynowanej nad pacjentami z NF, krótka wiadomość do posłów i adresy posłów w podziale na kluby."
---

# Interpelacja poselska

Od 30 kwietnia 2026 r. 2 830 pacjentów z neurofibromatozami, którzy byli w pilotażu opieki koordynowanej, nie ma koordynatora ani stałego zespołu. Ministerstwo Zdrowia zakończyło prace nad stałym świadczeniem i odesłało ich do Ośrodków Eksperckich Chorób Rzadkich, choć ustawa o tych ośrodkach nie daje im ani zadania koordynacji, ani pieniędzy na nią.

**Interpelacja poselska** to pisemne pytanie posła do ministra. Minister musi na nie odpowiedzieć, a odpowiedź jest publikowana na stronie Sejmu. Przygotowaliśmy gotowy projekt interpelacji do Ministra Zdrowia. Prosimy: wyślij go do posłów, najlepiej z różnych klubów, i poproś o jej złożenie. Zajmie to kilka minut.

## Krok 1. Pobierz interpelację

- [Pobierz interpelację (Word, .docx)]({{ '/pliki/interpelacja-MZ-NF.docx' | relative_url }})
- [Pobierz interpelację (tekst, .txt)]({{ '/pliki/interpelacja-MZ-NF.txt' | relative_url }})

## Krok 2. Skopiuj wiadomość

{% include mail.html id="wiadomosc-posel" body="wnioski/interpelacja-wiadomosc.txt" button="Kopiuj wiadomość" label="Treść wiadomości (pierwsza linia to temat maila)" note="Na końcu wpisz swoje imię i nazwisko w miejsce tekstu w nawiasach [ ]. Dołącz plik z interpelacją do maila." rows="10" %}

## Krok 3. Skopiuj adresy posłów

Możesz napisać do posłów jednego klubu, kilku klubów albo do wszystkich naraz. Przy każdym adresie jest imię i nazwisko posła. Programy pocztowe rozpoznają taki zapis, więc całość możesz wkleić prosto w pole UDW. Lista pochodzi z oficjalnych danych Sejmu, stan na 4 listopada 2026 r.

{% assign kluby = site.data.interpelacja.kluby %}
{% if kluby.size > 1 %}
### Wszyscy posłowie

{% capture wszystkie %}{% for k in kluby %}{% for p in k.poslowie %}{{ p.imie }} <{{ p.email }}>{% unless forloop.last %}, {% endunless %}{% endfor %}{% unless forloop.last %}, {% endunless %}{% endfor %}{% endcapture %}
<div class="mail-box">
<p class="mail"><button type="button" class="btn copy" data-target="adresy-wszyscy">Kopiuj wszystkie adresy</button></p>
<p class="copy-msg" role="status" aria-live="polite"></p>
<label for="adresy-wszyscy">Adresy e-mail wszystkich posłów. Jeśli przycisk nie działa, przytrzymaj palec w polu, wybierz „Zaznacz wszystko”, a potem „Kopiuj”.</label>
<textarea id="adresy-wszyscy" readonly rows="5">{{ wszystkie | escape }}</textarea>
</div>
{% endif %}

{% for k in kluby %}
### {{ k.klub }} ({{ k.poslowie | size }})

<div class="mail-box">
<p class="mail"><button type="button" class="btn copy" data-target="adresy-{{ forloop.index }}">Kopiuj adresy</button></p>
<p class="copy-msg" role="status" aria-live="polite"></p>
<label for="adresy-{{ forloop.index }}">Adresy e-mail: {{ k.klub }}. Jeśli przycisk nie działa, przytrzymaj palec w polu, wybierz „Zaznacz wszystko”, a potem „Kopiuj”.</label>
<textarea id="adresy-{{ forloop.index }}" readonly rows="6">{% capture lista %}{% for p in k.poslowie %}{{ p.imie }} <{{ p.email }}>{% unless forloop.last %}, {% endunless %}{% endfor %}{% endcapture %}{{ lista | escape }}</textarea>
</div>
{% endfor %}



## Krok 4. Wyślij

1. Otwórz nowy e-mail w swojej poczcie.
2. Wklej adresy w polu **UDW** (ukryte do wiadomości), a nie w polu „Do” ani „DW”. Wtedy posłowie nie widzą nawzajem swoich adresów, a Twój mail rzadziej trafia do spamu.
3. W polu „Do” wpisz swój własny adres.
4. Część skrzynek pocztowych ogranicza liczbę odbiorców jednej wiadomości. Jeśli mail z wszystkimi adresami nie przejdzie, wyślij go osobno do każdego klubu.
5. Pierwszą linię wiadomości („Temat: …”) przenieś do tematu maila, a resztę wklej jako treść.
6. Dołącz plik z interpelacją, podpisz się i wyślij.
