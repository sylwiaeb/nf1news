"""Codzienny post na X z licznikiem: ile dni pacjenci z NF są bez
opieki medycznej i ile dni minęło od decyzji Ministerstwa Zdrowia
o zakończeniu prac.

Liczy tak samo jak strona czekamy.nf1news.pl (pełne dni, czas polski).
Treść zmienia się dzień po dniu (kilka wersji po kolei), żeby X nie uznał
postów za powtarzany spam. @MZ_GOV_PL jest oznaczane tylko w poniedziałki
i w dni okrągłe (co 50 dni, rocznice miesięczne), nie codziennie.
Do posta dołącza grafikę z licznikiem (narzedzia/grafika.mjs, układ
„licznik”), a link do strony z licznikiem idzie w pierwszym komentarzu.

Użycie:
  python .github/scripts/x_licznik.py            # wysyła na X
  python .github/scripts/x_licznik.py --proba    # tylko pokazuje tekst i robi grafikę
  python .github/scripts/x_licznik.py --proba --dzien 2026-11-12
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Warsaw")
KONIEC_PILOTAZU = datetime(2026, 5, 1, tzinfo=TZ)   # pilotaż skończył się 30.04.2026
PISMO_MZ = datetime(2026, 10, 23, tzinfo=TZ)        # pismo MZ „zakończono dalsze prace”
LINK = "https://czekamy.nf1news.pl/"
GRAFIKI = "licznik-grafiki"


def dni(od, teraz):
    return max(0, int((teraz - od).total_seconds() // 86400))


def odm(n, jeden, kilka, wiele):
    if n == 1:
        return jeden
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return kilka
    return wiele


def dni_slowo(n):
    return "dzień" if n == 1 else "dni"


def miesiace_od_pilotazu(d):
    """Liczba pełnych miesięcy, jeśli dziś jest rocznica miesięczna (30. dzień, w lutym ostatni)."""
    ostatni = (date(d.year + (d.month == 12), d.month % 12 + 1, 1) - timedelta(days=1)).day
    if d.day != min(30, ostatni):
        return 0
    return (d.year - 2026) * 12 + d.month - 4


def tresc(d1, d2, dzien):
    """Tekst posta na dany dzień. d1: dni bez opieki, d2: dni od decyzji MZ o zakończeniu prac."""
    t1 = f"{d1} {dni_slowo(d1)}"
    t2 = f"{d2} {dni_slowo(d2)}"
    tyg = d1 // 7
    m = miesiace_od_pilotazu(dzien)
    okragly = d1 % 50 == 0 or m > 0
    oznacz = okragly or dzien.weekday() == 0
    mz = "@MZ_GOV_PL" if oznacz else "Ministerstwo Zdrowia"
    mz_dop = "@MZ_GOV_PL" if oznacz else "Ministerstwa Zdrowia"

    if m > 0:
        tekst = (f"Dziś mija {m} {odm(m, 'miesiąc', 'miesiące', 'miesięcy')} od końca pilotażu "
                 f"koordynowanej opieki nad pacjentami z NF. {t1} bez opieki medycznej.\n\n"
                 f"{mz} od {t2} milczy w sprawie tego, kto i kiedy zapewni pacjentom opiekę.")
    elif d1 % 50 == 0:
        tekst = (f"{d1}. dzień bez opieki medycznej dla pacjentów z NF.\n\n"
                 f"Od {t2} {mz} milczy. Pani Minister Zdrowia, Panie Ministrze, "
                 f"pacjenci czekają na zmianę decyzji i na dialog.")
    else:
        wersje = [
            f"Licznik NF, dzień {d1}.\n\n"
            f"{t1} pacjenci z NF są bez opieki medycznej.\n"
            f"Od {t2} {mz} milczy.",

            f"{t1} bez opieki medycznej. Tyle trwa to dla pacjentów z neurofibromatozą "
            f"od końca pilotażu 30 kwietnia 2026 r.\n\n"
            f"{mz} od {t2} nie mówi, kto i kiedy zapewni im opiekę.",

            f"Pani Minister Zdrowia, Panie Ministrze,\n"
            f"pacjenci z NF czekają już {t1} na opiekę medyczną.\n\n"
            f"Od decyzji {mz_dop} o zakończeniu prac minęło {t2}. Pacjenci czekają na dialog.",

            f"Dziś {d1}. dzień, odkąd pacjenci z NF nie mają opieki medycznej. "
            f"To {tyg} {odm(tyg, 'tydzień', 'tygodnie', 'tygodni')}.\n\n"
            f"I {t2} milczenia {mz_dop} od decyzji o zakończeniu prac.",

            f"Neurofibromatoza to choroba na całe życie. Opieka wymaga wielu specjalistów, "
            f"którzy działają razem.\n\n"
            f"Od {t1} pacjenci z NF nie mają opieki medycznej. "
            f"{mz} milczy od {t2}.",

            f"{d2} {dni_slowo(d2)} temu {mz} zdecydowało o zakończeniu prac. "
            f"Od tamtej pory milczy.\n\n"
            f"Pacjenci z NF są bez opieki medycznej już {t1}.",

            f"Pilotaż koordynowanej opieki dla 2 830 pacjentów z NF skończył się 30 kwietnia 2026 r.\n\n"
            f"Dziś: {t1} bez opieki medycznej, {t2} milczenia {mz_dop}.",
        ]
        tekst = wersje[d1 % len(wersje)]

    tagi = [["#NF1", "#neurofibromatoza"], ["#NF1", "#ChorobyRzadkie"],
            ["#neurofibromatoza", "#ChorobyRzadkie"], ["#NF1", "#neurofibromatoza", "#ChorobyRzadkie"]]
    return f"{tekst}\n\n{' '.join(tagi[d1 % len(tagi)])}"


def grafika(d1, d2, dzien, folder):
    nazwa = f"licznik-{dzien.isoformat()}"
    spec = {
        "uklad": "licznik",
        "motyw": "ciemny",
        "kolor": "#d32f2f",
        "etykieta": f"Pacjenci z NF czekają · {dzien.day}.{dzien.month:02d}.{dzien.year}",
        "liczba": str(d1),
        "jednostka": dni_slowo(d1),
        "opis": "==bez opieki medycznej== od końca pilotażu 30.04.2026",
        "drugi": {"liczba": str(d2),
                  "opis": f"{dni_slowo(d2)} ==milczenia Ministerstwa Zdrowia==\nod decyzji o zakończeniu prac 23.10.2026"},
        "pytanie": "Pani Minister Zdrowia, Panie Ministrze, pacjenci czekają na dialog.",
        "domena": "czekamy.nf1news.pl",
    }
    os.makedirs(folder, exist_ok=True)
    plik = os.path.join(folder, f"{nazwa}.json")
    json.dump(spec, open(plik, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run(["node", "narzedzia/grafika.mjs", plik, folder], check=True)
    alt = (f"Licznik, {dzien.day}.{dzien.month:02d}.{dzien.year}: {d1} {dni_slowo(d1)} bez opieki "
           f"medycznej dla pacjentów z NF od końca pilotażu 30 kwietnia 2026 r. {d2} {dni_slowo(d2)} milczenia "
           f"Ministerstwa Zdrowia od decyzji o zakończeniu prac 23 października 2026 r. Pani Minister Zdrowia, Panie Ministrze, "
           f"pacjenci czekają na dialog.")
    return os.path.join(folder, f"{nazwa}-kwadrat.png"), alt


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--proba", action="store_true", help="nie wysyła, tylko pokazuje")
    a.add_argument("--dzien", help="RRRR-MM-DD, domyślnie dziś (czas polski)")
    a.add_argument("--bez-grafiki", action="store_true")
    args = a.parse_args()

    teraz = datetime.now(TZ)
    if args.dzien:
        teraz = datetime.combine(date.fromisoformat(args.dzien), time(8, 0), TZ)
    d1, d2 = dni(KONIEC_PILOTAZU, teraz), dni(PISMO_MZ, teraz)
    tekst = tresc(d1, d2, teraz.date())
    print(f"--- {teraz:%Y-%m-%d} ({len(tekst)} znaków) ---\n{tekst}\n--- komentarz ---\n{LINK}")
    if len(tekst) > 280:
        print("Tekst za długi dla X.")
        sys.exit(1)

    obraz, alt = (None, None) if args.bez_grafiki else grafika(d1, d2, teraz.date(), GRAFIKI)
    if args.proba:
        return

    import requests
    from requests_oauthlib import OAuth1
    sys.path.insert(0, os.path.dirname(__file__))
    from x_post import upload_image

    keys = [os.environ.get(k) for k in
            ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")]
    if not all(keys):
        print("Brak kluczy X w sekretach repozytorium.")
        sys.exit(1)
    auth = OAuth1(*keys)
    payload = {"text": tekst}
    if obraz:
        media_id = upload_image(obraz, alt, auth)
        if media_id:
            payload["media"] = {"media_ids": [str(media_id)]}
    r = requests.post("https://api.x.com/2/tweets", json=payload, auth=auth, timeout=30)
    print(f"post: {r.status_code} {r.text}")
    if r.status_code >= 300:
        sys.exit(1)
    tweet_id = r.json()["data"]["id"]
    r = requests.post("https://api.x.com/2/tweets", auth=auth, timeout=30, json={
        "text": LINK, "reply": {"in_reply_to_tweet_id": tweet_id}})
    print(f"link w komentarzu: {r.status_code} {r.text}")
    sys.exit(0 if r.status_code < 300 else 1)


if __name__ == "__main__":
    main()
