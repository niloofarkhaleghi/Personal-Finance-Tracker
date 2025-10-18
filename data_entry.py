from datetime import datetime

DATE_FMT = "%d-%m-%Y"
KATEGORIEN = {
    "E": "Einnahme",
    "A": "Ausgabe",
    "L": "Lebensmittel",
    "M": "Miete",
    "S": "Shopping",
    "T": "Transport"
}


def get_date(prompt, allow_default=False):
    """Fragt ein Datum ab und prüft das Format."""
    while True:
        s = input(prompt).strip()
        if allow_default and not s:
            return datetime.today().strftime(DATE_FMT)
        try:
            return datetime.strptime(s, DATE_FMT).strftime(DATE_FMT)
        except ValueError:
            print("❌ Ungültiges Datum. Bitte im Format dd-mm-yyyy eingeben.")


def get_amount():
    """Fragt einen Betrag ab und prüft, ob er gültig ist."""
    while True:
        s = input("Betrag eingeben (z. B. 45 oder -20): ").strip()
        try:
            betrag = float(s)
            if betrag == 0:
                print("❌ Der Betrag darf nicht 0 sein.")
                continue
            return betrag
        except ValueError:
            print("❌ Bitte eine gültige Zahl eingeben, z. B. 12.50")


def get_category(betrag=None):
    """Automatische Kategorie, falls Betrag negativ oder positiv."""
    if betrag is not None:
        if betrag < 0:
            return "Ausgabe"
        elif betrag > 0:
            return "Einnahme"

    while True:
        kat = input(
            "Kategorie eingeben ('E'=Einnahme, 'A'=Ausgabe, 'L'=Lebensmittel, "
            "'M'=Miete, 'S'=Shopping, 'T'=Transport): "
        ).strip().upper()
        if kat in KATEGORIEN:
            return KATEGORIEN[kat]
        print("❌ Ungültige Eingabe. Bitte 'E', 'A', 'L', 'M', 'S' oder 'T' eingeben.")


def get_description():
    """Fragt eine optionale Beschreibung ab."""
    return input("Beschreibung eingeben (optional): ").strip()
