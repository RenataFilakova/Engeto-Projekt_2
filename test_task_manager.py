import pytest
from vylepseny_task_manager import (
    pripojeni_db,
    vytvoreni_tabulky,
    pridat_ukol_db,
    aktualizovat_ukol_db,
    odstranit_ukol_db,
)


TABLE = "ukoly"


@pytest.fixture(scope="module")
def conn_module():
    """Připojení k testovací DB a zajištění tabulky."""
    conn = pripojeni_db()
    assert conn is not None, "Nepodařilo se připojit k databázi"

    vytvoreni_tabulky(conn)
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def cleanup(conn_module):
    """Vyčistí testovací data před a po každém testu."""
    with conn_module.cursor() as cursor:
        cursor.execute(f"DELETE FROM {TABLE} WHERE nazev LIKE %s", ("test_%",))
        conn_module.commit()
    yield
    with conn_module.cursor() as cursor:
        cursor.execute(f"DELETE FROM {TABLE} WHERE nazev LIKE %s", ("test_%",))
        conn_module.commit()


# =========================
# TEST: PŘIDÁNÍ ÚKOLU
# =========================

def test_pridat_ukol_db_positive(conn_module):
    new_id = pridat_ukol_db(conn_module, "test_pridani", "test_popis")
    assert isinstance(new_id, int)

    with conn_module.cursor() as cursor:
        cursor.execute(
            "SELECT nazev, popis, stav FROM ukoly WHERE id = %s",
            (new_id,),
        )
        row = cursor.fetchone()

    assert row is not None
    assert row[0] == "test_pridani"
    assert row[1] == "test_popis"
    assert row[2] == "Nezahájeno"


def test_pridat_ukol_db_negative():
    conn = pripojeni_db()
    with pytest.raises(ValueError):
        pridat_ukol_db(conn, "", "popis")
    with pytest.raises(ValueError):
        pridat_ukol_db(conn, "nazev", "")
    conn.close()


# =========================
# TEST: AKTUALIZACE ÚKOLU
# =========================

def test_aktualizovat_ukol_db_positive(conn_module):
    task_id = pridat_ukol_db(conn_module, "test_update", "popis")

    ok = aktualizovat_ukol_db(conn_module, task_id, "Hotovo")
    assert ok is True

    with conn_module.cursor() as cursor:
        cursor.execute(
            "SELECT stav FROM ukoly WHERE id = %s",
            (task_id,),
        )
        stav = cursor.fetchone()[0]

    assert stav == "Hotovo"


def test_aktualizovat_ukol_db_negative_invalid_state(conn_module):
    task_id = pridat_ukol_db(conn_module, "test_update_invalid", "popis")

    with pytest.raises(ValueError):
        aktualizovat_ukol_db(conn_module, task_id, "NEPLATNY_STAV")


# =========================
# TEST: ODSTRANĚNÍ ÚKOLU
# =========================

def test_odstranit_ukol_db_positive(conn_module):
    task_id = pridat_ukol_db(conn_module, "test_delete", "popis")

    ok = odstranit_ukol_db(conn_module, task_id)
    assert ok is True

    with conn_module.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM ukoly WHERE id = %s",
            (task_id,),
        )
        count = cursor.fetchone()[0]

    assert count == 0


def test_odstranit_ukol_db_negative(conn_module):
    ok = odstranit_ukol_db(conn_module, 999999)
    assert ok is False
