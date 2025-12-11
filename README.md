Projekt 2: Vylepšený Task Manager (Engeto)
1. Popis projektu

Projekt implementuje správu úkolů ukládaných v MySQL databázi.
Aplikace umožňuje provádět CRUD operace (Create, Read, Update, Delete) a obsahuje také automatizované testy pomocí pytestu.


2. Funkce aplikace
Hlavní funkcionality:

Přidání úkolu

Zobrazení úkolů (pouze Nezahájeno + Probíhá)

Aktualizace úkolu (změna stavu)

Odstranění úkolu

Ukončení programu

Automatické hodnoty:

ID generováno databází

Výchozí stav = Nezahájeno

Datum vytvoření = aktuální timestamp

3. Databázová struktura
Databáze:

task_manager_test

Tabulka ukoly:
Sloupec	Typ	Poznámka
id	INT AUTO_INCREMENT	primární klíč
nazev	VARCHAR(255)	povinný
popis	TEXT	povinný
stav	VARCHAR(50)	výchozí: Nezahájeno
datum_vytvoreni	DATETIME	automaticky
4. Nastavení prostředí

Před spuštěním aplikace nastavte environment proměnné (PowerShell):

$env:TM_DB_HOST="127.0.0.1"
$env:TM_DB_USER="root"
$env:TM_DB_PASSWORD="heslo"
$env:TM_DB_NAME="task_manager_test"


5. Spuštění aplikace
python vylepseny_task_manager.py

6. Automatizované testy

Testy se nacházejí v souboru:

tests_testmanager.py

Spuštění testů:
python -m pytest -q tests_testmanager.py

Očekávaný výsledek:
6 passed


Testy pokrývají:

přidání úkolu

aktualizaci úkolu

odstranění úkolu

validaci vstupů

chování při neplatných hodnotách

Každá testovaná funkce obsahuje pozitivní i negativní scénář.

7. Instalace závislostí
pip install -r requirements.txt


Obsah requirements.txt:

mysql-connector-python
pytest

8. .gitignore

Repo ignoruje:

__pycache__/

.pytest_cache/

.pyc soubory

virtuální prostředí (venv/)

editorové složky (VSCode, IDEA)

9. Splnění zadání

Projekt splňuje všechny body požadované v zadání:

✔ použití MySQL
✔ CRUD operace
✔ validace vstupů
✔ automatizované testy (pozitivní + negativní)
✔ mazání testovacích dat
✔ dokumentace v README
✔ čistý repozitář bez zbytečných souborů
