Funkcionalita aplikace:

Aplikace nabízí následující možnosti:

Přidat úkol

zadání názvu a popisu

validace prázdných vstupů

úkol se ukládá do databáze

Zobrazit úkoly

výpis všech uložených úkolů

přehledná struktura výpisu

Aktualizovat úkol

výběr úkolu podle ID

změna stavu na: Nezahájeno / Probíhá / Hotovo

možnost návratu do menu volbou q

Odstranit úkol

smazání úkolu podle ID

zobrazení seznamu úkolů před mazáním

možnost návratu volbou q

Ukončit program

Databázová vrstva

Aplikace používá MySQL a při spuštění provede tyto akce:

připojí se pomocí zadaných environmentálních proměnných

automaticky vytvoří tabulku ukoly, pokud neexistuje

ukládá úkoly se strukturou:

Sloupec	Typ	Popis
id	INT AUTO_INCREMENT	Primární klíč
nazev	VARCHAR(255)	Název úkolu
popis	TEXT	Popis úkolu
stav	VARCHAR(50)	Stav úkolu
datum_vytvoreni	DATETIME	Automatické vyplnění
🔧 Nastavení MySQL připojení

Před spuštěním aplikace je nutné nastavit environmentální proměnné:

Windows PowerShell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="TVÉ_HESLO"
$env:DB_NAME="task_manager_test"

Alternativně je lze přidat do systémových proměnných natrvalo.
 
 Spuštění aplikace
python vylepseny_task_manager.py

 Automatizované testy

Testy jsou napsány v souboru tests_testmanager.py.
Testují:

přidání úkolu

aktualizaci úkolu

mazání úkolu

negativní a hraniční scénáře

validaci vstupních hodnot

práci s MySQL pomocí testovací databáze

Spuštění testů:
python -m pytest -q

Struktura projektu:
Projekt_2/
│
├── vylepseny_task_manager.py     # hlavní aplikace
├── tests_testmanager.py          # automatizované testy
├── README.md                     # dokumentace
└── .gitignore                    # ignorované soubory

