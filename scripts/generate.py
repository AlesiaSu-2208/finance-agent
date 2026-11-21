"""Генерирует выдуманную выписку по карте за май–октябрь 2026 → data/statement.csv.

Персонаж (вымышленный): одинокая женщина 46 лет, переехала в Польшу (Варшава) из другой
страны, работает по найму, снимает кавалерку, учит польский, оформляет карту побыта,
каждый месяц отправляет деньги семье. Суммы в злотых (PLN).
Все магазины, суммы и операции вымышлены; номеров карт, счетов и имён нет."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "statement.csv"

START, END = date(2026, 5, 1), date(2026, 10, 31)

GROCERIES_BIG = [("Lidl", "Zakupy spożywcze na tydzień"), ("Biedronka", "Zakupy spożywcze"),
                 ("Auchan", "Duże zakupy spożywcze"), ("Carrefour", "Zakupy spożywcze")]
GROCERIES_SMALL = [("Żabka", "Drobne zakupy"), ("Biedronka", "Zakupy spożywcze"),
                   ("Warzywniak Pod Lipą", "Warzywa i owoce")]
COFFEE = [("Costa Coffee", "Kawa na wynos"), ("Starbucks", "Kawa"), ("Kawiarnia Ministerstwo", "Kawa i ciastko")]
DELIVERY = [("Pyszne.pl", "Dostawa jedzenia"), ("Wolt", "Dostawa jedzenia"), ("Uber Eats", "Dostawa jedzenia")]
RESTAURANTS = [("Restauracja Stary Dom", "Kolacja w restauracji"), ("Bar mleczny Prasowy", "Obiad"),
               ("Pizzeria Na Rogu", "Pizza ze znajomymi"), ("Sushi Zushi", "Sushi")]
TAXI = [("Bolt", "Przejazd"), ("Uber", "Przejazd")]
SHOPS = [("Allegro", "Zamówienie internetowe"), ("Allegro", "Artykuły do domu"),
         ("Zalando", "Odzież i obuwie"), ("Sinsay", "Odzież"), ("Pepco", "Artykuły do domu")]
BEAUTY = [("Rossmann", "Kosmetyki i chemia"), ("Hebe", "Kosmetyki")]
PHARMACY = [("Apteka Gemini", "Leki"), ("Apteka DOZ", "Leki i witaminy")]
CINEMA = [("Multikino", "Bilety do kina"), ("Cinema City", "Bilety do kina")]

rows = []


def add(d, amount, merchant, desc):
    rows.append((d.isoformat(), round(amount, 2), merchant, desc))


def rnd(a, b, step=1):
    return round(random.uniform(a, b) / step) * step + random.choice([0, 0.49, 0.99])


d = START
while d <= END:
    wd = d.weekday()
    m = d.month
    # Доход
    if d.day == 10:
        add(d, 9800, "Pracodawca", "Wynagrodzenie")
    if d == date(2026, 5, 20):
        add(d, 1180, "Urząd Skarbowy", "Zwrot podatku PIT")
    if d == date(2026, 7, 24):
        add(d, 1500, "Pracodawca", "Premia kwartalna")

    # Фиксированные ежемесячные платежи
    if d.day == 1:
        add(d, -3100, "Najem mieszkania", "Przelew za najem kawalerki")
    if d.day == 4 and m in (5, 7, 9):
        add(d, -round(random.uniform(170, 240), 2), "PGE Obrót", "Rachunek za prąd")
    if d.day == 3:
        add(d, -110, "ZTM Warszawa", "Bilet miesięczny 30-dniowy")
    if d.day == 5:
        add(d, -139, "LuxMed", "Abonament medyczny")
    if d.day == 6:
        add(d, -49.99, "Play", "Abonament telefoniczny")
    if d.day == 8:
        add(d, -69, "Orange Światłowód", "Internet domowy")
    if d.day == 12:
        add(d, -49, "Netflix", "Subskrypcja")
    if d.day == 15:
        add(d, -23.99, "Spotify", "Subskrypcja muzyczna")
    if d.day == 11:
        add(d, -rnd(450, 650, 10), "Wise", "Przelew do rodziny za granicę")
    if d.day == 14 and m in (5, 9):   # курс оплачивается за семестр (2 месяца)
        add(d, -960, "Szkoła językowa Polonus", "Kurs polskiego B1 — semestr")
    if d.day == 18:
        add(d, -260, "Studio Jogi Lotos", "Karnet na jogę")

    # Продукты: большая закупка по субботам, мелкие — 2–3 раза в неделю
    if wd == 5:
        merch, desc = random.choice(GROCERIES_BIG)
        add(d, -rnd(150, 290), merch, desc)
    if wd < 5 and random.random() < 0.5:
        merch, desc = random.choice(GROCERIES_SMALL)
        add(d, -rnd(15, 85), merch, desc)
    # Кофе по будням иногда
    if wd < 5 and random.random() < 0.3:
        merch, desc = random.choice(COFFEE)
        add(d, -rnd(14, 26), merch, desc)
    # Доставка — чаще в пятницу и выходные
    if random.random() < (0.22 if wd >= 4 else 0.04):
        merch, desc = random.choice(DELIVERY)
        add(d, -rnd(45, 95), merch, desc)
    if random.random() < 0.07:
        merch, desc = random.choice(RESTAURANTS)
        amt = (24, 36) if "Bar mleczny" in merch else (70, 190)
        add(d, -rnd(*amt), merch, desc)
    # Такси изредка
    if random.random() < 0.1:
        merch, desc = random.choice(TAXI)
        add(d, -rnd(18, 48), merch, desc)
    # Покупки
    if random.random() < 0.09:
        merch, desc = random.choice(SHOPS)
        add(d, -rnd(35, 320), merch, desc)
    # Уход и косметика
    if random.random() < 0.08:
        merch, desc = random.choice(BEAUTY)
        add(d, -rnd(25, 120), merch, desc)
    if random.random() < 0.05:
        merch, desc = random.choice(PHARMACY)
        add(d, -rnd(18, 90), merch, desc)
    # Кино по выходным
    if wd >= 4 and random.random() < 0.1:
        merch, desc = random.choice(CINEMA)
        add(d, -rnd(30, 38), merch, desc)
    d += timedelta(days=1)

# Регулярное, но не ежемесячное
for dd in (date(2026, 5, 16), date(2026, 6, 27), date(2026, 8, 8), date(2026, 9, 19), date(2026, 10, 31)):
    add(dd, -rnd(180, 250, 10), "Salon fryzjerski Nożyczki", "Fryzjer")

# Редкие и крупные траты
add(date(2026, 5, 9), -1340, "IKEA", "Meble i dodatki do mieszkania")
add(date(2026, 5, 22), -17, "Urząd Miasta", "Opłata skarbowa za pełnomocnictwo")
add(date(2026, 6, 9), -440, "Urząd Wojewódzki", "Opłata za kartę pobytu")
add(date(2026, 6, 16), -320, "Tłumacz przysięgły", "Tłumaczenie dokumentów")
add(date(2026, 6, 20), -140, "Teatr Polski", "Bilety do teatru")
add(date(2026, 7, 2), -1150, "Wizz Air", "Bilet lotniczy do domu i z powrotem")
add(date(2026, 7, 5), -1000, "Western Union", "Przelew dla mamy na leczenie")
add(date(2026, 7, 6), -420, "Allegro", "Prezenty dla rodziny")
add(date(2026, 8, 22), -220, "Torwar", "Bilet na koncert")
add(date(2026, 9, 9), -900, "Gabinet stomatologiczny Uśmiech", "Leczenie kanałowe")
add(date(2026, 9, 12), -520, "Booking.com", "Weekend w Gdańsku — nocleg")
add(date(2026, 9, 12), -99, "PKP Intercity", "Pociąg do Gdańska")
add(date(2026, 9, 14), -99, "PKP Intercity", "Pociąg z Gdańska")
add(date(2026, 10, 7), -600, "Szkoła językowa Polonus", "Egzamin certyfikatowy z polskiego B1")
add(date(2026, 10, 21), -3299, "Media Expert", "Laptop do pracy")
add(date(2026, 8, 3), 149.99, "Zalando", "Zwrot za towar")

rows.sort(key=lambda r: r[0])
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["date", "amount", "merchant", "description"])
    w.writerows(rows)
print(f"Записано {len(rows)} операций в {OUT}")
