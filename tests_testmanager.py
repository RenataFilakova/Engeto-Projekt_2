"""
Pytest testy (interaktivní) pro vylepseny_task_manager.
Testy používají monkeypatch k simulaci vstupu přes input() a capsys k zachycení výstupu.

Spuštění:
python -m pytest -q tests_testmanager.py
"""

import pytest
import builtins
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
    conn = pripojeni_db()  # používá env proměnné nastavené v PowerShellu
    vytvoreni_tabulky(conn)
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def cleanup(conn_module):
    # před a po každém testu smaže testovací záznamy
    cursor = conn_module.cursor()
    cursor.execute(f"DELETE FROM {TABLE} WHERE nazev LIKE %s", ("test_%",))
    conn_module.commit()
    cursor.close()
    yield
    cursor = conn_module.cursor()
    cursor.execute(f"DELETE FROM {TABLE} WHERE nazev LIKE %s", ("test_%",))
    conn_module.commit()
    cursor.close()


# ---------- Přidání úkolu (interaktivně) ----------

def test_pridat_ukol_positive(conn_module, monkeypatch):
    inputs = iter(["test_pridani_ok", "popis testu"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    pridat_ukol(conn_module)
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT id, nazev, popis, stav FROM {TABLE} WHERE nazev=%s", ("test_pridani_ok",))
    row = cursor.fetchone()
    cursor.close()
    assert row is not None
    assert row[1] == "test_pridani_ok"
    assert row[2] == "popis testu"
    assert row[3] == "Nezahájeno"


def test_pridat_ukol_negative_empty_name(conn_module, monkeypatch, capsys):
    # nejprve prázdný název -> očekáváme chybovou hlášku, poté zadáme platné hodnoty, aby funkce skončila
    inputs = iter(["", "nějaký popis", "test_pridani_ok2", "popis2"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    pridat_ukol(conn_module)
    out = capsys.readouterr().out
    assert "Název i popis jsou povinné" in out or "povinné" in out
    # ověříme, že byl vložen ten platný (druhý) záznam
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT nazev FROM {TABLE} WHERE nazev=%s", ("test_pridani_ok2",))
    row = cursor.fetchone()
    cursor.close()
    assert row is not None


# ---------- Aktualizace úkolu (interaktivně) ----------
def test_aktualizovat_ukol_positive(conn_module, monkeypatch):
    # vložíme testovací úkol
    inputs_add = iter(["test_update_ok", "popis"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs_add))
    pridat_ukol(conn_module)
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT id FROM {TABLE} WHERE nazev=%s", ("test_update_ok",))
    new_id = cursor.fetchone()[0]
    cursor.close()

    # simulujeme aktualizaci: zadáme ID a volbu 1 (Probíhá)
    inputs_update = iter([str(new_id), "1"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs_update))
    aktualizovat_ukol(conn_module)
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT stav FROM {TABLE} WHERE id=%s", (new_id,))
    stav = cursor.fetchone()[0]
    cursor.close()
    assert stav == "Probíhá"


def test_aktualizovat_ukol_negative_invalid_id(conn_module, monkeypatch, capsys):
    # připravíme existující úkol, ale jako první zadáme neexistující ID -> ověříme chybovou hlášku
    inputs_add = iter(["test_update2", "popis"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs_add))
    pridat_ukol(conn_module)
    # získáme existující id, abychom mohli funkci dovést do konce po neplatném vstupu
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT id FROM {TABLE} WHERE nazev=%s", ("test_update2",))
    real_id = cursor.fetchone()[0]
    cursor.close()

    # nejprve zadáme neexistující ID, poté platné id a volbu stavu
    inputs = iter(["999999", "1", str(real_id), "2"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    aktualizovat_ukol(conn_module)
    out = capsys.readouterr().out
    assert "Úkol s tímto ID neexistuje" in out or "neexistuje" in out


# ---------- Odstranění úkolu (interaktivně) ----------
def test_odstranit_ukol_positive(conn_module, monkeypatch):
    inputs_add = iter(["test_remove_ok", "popis"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs_add))
    pridat_ukol(conn_module)
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT id FROM {TABLE} WHERE nazev=%s", ("test_remove_ok",))
    new_id = cursor.fetchone()[0]
    cursor.close()

    inputs_del = iter([str(new_id), "a"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs_del))
    odstranit_ukol(conn_module)
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE id=%s", (new_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    assert count == 0


def test_odstranit_ukol_negative_invalid_id(conn_module, monkeypatch, capsys):
    # vytvoříme jeden reálný úkol, ale jako první zadáme neexistující ID -> ověříme chybovou hlášku
    inputs_add = iter(["test_remove2", "popis"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs_add))
    pridat_ukol(conn_module)
    cursor = conn_module.cursor()
    cursor.execute(f"SELECT id FROM {TABLE} WHERE nazev=%s", ("test_remove2",))
    real_id = cursor.fetchone()[0]
    cursor.close()

    # nejprve neexistující ID, pak platné ID a potvrzení, aby funkce skončila
    inputs = iter(["999999", "a", str(real_id), "a"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    odstranit_ukol(conn_module)
    out = capsys.readouterr().out
    assert "Úkol s tímto ID neexistuje" in out or "neexistuje" in out
