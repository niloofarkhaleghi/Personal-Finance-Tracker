import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    csv_file = "finance_data.csv"
    columns = ["date", "amount", "category", "description"]
    date_format = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Wenn die CSV nicht existiert, mit Header anlegen."""
        try:
            pd.read_csv(cls.csv_file, on_bad_lines='skip', encoding='utf-8')
        except FileNotFoundError:
            pd.DataFrame(columns=cls.columns).to_csv(cls.csv_file, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """Einen neuen Eintrag ans Ende der CSV anhängen."""
        neuer_eintrag = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writerow(neuer_eintrag)
        print("Eintrag wurde erfolgreich hinzugefügt!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Transaktionen im Datumsbereich filtern und Zusammenfassung ausgeben."""
        # 🩵 Fix 1: robustes Einlesen, keine Fehler bei kaputten Zeilen
        df = pd.read_csv(cls.csv_file, on_bad_lines='skip', encoding='utf-8')

        if df.empty:
            print("Keine Daten vorhanden.")
            return df

        # 🩵 Fix 2: fehlerhafte Daten still behandeln
        df["date"] = pd.to_datetime(df["date"], format=cls.date_format, dayfirst=True, errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

        # 🩵 Fix 3: englische Kategorien erkennen (nur zur Sicherheit)
        df["category"] = df["category"].replace({"Income": "Einnahme", "Expense": "Ausgabe"})

        start_dt = datetime.strptime(start_date, cls.date_format)
        end_dt = datetime.strptime(end_date, cls.date_format)

        maske = (df["date"] >= start_dt) & (df["date"] <= end_dt)
        gefiltert = df.loc[maske].dropna(subset=["date"]).sort_values("date")

        print(f"\nBuchungen von {start_dt.strftime(cls.date_format)} bis {end_dt.strftime(cls.date_format)}")
        if gefiltert.empty:
            print("Keine Buchungen gefunden.")
            print("\nZusammenfassung:")
            print("Gesamteinnahmen:  0,00 €")
            print("Gesamtausgaben:   0,00 €")
            print("Nettoersparnis:   0,00 €")
            return gefiltert

        print(gefiltert.to_string(
            index=False,
            formatters={"date": lambda x: x.strftime(cls.date_format)}
        ))

        # Summen berechnen
        gesamt_einnahmen = gefiltert.loc[gefiltert["category"] == "Einnahme", "amount"].sum()
        gesamt_ausgaben = gefiltert.loc[gefiltert["category"] == "Ausgabe", "amount"].sum()
        netto = gesamt_einnahmen - gesamt_ausgaben

        print("\nZusammenfassung:")
        print(f"Gesamteinnahmen:  {gesamt_einnahmen:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
        print(f"Gesamtausgaben:   {gesamt_ausgaben:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
        print(f"Nettoersparnis:   {netto:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
        return gefiltert


def add():
    """Neue Buchung hinzufügen."""
    CSV.initialize_csv()
    datum = get_date("Datum der Buchung eingeben (dd-mm-yyyy) oder Enter für heutiges Datum: ", allow_default=True)
    betrag = get_amount()
    kategorie = get_category(betrag)
    beschreibung = get_description()
    CSV.add_entry(datum, betrag, kategorie, beschreibung)


def plot_transactions(df):


    """Diagramm für Einnahmen und Ausgaben anzeigen."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")
    if df.empty:
        print("Keine Daten zum Plotten vorhanden.")
        return

    # Kategorien vereinheitlichen
    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .replace({
            "Income": "Einnahme",
            "Einnahmen": "Einnahme",
            "Expense": "Ausgabe",
            "Ausgaben": "Ausgabe"
        })
    )

    # Gruppieren und aufsummieren pro Datum (sauberere Linien)
    df_einnahmen = (
        df[df["category"] == "Einnahme"]
        .groupby("date")["amount"]
        .sum()
        .cumsum()
        .reset_index()
    )
    df_ausgaben = (
        df[df["category"] == "Ausgabe"]
        .groupby("date")["amount"]
        .sum()
        .cumsum()
        .reset_index()
    )

    # Plot
    plt.figure(figsize=(10, 5))
    if not df_einnahmen.empty:
        plt.plot(df_einnahmen["date"], df_einnahmen["amount"], "o-", label="Einnahmen (kumulativ)", color="green")
    if not df_ausgaben.empty:
        plt.plot(df_ausgaben["date"], df_ausgaben["amount"], "o-", label="Ausgaben (kumulativ)", color="red")

    plt.title("Kumulierte Einnahmen und Ausgaben über die Zeit")
    plt.xlabel("Datum")
    plt.ylabel("Betrag (€)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()


def analyze_by_month():
    """Monatsanalyse (Einnahmen und Ausgaben pro Monat)."""
    # 🩵 Fix 4: robustes Einlesen
    df = pd.read_csv(CSV.csv_file, on_bad_lines='skip', encoding='utf-8')
    if df.empty:
        print("Keine Daten vorhanden.")
        return

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["category"] = df["category"].replace({"Income": "Einnahme", "Expense": "Ausgabe"})
    df["Monat"] = df["date"].dt.to_period("M")

    summary = df.groupby(["Monat", "category"])["amount"].sum().unstack(fill_value=0)
    print("\nEinnahmen/Ausgaben pro Monat:\n")
    print(summary)

    summary.plot(kind="bar", title="Einnahmen vs. Ausgaben pro Monat")
    plt.xlabel("Monat")
    plt.ylabel("Betrag (€)")
    plt.tight_layout()
    plt.show()


def export_to_excel():
    """Exportiert alle Daten als Excel-Datei."""
    df = pd.read_csv(CSV.csv_file, on_bad_lines='skip', encoding='utf-8')
    if df.empty:
        print("Keine Daten zum Exportieren vorhanden.")
        return
    df.to_excel("finanzbericht.xlsx", index=False)
    print("Datei 'finanzbericht.xlsx' wurde erfolgreich exportiert!")


def main():
    while True:
        print("\n===== Finanzmanager Menü =====")
        print("1. Neue Buchung hinzufügen")
        print("2. Buchungen und Zusammenfassung im Datumsbereich anzeigen")
        print("3. Monatsanalyse anzeigen")
        print("4. Daten nach Excel exportieren")
        print("5. Beenden")

        try:
            wahl = input("Bitte Auswahl eingeben (1–5): ").strip()
        except EOFError:
            print("\nKeine Eingabe verfügbar. Programm wird beendet...")
            break

        if wahl == "1":
            add()
        elif wahl == "2":
            start_date = get_date("Startdatum eingeben (dd-mm-yyyy): ")
            end_date = get_date("Enddatum eingeben (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty and input("Diagramm anzeigen? [j/N] ").strip().lower() == "j":
                plot_transactions(df)
        elif wahl == "3":
            analyze_by_month()
        elif wahl == "4":
            export_to_excel()
        elif wahl == "5":
            print("Programm wird beendet...")
            break
        else:
            print("Ungültige Auswahl! Bitte 1 bis 5 eingeben.")


if __name__ == "__main__":
    main()
