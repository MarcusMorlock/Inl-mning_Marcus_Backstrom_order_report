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
I `reporting.py` användes en `@dataclass`  `ReportConfig` för att hantera konfigurationsinställningar och sökvägar. Det kapslar in inställningar på ett typsäkert och oföränderligt (*immutable*) sätt istället för att skicka runt lösa strängar och hårdkodade argument i pipeline-funktionerna.

### 5. Vilka viktiga beteenden skyddar dina automatiska tester, och vilken nytta ger testerna om programmet förändras i framtiden?

Testsviten i `tests/` skyddar systemets kritiska I/O-, validerings- och loggningsfunktionalitet genom följande verifieringar:

* **I/O- och filhantering (`test_io.py`):**
  * **Dataintegritet:** Säkerställer att korrekt formaterade CSV-filer läses in till identiska `pandas.DataFrame`-objekt med rätt datatyper.
  * **Felhantering vid felaktig indata:** Verifierar att systemet kastar `FileNotFoundError` om filen saknas, samt `ValueError` om filen är tom eller saknar giltig CSV-struktur (t.ex. 0-bytesfiler).
  * **Robust utdata:** Kontrollerar att målmappar skapas automatiskt om de saknas när rapporter sparas, samt att OS- och behörighetsfel (`PermissionError`) fångas upp och retsamt omvandlas till kontrollerade `RuntimeError` (verifierat via mocking med `unittest.mock.patch`).

* **Loggningskonfiguration (`test_log_config.py`):**
  * **Strukturerat format:** Verifierar med reguljära uttryck (`re`) att loggmeddelanden följer den exakta tids- och nivåstrukturen (`YYYY-MM-DD HH:MM:SS | INFO | order_report | ...`).
  * **Idempotens/Dupliceringsskydd:** Säkerställer att upprepade anrop till `configure_log()` inte skapar dubbla handlers eller duplicerade loggrader.

* **Schema- och kolumnvalidering (`test_validation.py`):**
  * **Datakvalitet:** Verifierar att `validate_order_df()` kastar `ValueError` och loggar ett `ERROR`-meddelande om obligatoriska kolumner (`REQUIRED`) saknas, samt släpper igenom giltiga dataframes utan anmärkning.

**Framtida nytta:** Testerna fungerar som ett automatiskt säkerhetsnät (regressionsskydd). Om koden refaktoreras eller nya funktioner byggs ut i framtiden upptäcker `pytest` omedelbart om en förändring krockar med befintlig I/O-logik, förstör loggformatet eller släpper igenom ogiltig data.

### 6. Vad var svårast?
Det svåraste i projektet var framför allt tre saker:

- Gränsdragningen vid omskrivning: Att avgöra vad som faktiskt krävde en komplett omskrivning från grunden och vad som bara behövde flyttas över till en bättre struktur.

- Hitta rätt nivå på modularitet: Det var en balansgång att dela upp originalkoden i mindre, fokuserade funktioner utan att "över-atomisera" och stycka sönder flödet i för många mikrofuktioner.

- Sökvägar och modulstruktur: Att bygga en sökvägshantering som var både modulär och konsekvent, så att paketet fungerar på exakt samma sätt oavsett om det körs från terminalen, testerna eller i Jupyter Notebooks.

### 7. Vad hade du velat förbättra ytterligare om du haft mer tid?
* Utöka testtäckningen i `pytest` med fler kantfall för `validate.py` (t.ex. validering av negativa priser, ogiltiga datumformat eller extrema rabattsatser).
* Använda `dataclass` för att göra transform och process modulär så det går både om man vill använda `dataclass` och få det som original koden gjorde och testa å göra så det kan bli olika typer av reporter antingen med flera `datclasses` eller manuella inputs. 