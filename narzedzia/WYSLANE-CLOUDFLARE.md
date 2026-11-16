# Wspólny zapis „wysłane” (Cloudflare)

Strona /napisz-do-posla/ działa bez tego, ale wtedy zaznaczenia widzi tylko osoba, która je zrobiła.
Ze wspólnym zapisem każdy widzi, do kogo już wysłano.

1. Załóż darmowe konto na dash.cloudflare.com (neutralny e-mail).
2. Workers & Pages → KV → Create namespace, nazwa: `nf1news-wyslane`.
3. Workers & Pages → Create → Worker, nazwa np. `wyslane`. Edit code → wklej `wyslane-worker.js` → Deploy.
4. Ustawienia workera → Bindings → KV namespace: nazwa zmiennej `WYSLANE`, namespace `nf1news-wyslane`.
5. Ustawienia → Variables and Secrets → Secret `ADMIN_TOKEN` (długie, losowe hasło; pozwala cofać dowolne zaznaczenia).
6. Adres workera (np. https://wyslane.<konto>.workers.dev) wpisz w `napisz-do-posla.html` w `var ZAPIS = '';`.

Cofnięcie zaznaczenia (admin): `curl -X DELETE -H "X-Token: <ADMIN_TOKEN>" https://wyslane.<konto>.workers.dev/wyslane/<id posła>`
Lista wszystkich zaznaczeń: otwórz https://wyslane.<konto>.workers.dev/wyslane

## Tryb administratora na stronie
Otwórz https://nf1news.pl/napisz-do-posla/#admin i wpisz ADMIN_TOKEN w polu „Hasło administratora”.
Hasło zostaje tylko w tej przeglądarce. W tym trybie nie ma dziennego limitu i można odznaczyć każdego posła.
