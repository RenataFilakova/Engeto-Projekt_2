import pytest
from vylepseny_task_manager import (
    pripojeni_db,
    vytvoreni_tabulky,
    pridat_ukol,
    aktualizovat_ukol,
    odstranit_ukol,
)


TABLE = "ukoly"


@pytest.fixture(scope="module")
def conn_module():
    """Trvalé připojení k DB pro testy."""
    conn = pripojeni_db()
    vytvoreni_tabulky(conn)
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def cleanup(conn_module):
    """Před a po každém testu smaže testovací úkoly."""
    cursor = conn_module.cursor()
    cursor.execute(f"DELETE FROM {TABLE} WHERE nazev LIKE %s", ("test_%",))
    conn_module.commit()
    cursor.close()
    yield
    cursor = conn_module.cursor()
    cursor.execute(f"DELETE FROM {TABLE} WHERE nazev LIKE %s", ("test_%",))
    conn_module.commit()
    cursor.close()


def test_pridat_ukol_positive(conn_module, monkeypatch):
    inputs = iter(["test_pridani", "popis"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    new_id = pridat_ukol(conn_module)
    assert isinstance(new_id, int)


def test_pridat_ukol_negative_empty_name(conn_module, monkeypatch):
    inputs = iter(["", "popis"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert pridat_ukol(conn_module) is None


def test_aktualizovat_ukol_positive(conn_module, monkeypatch):
    cursor = conn_module.cursor()
    cursor.execute(
        f"INSERT INTO {TABLE} (nazev, popis, stav) VALUES ('test_upd', 'p', 'Nezahájeno')"
    )
    conn_module.commit()
    test_id = cursor.lastrowid
    cursor.close()

    inputs = iter([str(test_id), "1"])  # Probíhá
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert aktualizovat_ukol(conn_module) is True


def test_aktualizovat_ukol_escape(conn_module, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert aktualizovat_ukol(conn_module) is False


def test_odstranit_ukol_positive(conn_module, monkeypatch):
    cursor = conn_module.cursor()
    cursor.execute(
        f"INSERT INTO {TABLE} (nazev, popis, stav) VALUES ('test_del', 'p', 'Nezahájeno')"
    )
    conn_module.commit()
    test_id = cursor.lastrowid
    cursor.close()

    inputs = iter([str(test_id)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert odstranit_ukol(conn_module) is True


def test_odstranit_ukol_escape(conn_module, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert odstranit_ukol(conn_module) is False
