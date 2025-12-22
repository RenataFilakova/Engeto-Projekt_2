# Projekt 2 – Vylepšený Task Manager (MySQL + pytest)

Konzolová aplikace pro správu úkolů, která využívá **MySQL databázi** pro ukládání dat  
a obsahuje **automatizované testy pomocí pytest**, ověřující skutečný stav databáze.



---

 Funkcionalita aplikace

Aplikace umožňuje provádět základní CRUD operace nad úkoly:

- Přidání úkolu (název, popis, výchozí stav *Nezahájeno*)
- Zobrazení aktivních úkolů (*Nezahájeno*, *Probíhá*)
- Aktualizaci stavu úkolu (*Probíhá*, *Hotovo*)
- Odstranění úkolu
- Ukončení programu

Aplikace obsahuje validaci vstupů a únikové znaky (`q`) pro návrat do hlavního menu.

---

 Použité technologie

- Python 3
- MySQL
- mysql-connector-python
- pytest

---

 Databáze

Aplikace pracuje s MySQL databází.

- Databázové připojení je řízeno pomocí **environmentálních proměnných**
- Tabulka `ukoly` se vytvoří automaticky při spuštění aplikace (pokud neexistuje)
- Sloupec `datum_vytvoreni` je generován přímo databází

 Struktura tabulky `ukoly`

- `id` – primární klíč
- `nazev` – název úkolu
- `popis` – popis úkolu
- `stav` – stav úkolu (*Nezahájeno*, *Probíhá*, *Hotovo*)
- `datum_vytvoreni` – timestamp vytvoření

---

 Spuštění aplikace

Před spuštěním je nutné mít dostupnou MySQL databázi  
a nastavené environmentální proměnné:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="heslo"
$env:DB_NAME="task_manager_test"
