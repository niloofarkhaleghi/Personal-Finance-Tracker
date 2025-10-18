# Personal Finance Tracker (Python · Pandas)

Ein interaktives Python-Tool zur Verwaltung persönlicher Finanzen.  
Ermöglicht das Erfassen, Analysieren und Visualisieren von Einnahmen und Ausgaben über CSV-Dateien.  
Ideal zum Lernen von **Pandas**, **Matplotlib** und **praktischer Datenanalyse**.

---

##  Funktionen

 **Neue Buchungen hinzufügen**  
- Eingabe von Datum, Betrag, Kategorie und Beschreibung  
- Automatische Erkennung von Einnahmen (positiv) und Ausgaben (negativ)

 **Analysefunktionen**  
- Zeitraumanalyse mit Gesamteinnahmen, Ausgaben und Nettoersparnis  
- Monatsweise Auswertung (`pandas.groupby()` + `sum()`)  
- Balkendiagramme und Verlaufskurven (`matplotlib`)

 **Kategorien & Erweiterungen**  
- Vordefinierte Kategorien (Miete, Lebensmittel, Shopping usw.)  
- Eigene Kategorien können leicht ergänzt werden

 **Export-Funktion**  
- Export als `.xlsx`-Datei (`pandas.to_excel`)  
- Optional: PDF-Bericht mit Diagrammen und Summen (z. B. über ReportLab)

---

## Technologien
- **Python 3.x**
- **Pandas** – Datenanalyse
- **Matplotlib** – Diagrammerstellung
- **OpenPyXL** – Excel-Export

---



##  Verwendung
python main.py

Dann über das Menü:
1️⃣ Neue Buchung hinzufügen
2️⃣ Buchungen im Datumsbereich anzeigen
3️⃣ Monatsanalyse anzeigen
4️⃣ Daten exportieren
5️⃣ Programm beenden


## Erweiterungen durch mich

Ich habe dieses Projekt auf Basis eines Tutorials weiterentwickelt und um folgende Funktionen erweitert:

Monats- & Kategorieauswertung
→ Gruppierung und Visualisierung mit pandas.groupby() und plot.bar()

Kategorisierungssystem erweitert
→ Eigene Kategorien definierbar (z. B. Freizeit, Energie, Reisen)

Exportfunktion für Excel & PDF
→ df.to_excel() und PDF-Bericht mit Diagrammen

Automatische Einnahme-/Ausgabenerkennung
→ Positive Beträge = Einnahme, negative = Ausgabe
→ Ideal für Bank-CSV-Datenübernahme


## Projektstruktur
<pre>
Personal Finance Tracker/
├── main.py
├── data_entry.py
├── finance_data.csv
├── requirements.txt
├── README.md

</pre>


## Lerneffekt

Dieses Projekt half mir, meine Kenntnisse in:

- Pandas (Gruppierungen, Aggregationen)

- Matplotlib (Diagrammerstellung)

- Dateiverwaltung in Python (CSV, Excel)

- Fehlerbehandlung und Benutzereingabe

zu vertiefen und praxisnah anzuwenden.


## Autorin

Niloofar Khaleghi
Masterstudentin – Ingenieurinformatik
Oktober 2025


## Credits & Inspiration

Das Grundkonzept dieses Projekts basiert auf einem Tutorial von 
<a href="https://www.youtube.com/@TechWithTim">Tech With Tim</a>


Ich habe das Projekt weiterentwickelt und erweitert um:

- Monats- und Kategorieauswertung (Data Analysis)

- Exportfunktionen (Excel/PDF)

- Automatische Einnahme-/Ausgabenerkennung

- Erweiterbares Kategoriesystem


## Installation

```bash
pip install -r requirements.txt