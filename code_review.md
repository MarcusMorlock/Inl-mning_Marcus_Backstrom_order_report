1.
Observation: Hela programmets flöde — från filinläsning och databearbetning till beräkningar och filskrivning — ligger insvept i ett enda globalt `try...except Exception`-block.

Konsekvens: Det går inte att se var i processen ett fel faktiskt uppstod. Om skriptet kraschar vet man inte om det var inläsningen, bearbetningen eller sparandet som misslyckades, vilket gör felsökning och vidareutveckling svår.

Förslag: Ta bort det täckande `try-except`-blocket runt hela skriptet. Dela upp koden i tydliga, separata steg (inläsning, transformering/beräkning, spara rapport) och validera indatan explicit innan bearbetningen påbörjas.

2.
Observation: Beräkningskedjan för försäljning och returer per kategori (result1) och region (result2) är uppbyggd av identisk kod på två ställen i filen.

Konsekvens: Onödig duplicering gör koden svårare att underhålla. Om formeln för return_rate eller avrundningen behöver ändras måste det göras manuellt i flera block, med risk för att man missar något.

Förslag:Skapa en återanvändbar funktion som tar emot kolumnnamnet (t.ex. "product_category" eller "region") som parameter och returnerar den aggregerade DataFramen.

3.
Observation: Samma anrop med os.path.join(OUTPUT_FOLDER, ...) och .to_csv(..., index=False) upprepas manuellt fyra gånger för varje genererad rapport.

Konsekvens: Filskrivningslogiken är hårdkopplad och utspridd i filen, vilket ökar mängden boilerplate-kod.

Förslag: Skapa en hjälpfunktion eller hanterare för filexport som tar emot en DataFrame och ett filnamn och sköter skrivningen till utdatamappen.

4.
Observation: Programmet använder print()-satser för att skriva ut statusuppdateringar i konsolen under körningen.

Konsekvens: Informationen visas bara live i terminalen och sparas ingenstans. Körs skriptet automatiskt eller i bakgrunden går all historik förlorad, vilket gör det omöjligt att i efterhand kontrollera vad som hänt eller felsöka.

Förslag: Ersätt print() med Pythons inbyggda logging-modul. Sätt upp en central loggning som skriver meddelanden med tidsstämplar och loggnivåer, samt sparar dem till en loggfil.

#
5.
Observation: Saknade eller ogiltiga priser i unit_price ersätts automatiskt med medianvärdet för hela kolumnen via .fillna(data["unit_price"].median()).

Konsekvens: Att tyst hitta på ekonomiska siffror förvränger de totala försäljningsvärdena (total_sales) och döljer korrupt indata. I en finansiell rapport skapar detta en allvarlig revisions- och compliance-risk, då rapporten genererar direkt felaktiga underlag för ekonomiska beslut och bokföring.

Förslag: Validera att unit_price inte innehåller saknade värden och kasta ett tydligt fel eller logga en varning om priser saknas, istället för att ändra datan i tysthet.