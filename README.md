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
│   └── testing.ipynb
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

---

## Reflektion

### 1. Vilka var de viktigaste problemen i originalkoden?
Originalkoden var uppbyggd som en monolit i en enda fil (`order_report.py`). De största bristerna var:
* **Brutit mot Single Responsibility Principle (SRP):** Samma kodblock läste filer, tvättade data, utförde beräkningar och skrev till disk.
* **Svårtestat:** Eftersom I/O var sammankopplat med beräkningarna gick det inte att enhetstesta transformeringar utan att skriva filer till disken.
* **Bristfälligt felhanterande & logging:** Använde `print()` istället för strukturerad `logging`, samt en bred `except Exception` som dolde potentiella fel.
* **Kodduplicering:** Samma `groupby`- och aggregeringslogik upprepades manuellt tre gånger för olika rapportvyer.

### 2. Vilka förändringar tycker du förbättrade programmet mest?
Separationen av ansvarsområden var den enskilt viktigaste förbättringen. Att bryta ut beräkningarna till rena funktioner (*pure functions*) i `transform.py` som enbart tar emot och returnerar `DataFrames` gjorde koden förutsägbar och testbar. Att ersätta `print()` med centraliserad `logging` i `log_config.py` samt hantera sökvägar dynamiskt via `pathlib` gjorde hela systemet robust.

### 3. Varför valde du den projektstruktur du använde?
Strukturen delar upp flödet i logiska lager:
* `io.py` hanterar enbart filsystemet.
* `validation.py` säkerställer dataintegritet.
* `processes.py` och `transform.py` hanterar datatransformation.
* `__main__.py` fungerar som orkestrerare.

Detta gör projektet lättnavigerat för andra utvecklare – vill man lägga till en ny rapport behöver man bara lägga till en funktion i `transform.py` utan att riskera att förstöra I/O- eller valideringslogik.

### 4. Var använde du OOP/dataclass och varför passade det där?
I `reporting.py` användes en `@dataclass` (t.ex. `ReportConfig`) för att hantera konfigurationsinställningar och sökvägar. Det kapslar in inställningar på ett typsäkert och oföränderligt (*immutable*) sätt istället för att skicka runt lösa strängar och hårdkodade argument i pipeline-funktionerna.

### 5. Vilka viktiga beteenden skyddar dina automatiska tester, och vilken nytta ger testerna om programmet förändras i framtiden?
Testerna i `tests/` täcker tre centrala områden:
* `test_io.py`: Verifierar att korrekt fel kastas (`FileNotFoundError`) om indata saknas och att CSV-filer skrivs korrekt.
* `test_validation.py`: Säkerställer att datamodellen upptäcker och stoppar skadad data som saknar obligatoriska kolumner (`ValueError`).
* `test_log_config.py`: Kontrollerar att loggningskonfigurationen inte skapar duplicerade handlers.

Testerna fungerar som ett säkerhetsnät vid framtida refaktorisering eller tillägg av funktioner (regressionsskydd).

### 6. Vad var svårast?
Att sätta knivskarpa gränser för varje moduls ansvar (SRP) – särskilt att helt rensa bort I/O-beroenden från transformations- och bearbetningsmodulerna, samt att hantera relativa sökvägar och moduleringsimporter så att paketet exekverar sömlöst både från terminalen och i Jupyter Notebooks.

### 7. Vad hade du velat förbättra ytterligare om du haft mer tid?
* Utöka testtäckningen i `pytest` med fler kantfall för `processes.py` (t.ex. validering av negativa priser, ogiltiga datumformat eller extrema rabattsatser).
* Lägga till CLI-argumenthantering via `argparse` i `__main__.py` så att användare kan skicka in anpassade filvägar direkt från terminalen.