import os
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Tuple

# =========================
# DB CONFIG (ENV VARS)
# =========================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "task_manager_test")


# =========================
# DB CONNECTION & SETUP
# =========================

def pripojeni_db() -> Optional[mysql.connector.connection_cext.CMySQLConnection]:
    """Vytvoří připojení k databázi."""
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None


def vytvoreni_tabulky(conn) -> None:
    """Vytvoří tabulku ukoly, pokud neexistuje."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(50) NOT NULL,
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.commit()


# =========================
# DB LOGIC (TESTABLE)
# =========================

def pridat_ukol_db(conn, nazev: str, popis: str) -> int:
    """Uloží úkol do DB a vrátí jeho ID."""
    if not nazev or not popis:
        raise ValueError("Název a popis nesmí být prázdné.")

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
            (nazev, popis, "Nezahájeno"),
        )
        conn.commit()
        return cursor.lastrowid


def ziskat_aktivni_ukoly(conn) -> List[Tuple]:
    """Vrátí aktivní úkoly (Nezahájeno, Probíhá)."""
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM ukoly WHERE stav != 'Hotovo'"
        )
        return cursor.fetchall()


def aktualizovat_ukol_db(conn, task_id: int, novy_stav: str) -> bool:
    """Aktualizuje stav úkolu."""
    if novy_stav not in ("Probíhá", "Hotovo"):
        raise ValueError("Neplatný stav.")

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE ukoly SET stav=%s WHERE id=%s",
            (novy_stav, task_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def odstranit_ukol_db(conn, task_id: int) -> bool:
    """Odstraní úkol z DB."""
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM ukoly WHERE id=%s", (task_id,))
        conn.commit()
        return cursor.rowcount > 0


# =========================
# UI FUNCTIONS
# =========================

def zobrazit_ukoly(conn) -> None:
    ukoly = ziskat_aktivni_ukoly(conn)
    print("\nAKTIVNÍ ÚKOLY:")
    print("-" * 30)
    if not ukoly:
        print("Žádné úkoly k zobrazení.")
    else:
        for u in ukoly:
            print(f"[{u[0]}] {u[1]} – {u[3]}")
            print(f"    Popis: {u[2]}")
    print("-" * 30)


def pridat_ukol(conn) -> None:
    nazev = input("Zadej název úkolu: ").strip()
    popis = input("Zadej popis úkolu: ").strip()
    try:
        new_id = pridat_ukol_db(conn, nazev, popis)
        print(f"Úkol byl uložen pod ID {new_id}.")
    except ValueError as e:
        print(e)


def aktualizovat_ukol(conn) -> None:
    zobrazit_ukoly(conn)
    volba = input("Zadej ID úkolu ke změně nebo 'q' pro návrat: ").strip()
    if volba.lower() == "q":
        return

    if not volba.isdigit():
        print("Neplatné ID.")
        return

    print("1 – Probíhá\n2 – Hotovo")
    stav = input("Zadej číslo stavu: ").strip()

    stav_map = {"1": "Probíhá", "2": "Hotovo"}
    if stav not in stav_map:
        print("Neplatná volba stavu.")
        return

    if aktualizovat_ukol_db(conn, int(volba), stav_map[stav]):
        print("Stav úkolu byl aktualizován.")
    else:
        print("Úkol s tímto ID neexistuje.")


def odstranit_ukol(conn) -> None:
    zobrazit_ukoly(conn)
    volba = input("Zadej ID úkolu k odstranění nebo 'q' pro návrat: ").strip()
    if volba.lower() == "q":
        return

    if not volba.isdigit():
        print("Neplatné ID.")
        return

    if odstranit_ukol_db(conn, int(volba)):
        print("Úkol byl odstraněn.")
    else:
        print("Úkol s tímto ID neexistuje.")


# =========================
# MAIN MENU
# =========================

def hlavni_menu(conn) -> None:
    while True:
        print("\n===== TASK MANAGER =====")
        print("1 – Přidat úkol")
        print("2 – Zobrazit úkoly")
        print("3 – Aktualizovat úkol")
        print("4 – Odstranit úkol")
        print("5 – Konec")

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
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba.")


if __name__ == "__main__":
    conn = pripojeni_db()
    if conn:
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
        conn.close()
