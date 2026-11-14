// Wspólny zapis „wysłane” dla strony /napisz-do-posla/ (Cloudflare Worker + KV).
// Instrukcja: narzedzia/WYSLANE-CLOUDFLARE.md
// Wymaga: KV namespace podpiętego jako WYSLANE, zmienna ADMIN_TOKEN (sekret).
const ORIGIN = 'https://nf1news.pl';
const MAX_ID = 1000;          // id posłów z api.sejm.gov.pl są mniejsze
const LIMIT_IP_DZIEN = 10;    // ile zaznaczeń dziennie z jednego adresu IP

const cors = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'X-Token',
};
const json = (d, status = 200) => new Response(JSON.stringify(d), { status, headers: { ...cors, 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

export default {
  async fetch(req, env) {
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    const url = new URL(req.url);
    const m = url.pathname.match(/^\/wyslane(?:\/(\d+))?$/);
    if (!m) return json({ blad: 'nie ma' }, 404);

    if (req.method === 'GET' && !m[1]) {
      const out = {};
      let cursor;
      do {
        const r = await env.WYSLANE.list({ prefix: 'w:', cursor });
        for (const k of r.keys) out[k.name.slice(2)] = (k.metadata && k.metadata.d) || '1';
        cursor = r.list_complete ? null : r.cursor;
      } while (cursor);
      return json(out);
    }

    const id = Number(m[1]);
    if (!id || id > MAX_ID) return json({ blad: 'zły numer' }, 400);
    const key = 'w:' + id;
    const token = req.headers.get('X-Token') || '';
    const admin = env.ADMIN_TOKEN && token === env.ADMIN_TOKEN;

    if (req.method === 'POST') {
      const istnieje = await env.WYSLANE.get(key);
      if (istnieje) return json({ juz: true }, 409);
      const ip = req.headers.get('CF-Connecting-IP') || '?';
      const dzis = new Date().toISOString().slice(0, 10);
      // Adres IP nie jest zapisywany: tylko jego skrót, kasowany po 2 dniach.
      const skrot = [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(dzis + ip)))].slice(0, 8).map(b => b.toString(16).padStart(2, '0')).join('');
      const limKey = 'ip:' + dzis + ':' + skrot;
      const ile = Number(await env.WYSLANE.get(limKey)) || 0;
      if (!admin && ile >= LIMIT_IP_DZIEN) return json({ blad: 'limit' }, 429);
      await env.WYSLANE.put(limKey, String(ile + 1), { expirationTtl: 172800 });
      const nowy = crypto.randomUUID();
      await env.WYSLANE.put(key, nowy, { metadata: { d: dzis } });
      return json({ token: nowy });
    }

    if (req.method === 'DELETE') {
      const zapisany = await env.WYSLANE.get(key);
      if (!zapisany) return json({ ok: true });
      if (!admin && token !== zapisany) return json({ blad: 'brak uprawnień' }, 403);
      await env.WYSLANE.delete(key);
      return json({ ok: true });
    }
    return json({ blad: 'metoda' }, 405);
  },
};
