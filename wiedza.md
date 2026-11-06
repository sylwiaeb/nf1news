---
layout: default
title: Wiedza
permalink: /wiedza/
description: Co nowego w leczeniu NF1. Wybrane interesujące artykuły o NF1, z linkiem do źródła.
---

# Wiedza

Co nowego w leczeniu NF1 na świecie. Zamieszczamy tu interesujące artykuły o NF1. Pełny tekst jest zawsze w źródle, pod linkiem.

<p class="source">To nie jest porada medyczna. O leczeniu decyduje lekarz prowadzący.</p>

<div class="szukaj">
  <input type="search" id="q" placeholder="Szukaj, np. selumetynib, ból, dorośli" aria-label="Szukaj w artykułach">
  <p class="tematy" id="tematy">{% assign wszystkie = site.wiedza | map: "tematy" | join: "," | split: "," | uniq | sort %}<button class="btn small on" data-t="">wszystkie</button>{% for t in wszystkie %}<button class="btn small" data-t="{{ t }}">{{ t }}</button>{% endfor %}</p>
  <p class="source" id="ile"></p>
</div>

{% assign artykuly = site.wiedza | sort: "data" | reverse %}
{% for a in artykuly %}
<section class="card wiedza" id="{{ a.slug }}" data-tematy="{{ a.tematy | join: '|' }}">
  <h3>{{ a.title }}</h3>
  <p class="to">{{ a.zrodlo }}, {{ a.data | date: "%-d.%m.%Y" }}{% if a.autor %}, autor: {{ a.autor }}{% endif %}{% if a.jezyk %}. Artykuł po {% if a.jezyk == "angielski" %}angielsku{% else %}{{ a.jezyk }}{% endif %}{% endif %}.</p>
  <p class="to">{% for t in a.tematy %}<span class="tag">{{ t }}</span>{% endfor %}</p>
  <p>{{ a.lead }}</p>
  <details>
    <summary>Najważniejsze informacje</summary>
    {{ a.content | markdownify }}
  </details>
  <p class="files"><a class="btn" href="{{ a.link }}">Przeczytaj artykuł w źródle{% if a.jezyk == "angielski" %} (po angielsku){% endif %} →</a></p>
</section>
{% endfor %}
<p id="brak" class="source" hidden>Nic nie znaleziono. Spróbuj innego słowa.</p>

<style>
.szukaj { margin: 1rem 0 1.5rem; font-family: system-ui, sans-serif; }
.szukaj input { width: 100%; font: 1rem system-ui, sans-serif; padding: 0.55rem 0.7rem; border: 1px solid #aaa; border-radius: 6px; background: transparent; color: inherit; }
.tematy { margin: 0.6rem 0 0; }
.tematy .btn.small { margin: 0 0.3rem 0.4rem 0; }
.tematy .btn.on { background: var(--c1); border-color: var(--c1); color: #fff; }
.tag { display: inline-block; margin: 0 0.3rem 0.2rem 0; padding: 0 0.45rem; border-radius: 3px; background: #eef1f5; color: #444; font-size: 0.78rem; }
@media (prefers-color-scheme: dark) { .tag { background: #2a2f36; color: #ccc; } .szukaj input { border-color: #555; } }
.wiedza details { margin: 0.4rem 0; }
.wiedza summary { cursor: pointer; font-family: system-ui, sans-serif; font-size: 0.9rem; color: var(--c1); }
</style>
<script>
(function () {
  var q = document.getElementById('q'), karty = [].slice.call(document.querySelectorAll('.card.wiedza')),
      przyciski = [].slice.call(document.querySelectorAll('#tematy button')), ile = document.getElementById('ile'),
      brak = document.getElementById('brak'), temat = '';
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l'); }
  karty.forEach(function (k) { k._t = norm(k.textContent); });
  function filtruj() {
    var slowa = norm(q.value).split(/\s+/).filter(Boolean), n = 0;
    karty.forEach(function (k) {
      var ok = (!temat || k.dataset.tematy.split('|').indexOf(temat) > -1) && slowa.every(function (w) { return k._t.indexOf(w) > -1; });
      k.hidden = !ok; if (ok) n++;
      if (ok && slowa.length) k.querySelector('details').open = true;
    });
    ile.textContent = (slowa.length || temat) ? 'Znaleziono: ' + n + ' z ' + karty.length : 'Artykułów: ' + karty.length;
    brak.hidden = n > 0;
  }
  q.addEventListener('input', filtruj);
  przyciski.forEach(function (b) { b.addEventListener('click', function () {
    temat = b.dataset.t; przyciski.forEach(function (x) { x.classList.toggle('on', x === b); }); filtruj();
  }); });
  var p = new URLSearchParams(location.search).get('q'); if (p) q.value = p;
  filtruj();
})();
</script>
