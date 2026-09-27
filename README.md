# Order Report System (Refactored)

Ett refaktorerat Python-paket för e-handelsorderrapportering. Systemet läser in orderdata från CSV-filer, validerar datastrukturen, tvättar och beräknar nyckeltal (t.ex. försäljningsvärde efter rabatt och returgrad) samt genererar strukturerade rapporter.

---

## Beroenden

* **Python 3.13+**
* **Pandas** (för databehandling och aggregering)
* **pytest** (för automatiserad testning)
* **Standardbibliotek:** `pathlib`, `logging`, `dataclasses`

---

## Installation & Förberedelser

1. **Klona repositoryt** och navigera till projektmappen:
   ```bash
   cd order_report_project
   ```

2. **Skapa och aktivera en virtuell miljö:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Linux/Git Bash
   # eller .venv\Scripts\activate på Windows CMD
   ```

3. **Installera paketet i editable mode (`-e`):**
   ```bash
   pip install -e .
   ```

---

## Hur programmet körs

Skriptet körs som en modul direkt via Python från rotmappen:

```bash
python -m order_report
```

Detta exekverar pipeline-flödet i `order_report/__main__.py`:
1. Konfigurerar loggning till `logs/order_report.log`.
2. Läser in rådata från `data/orders.csv`.
3. Validerar och tvättar datan i memory.
4. Genererar rapporter och sparar resultaten som CSV-filer i `data_output/`.

---

## Hur testerna körs

Kör testsviten via `pytest`:

```bash
pytest
```

För utförlig utskrift under körning:
```bash
pytest -v
```

---

## Projektstruktur

```text
order_report_project/
├── data/                  # Inkommande rådata (orders.csv)
├── data_output/           # Genererade CSV-rapporter
├── logs/                  # Loggfiler från körningar
├── notebooks/             # Notebooks för tester och verifiering
│   ├── output.ipynb
├── order_report/          # Huvudpaketet
│   ├── __init__.py        # Exporterar det publika gränssnittet
│   ├── __main__.py        # Huvudstartpunkt (entry point för execution)
│   ├── io.py              # I/O-hantering (läs/skriv CSV)
│   ├── log_config.py      # Centraliserad konfiguration av logging
│   ├── processes.py       # Datatvätt och härledning av kolumner
│   ├── reporting.py       # Dataklasser/OOP för rapportkonfiguration
│   ├── transform.py       # Rena funktioner för aggregering och beräkningar
│   └── validation.py      # Schema- och kolumnvalidering
├── tests/                 # Automatiska enhetstester
│   ├── test_io.py
│   ├── test_log_config.py
│   └── test_validation.py
├── .gitignore
├── code_review.md         # Kodgranskning av ursprunglig kod
├── order_report.py        # Ursprunglig monolitisk källkodsfil
├── pyproject.toml         # Paket- och beroendekonfiguration
└── README.md              # Projekt- och reflektionsdokumentation
```