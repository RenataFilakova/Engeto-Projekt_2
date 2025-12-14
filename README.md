Projekt 2 – Vylepšený Task Manager (MySQL + Python)


Aplikace umožňuje spravovat úkoly (CRUD operace) a ukládat je do **MySQL databáze** místo do paměti programu.

Projekt zahrnuje:
- plně funkční konzolovou aplikaci,
- validaci uživatelských vstupů,
- práci s databází,
- testování pomocí `pytest`.

---

  Funkcionalita aplikace

Aplikace umožňuje:

1️ **Přidat úkol**
- uživatel zadá název a popis (obojí povinné),
- výchozí stav: **Nezahájeno**,
- datum vytvoření se ukládá automaticky (`NOW()`),
- vložení probíhá do MySQL databáze.

2️ **Zobrazit aktivní úkoly**
- zobrazují se pouze úkoly se stavem:
  - **Nezahájeno**
  - **Probíhá**
- výpis je formátovaný a přehledný.

3️ **Aktualizovat úkol**
- uživatel vidí aktivní úkoly,
- zadá ID úkolu nebo **q** pro návrat,
- vybere nový stav:  
  1 – Probíhá  
  2 – Hotovo  
- úkol je aktualizován v databázi.

4️ **Odstranit úkol**
- zobrazí se seznam aktivních úkolů,
- uživatel zadá ID nebo **q** pro návrat,
- úkol je trvale odstraněn z databáze.

5️ **Konec programu**



