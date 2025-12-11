📄 README.md – Projekt: Vylepšený Task Manager
📝 Popis projektu

Tento projekt je vylepšená verze správce úkolů.
Úkoly jsou ukládány do MySQL databáze a program podporuje operace CRUD (Create, Read, Update, Delete).
Součástí projektu jsou také automatizované testy pomocí pytestu.

📂 Funkcionality programu

Program nabízí:

Přidat úkol

Zobrazit úkoly (filtruje Nezahájeno + Probíhá)

Aktualizovat úkol

Odstranit úkol

Ukončit program

Automatické hodnoty:

ID = automaticky

Výchozí stav = Nezahájeno

Datum vytvoření = aktuální čas

🗄 Databáze a tabulka
Název databáze:

task_manager_test

Tabulka ukoly obsahuje:
Sloupec	Typ	Popis
id	INT AUTO_INCREMENT	Primární klíč
nazev	VARCHAR(255)	Povinné
popis	TEXT	Povinné
stav	VARCHAR(50)	Výchozí: Nezahájeno
datum_vytvoreni	DATETIME	Automatický timestamp
🛠 Nastavení projektu
1️⃣ Nastav environment proměnné

V PowerShellu:

$env:TM_DB_HOST="127.0.0.1"
$env:TM_DB_USER="root"
$env:TM_DB_PASSWORD="Prahacz10"
$env:TM_DB_NAME="task_manager_test"

2️⃣ Spuštění programu
python vylepseny_task_manager.py

🧪 Automatizované testy

Soubor: tests_testmanager.py
Testuje: přidání, aktualizaci, odstranění úkolů (pozitivní i negativní varianty).

Spuštění testů:
python -m pytest -q tests_testmanager.py

Očekávaný výsledek:
6 passed in X.XXs


Testy využívají:

pytest

monkeypatch (simulace input())

čištění databáze mezi testy

📁 .gitignore

Repozitorář ignoruje:

pycache

.pyc soubory

virtuální prostředí

pytest cache

editorové soubory

Autor:
Renata Filáková
