// Robi grafiki do wpisu: 1200x630 (podgląd linku na FB/X) i 1080x1080 (post na X i zdjęcie na FB).
//
// Użycie:  node narzedzia/grafika.mjs grafiki/2026-11-06-lekarze-mowili-gotowi.json
// Wynik:   assets/grafiki/2026-11-06-lekarze-mowili-gotowi.png
//          assets/grafiki/2026-11-06-lekarze-mowili-gotowi-kwadrat.png
//
// Opis pól pliku .json: JAK-DODAC-WPIS.md, sekcja „Grafika do wpisu”.
// Potrzebny Node i Playwright z Chromium (są w środowisku Claude).
import { readFileSync, mkdirSync } from "node:fs";
import { basename, join } from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");

const specPath = process.argv[2];
if (!specPath) {
  console.error("Podaj plik z opisem grafiki, np. grafiki/2026-11-06-tytul.json");
  process.exit(1);
}
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const name = basename(specPath, ".json");
const outDir = process.argv[3] || "assets/grafiki";
mkdirSync(outDir, { recursive: true });

const esc = (s = "") => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// ==tekst== to żółte wyróżnienie
// pojedyncze litery (w, z, i, a…) nie zostają na końcu linii
const fmt = (s = "") => esc(s)
  .replace(/(^|[\s(„])([aiouwzAIOUWZ]) /g, "$1$2\u00a0")
  .replace(/==(.+?)==/g, "<mark>$1</mark>").replace(/\n/g, "<br>");

const THEMES = {
  jasny: { bg: "#ffffff", fg: "#1a1a1a", muted: "#555555", mark: "#ffe17a", markFg: "#000",
           zielony: "#1b9e70", czerwony: "#e04848", niebieski: "#2a78d6", pomaranczowy: "#e0632e", szary: "#888" },
  ciemny: { bg: "#161616", fg: "#f2f2f2", muted: "#b0b0b0", mark: "#ffd43b", markFg: "#000",
            zielony: "#2fc48d", czerwony: "#ff6b6b", niebieski: "#5aa2f0", pomaranczowy: "#ff8a4c", szary: "#999" },
};
const t = THEMES[spec.motyw || "jasny"];
const color = (c) => t[c] || c || t.niebieski;

function body() {
  const u = spec.uklad || "naglowek";
  if (u === "zestawienie") {
    return (spec.elementy || []).map((e) => `
      <div class="blok" style="--k:${color(e.kolor)}">
        ${e.etykieta ? `<div class="etykieta">${fmt(e.etykieta)}</div>` : ""}
        <div class="duzy">${fmt(e.tekst)}</div>
        ${e.podpis ? `<div class="podpis">${fmt(e.podpis)}</div>` : ""}
      </div>`).join("");
  }
  if (u === "liczby") {
    return `${spec.etykieta ? `<div class="etykieta" style="color:${color(spec.kolor)}">${fmt(spec.etykieta)}</div>` : ""}
      ${spec.tekst ? `<div class="sredni">${fmt(spec.tekst)}</div>` : ""}
      <div class="liczby" style="grid-template-columns:repeat(${(spec.liczby || []).length},1fr)">${(spec.liczby || []).map((l) => `
        <div class="liczba" style="--k:${color(l.kolor)}"><div class="l">${fmt(l.liczba)}</div><div class="podpis">${fmt(l.opis)}</div></div>`).join("")}
      </div>`;
  }
  if (u === "licznik") {
    // duża liczba w stylu zegara klapkowego (jak na stronie czekamy.nf1news.pl) i opcjonalnie druga, mniejsza
    const karty = (n) => String(n).split("").map((z) => `<span class="karta">${esc(z)}</span>`).join("");
    const d = spec.drugi;
    return `${spec.etykieta ? `<div class="pasek" style="background:${color(spec.kolor)}">${fmt(spec.etykieta)}</div>` : ""}
      <div class="licznik">
        <div class="klapki">${karty(spec.liczba)}</div>
        <div class="jedn">${fmt(spec.jednostka || "dni")}</div>
        ${spec.opis ? `<div class="opis">${fmt(spec.opis)}</div>` : ""}
      </div>
      ${d ? `<div class="drugi"><div class="klapki male" style="--kb:${color(d.kolor || spec.kolor)}">${karty(d.liczba)}</div><div class="opis">${fmt(d.opis)}</div></div>` : ""}`;
  }
  // cytat i naglowek: jeden duży tekst z kreską z boku
  return `<div class="blok" style="--k:${color(spec.kolor)}">
      ${spec.etykieta ? `<div class="etykieta">${fmt(spec.etykieta)}</div>` : ""}
      <div class="duzy">${fmt(spec.tekst)}</div>
      ${spec.podpis ? `<div class="podpis">${fmt(spec.podpis)}</div>` : ""}
    </div>`;
}

function html(w, h) {
  const pad = w > 1100 && h < 700 ? 72 : 80;
  return `<!doctype html><html lang="pl"><head><meta charset="utf-8"><style>
    * { box-sizing: border-box; margin: 0; }
    html, body { width: ${w}px; height: ${h}px; background: ${t.bg}; color: ${t.fg}; }
    body { padding: ${pad}px; display: flex; flex-direction: column; font-family: Inter, sans-serif; }
    main { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 1.1em; overflow: hidden; font-size: 60px; }
    .blok { border-left: 11px solid var(--k); padding-left: 28px; }
    .etykieta { font-size: max(0.38em, 22px); font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--k); margin-bottom: 0.15em; }
    .duzy { font-family: "DejaVu Serif", Georgia, serif; font-weight: 700; line-height: 1.17; letter-spacing: -0.01em; }
    .sredni { font-family: "DejaVu Serif", Georgia, serif; font-weight: 700; font-size: 0.7em; line-height: 1.2; }
    .podpis { font-size: max(0.36em, 21px); color: ${t.muted}; margin-top: 0.35em; line-height: 1.3; }
    mark { background: ${t.mark}; color: ${t.markFg}; padding: 0 0.12em; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
    .liczby { display: grid; gap: 0.7em; }
    .liczba { border-top: 9px solid var(--k); padding-top: 0.25em; }
    .liczba .l { font-family: "DejaVu Serif", Georgia, serif; font-weight: 700; font-size: 1.25em; line-height: 1.1; white-space: nowrap; }
    .licznik { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 0.15em 0.3em; }
    .pasek { align-self: flex-start; color: #fff; font-weight: 800; font-size: max(0.42em, 24px); letter-spacing: 0.05em; text-transform: uppercase; padding: 0.3em 0.6em; border-radius: 0.2em; }
    .klapki { display: inline-flex; gap: 0.07em; font-family: "DejaVu Sans", Inter, sans-serif; font-weight: 800; font-size: 3em; line-height: 1; font-variant-numeric: tabular-nums; }
    .klapki.male { font-size: 1.15em; }
    .klapki.male .karta { background: var(--kb); box-shadow: none; }
    .karta { position: relative; display: inline-block; width: 0.8em; height: 1.2em; line-height: 1.2em; text-align: center; color: #f4f4f4;
             border-radius: 0.09em; background: linear-gradient(#262626 0 50%, #2c2c2c 50% 100%); box-shadow: 0 0 0 1px #3a3a3a, 0 0.04em 0.08em rgba(0,0,0,.35); }
    .karta::after { content: ""; position: absolute; left: 0; right: 0; top: 50%; height: max(0.025em, 2px); margin-top: -1px; background: ${t.bg}; }
    .licznik .jedn { font-family: "DejaVu Serif", Georgia, serif; font-weight: 700; font-size: 1.1em; padding-bottom: 0.1em; }
    .licznik .opis { flex-basis: 100%; font-family: "DejaVu Serif", Georgia, serif; font-weight: 700; font-size: 0.62em; line-height: 1.2; margin-top: 0.15em; }
    .drugi { display: flex; align-items: center; gap: 0.45em; border-top: 2px solid ${t.muted}55; padding-top: 0.6em; }
    .drugi .opis { font-family: "DejaVu Serif", Georgia, serif; font-weight: 700; font-size: 0.5em; line-height: 1.2; }
    footer { display: flex; justify-content: space-between; align-items: flex-end; gap: 40px; margin-top: 36px; font-weight: 700; }
    footer .pytanie { font-size: 30px; line-height: 1.25; }
    footer .domena { font-size: 25px; white-space: nowrap; }
  </style></head><body>
    <main id="m">${body()}</main>
    <footer><div class="pytanie">${fmt(spec.pytanie || "")}</div><div class="domena">${esc(spec.domena || "nf1news.pl")}</div></footer>
    <script>
      // Zmniejsza czcionkę, aż wszystko się zmieści.
      const m = document.getElementById("m");
      let s = ${spec.rozmiar || (h > w * 0.8 ? 82 : 72)};
      m.style.fontSize = s + "px";
      while ((m.scrollHeight > m.clientHeight + 1 || m.scrollWidth > m.clientWidth + 1) && s > 26) { s -= 2; m.style.fontSize = s + "px"; }
    </script>
  </body></html>`;
}

const browser = await chromium.launch();
for (const [w, h, suffix] of [[1200, 630, ""], [1080, 1080, "-kwadrat"]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await page.setContent(html(w, h));
  await page.waitForTimeout(150);
  const out = join(outDir, `${name}${suffix}.png`);
  await page.screenshot({ path: out });
  console.log(out);
  await page.close();
}
await browser.close();
