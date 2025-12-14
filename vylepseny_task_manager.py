import mysql.connector
from mysql.connector import Error
from typing import Optional

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "vylepseny_task_manager"


def pripojeni_db() -> Optional[mysql.connector.connection_cext.CMySQLConnection]:
    """Vytvoří připojení k MySQL databázi."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        print("Připojení k databázi proběhlo úspěšně.")
        return conn
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None


def vytvoreni_tabulky(conn) -> None:
    """Vytvoří tabulku 'ukoly', pokud neexistuje."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav VARCHAR(20) NOT NULL,
            datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()
    print("Tabulka 'ukoly' je připravena.")


def pridat_ukol(conn) -> Optional[int]:
    """Získá název a popis úkolu od uživatele a uloží ho do databáze."""

    nazev = input("Zadej název úkolu: ").strip()
    popis = input("Zadej popis úkolu: ").strip()

    if not nazev or not popis:
        print("Název i popis musí být vyplněny.")
        return None

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
        (nazev, popis, "Nezahájeno"),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()

    print(f"Úkol byl uložen pod ID {new_id}.")
    return new_id


def zobrazit_ukoly(conn) -> None:
    """Vypíše všechny úkoly mimo těch se stavem 'Hotovo'."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav != 'Hotovo'")
    ukoly = cursor.fetchall()
    cursor.close()

    print("\nAKTIVNÍ ÚKOLY:")
    print("-----------------------------")

    if not ukoly:
        print("Žádné úkoly k zobrazení.")
        return

    for u in ukoly:
        print(f"[{u[0]}] {u[1]} – {u[3]}")
        print(f"    Popis: {u[2]}")
        print("-----------------------------")


def aktualizovat_ukol(conn) -> bool:
    """Aktualizuje stav úkolu. Uživatel může zadat 'q' pro návrat do menu."""

    zobrazit_ukoly(conn)

    while True:
        user_input = input("Zadej ID úkolu ke změně nebo 'q' pro návrat: ").strip()

        if user_input.lower() == "q":
            print("Návrat do menu.")
            return False

        if not user_input.isdigit():
            print("Neplatné ID, zkus to znovu.")
            continue

        task_id = int(user_input)

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (task_id,))
        exists = cursor.fetchone()
        cursor.close()

        if not exists:
            print("Úkol s tímto ID neexistuje.")
            continue

        print("Nový stav:")
        print("1 – Probíhá")
        print("2 – Hotovo")

        volba = input("Zadej číslo stavu: ").strip()
        if volba == "1":
            new_state = "Probíhá"
        elif volba == "2":
            new_state = "Hotovo"
        else:
            print("Neplatná volba stavu.")
            continue

        cursor = conn.cursor()
        cursor.execute("UPDATE ukoly SET stav=%s WHERE id=%s", (new_state, task_id))
        conn.commit()
        cursor.close()

        print("Stav úkolu byl aktualizován.")
        return True


def odstranit_ukol(conn) -> bool:
    """Odstraní vybraný úkol. Uživatel může zadat 'q' pro návrat."""

    zobrazit_ukoly(conn)

    while True:
        user_input = input("Zadej ID úkolu k odstranění nebo 'q' pro návrat: ").strip()

        if user_input.lower() == "q":
            print("Návrat do menu.")
            return False

        if not user_input.isdigit():
            print("Neplatné ID, zkus to znovu.")
            continue

        task_id = int(user_input)

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id=%s", (task_id,))
        exists = cursor.fetchone()

        if not exists:
            cursor.close()
            print("Úkol s tímto ID neexistuje.")
            continue

        cursor.execute("DELETE FROM ukoly WHERE id=%s", (task_id,))
        conn.commit()
        cursor.close()

        print("Úkol byl odstraněn.")
        return True


def hlavni_menu(conn) -> None:
    """Zobrazuje hlavní menu aplikace a řídí tok programu."""

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
