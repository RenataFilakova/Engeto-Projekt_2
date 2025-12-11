import mysql.connector
from mysql.connector import Error

# ❗ UPRAV SEM SVOJE ÚDAJE ❗
DB_HOST = "localhost"
DB_USER = "novy_uzivatel"
DB_PASSWORD = "Prahacz10"  
DB_NAME = "task_manager"


# 1) Připojení k databázi
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if conn.is_connected():
            print("✅ Připojení k databázi proběhlo úspěšně.")
        return conn
    except Error as e:
        print("❌ Chyba připojení k databázi:", e)
        return None


# 2) Vytvoření tabulky
def vytvoreni_tabulky(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS ukoly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(255) NOT NULL,
        popis TEXT NOT NULL,
        stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
        datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    print("✅ Tabulka 'ukoly' je připravena.")


# 4) Přidání úkolu
def pridat_ukol(conn):
    while True:
        nazev = input("Zadej název úkolu: ").strip()
        popis = input("Zadej popis úkolu: ").strip()

        if not nazev or not popis:
            print("❗ Název i popis jsou povinné, zkus to znovu.")
            continue

        sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
        cur = conn.cursor()
        cur.execute(sql, (nazev, popis))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()

        print(f"✅ Úkol byl uložen s ID {new_id}. (stav: Nezahájeno)")
        break


# 5) Zobrazení úkolů
def zobrazit_ukoly(conn):
    sql = """
    SELECT id, nazev, popis, stav, datum_vytvoreni
    FROM ukoly
    WHERE stav IN ('Nezahájeno', 'Probíhá')
    ORDER BY datum_vytvoreni;
    """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()

    if not rows:
        print("ℹ Seznam úkolů je prázdný (Nezahájeno/Probíhá).")
        return

    print("\nAKTIVNÍ ÚKOLY:")
    print("-" * 60)
    for r in rows:
        print(f"[{r[0]}] {r[1]} ({r[3]}) – {r[2]} | vytvořeno: {r[4]}")
    print("-" * 60)


# 6) Aktualizace úkolu
def aktualizovat_ukol(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, nazev, stav FROM ukoly ORDER BY datum_vytvoreni;")
    rows = cur.fetchall()
    cur.close()

    if not rows:
        print("ℹ Žádné úkoly k aktualizaci.")
        return

    print("\nÚKOLY:")
    for r in rows:
        print(f"[{r[0]}] {r[1]} – aktuální stav: {r[2]}")

    while True:
        try:
            task_id = int(input("Zadej ID úkolu pro změnu stavu: ").strip())
        except ValueError:
            print("❗ Zadej platné číslo ID.")
            continue

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s", (task_id,))
        exists = cur.fetchone()[0] > 0
        cur.close()

        if not exists:
            print("❗ Úkol s tímto ID neexistuje, zkus to znovu.")
            continue

        print("Vyber nový stav:")
        print("1 – Probíhá")
        print("2 – Hotovo")
        volba = input("Zadej volbu: ").strip()

        if volba == "1":
            new_state = "Probíhá"
        elif volba == "2":
            new_state = "Hotovo"
        else:
            print("❗ Neplatná volba stavu.")
            continue

        cur = conn.cursor()
        cur.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (new_state, task_id))
        conn.commit()
        cur.close()

        print("✅ Stav úkolu byl aktualizován.")
        break


# 7) Odstranění úkolu
def odstranit_ukol(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, nazev FROM ukoly ORDER BY datum_vytvoreni;")
    rows = cur.fetchall()
    cur.close()

    if not rows:
        print("ℹ Žádné úkoly k odstranění.")
        return

    print("\nÚKOLY:")
    for r in rows:
        print(f"[{r[0]}] {r[1]}")

    while True:
        try:
            task_id = int(input("Zadej ID úkolu k odstranění: ").strip())
        except ValueError:
            print("❗ Zadej platné číslo ID.")
            continue

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s", (task_id,))
        exists = cur.fetchone()[0] > 0
        cur.close()

        if not exists:
            print("❗ Úkol s tímto ID neexistuje, zkus to znovu.")
            continue

        confirm = input("Opravdu chceš úkol smazat? (a/n): ").strip().lower()
        if confirm not in ("a", "y"):
            print("❌ Smazání zrušeno.")
            return

        cur = conn.cursor()
        cur.execute("DELETE FROM ukoly WHERE id = %s", (task_id,))
        conn.commit()
        cur.close()

        print("✅ Úkol byl smazán.")
        break


# 3) Hlavní menu
def hlavni_menu(conn):
    while True:
        print("\n===== Vylepšený Task Manager =====")
        print("1 – Přidat úkol")
        print("2 – Zobrazit úkoly (Nezahájeno / Probíhá)")
        print("3 – Aktualizovat úkol")
        print("4 – Odstranit úkol")
        print("5 – Ukončit program")

        volba = input("Zadej volbu: ").strip()

        if volba == "1":
            pridat_ukol(conn)
        elif volba == "2":
            zobrazit_ukoly(conn)
        elif volba == "3":
            aktualizovat_ukol(conn)
        elif volba == "4":
            odstranit_ukol(conn)
        elif volba == "5":
            print("👋 Konec programu.")
            break
        else:
            print("❗ Neplatná volba, zkus to znovu.")


def main():
    print("Spouštím Vylepšený Task Manager...")
    conn = pripojeni_db()
    if conn is None:
        print("❗ Nelze pokračovat bez připojení k databázi.")
        return

    vytvoreni_tabulky(conn)

    try:
        hlavni_menu(conn)
    finally:
        conn.close()
        print("🔚 Spojení s databází ukončeno.")


if __name__ == "__main__":
    main()
