import pytest
import json
from registry import Buergerregister
from person import Person
from json_persistence import JsonPersistence

# Hilfsfunktion zum Erstellen von Testpersonen
def create_person(vorname="Max", nachname="Mustermann", jahr=1990, stadt="Bremen"):
    return Person(vorname, nachname, jahr, stadt)

def test_roundtrip_save_and_load(tmp_path):
    """Testet Speichern und erneutes Laden (Roundtrip)."""
    # 1. Arrange
    datei = tmp_path / "test_daten.json"
    persistence = JsonPersistence()
    
    reg_original = Buergerregister()
    reg_original.add(create_person("Hans", "Müller"))
    reg_original.add(create_person("Lisa", "Meier"))

    # 2. Act
    persistence.save(reg_original, str(datei))
    reg_loaded = persistence.load(str(datei))

    # 3. Assert
    assert len(reg_loaded.list_all()) == 2
    # Prüfen, ob die Daten korrekt angekommen sind
    namen = [p.nachname for p in reg_loaded.list_all()]
    assert "Müller" in namen
    assert "Meier" in namen

def test_save_load_empty_register(tmp_path):
    """Leeres Register speichern und laden."""
    datei = tmp_path / "leer.json"
    persistence = JsonPersistence()
    reg = Buergerregister() # Leer

    persistence.save(reg, str(datei))
    reg_loaded = persistence.load(str(datei))

    assert len(reg_loaded.list_all()) == 0

def test_load_non_existent_file():
    """Nicht vorhandene Datei laden -> leeres Register."""
    persistence = JsonPersistence()
    # Datei existiert garantiert nicht
    reg = persistence.load("ghost_file_123.json")
    assert len(reg.list_all()) == 0

def test_load_mixed_valid_invalid_data(tmp_path):
    """Datei mit gültigen und ungültigen Datensätzen."""
    datei = tmp_path / "mixed.json"
    # Wir bauen manuell eine JSON-Datei
    raw_json = [
        {"vorname": "Gültig", "nachname": "Mensch", "geburtsjahr": 1990, "wohnort": "Hier"}, # OK
        {"vorname": "", "nachname": "Ungültig"}, # Vorname fehlt -> is_valid scheitert
        {"kaputt": 123} # Falsche Struktur
    ]
    datei.write_text(json.dumps(raw_json), encoding="utf-8")
    
    persistence = JsonPersistence()
    reg = persistence.load(str(datei))

    # Nur der eine gültige Eintrag sollte im Register landen
    assert len(reg.list_all()) == 1
    assert reg.list_all()[0].nachname == "Mensch"

def test_duplicate_lastnames(tmp_path):
    """Mehrere Personen mit demselben Nachnamen bleiben erhalten."""
    # Deine registry.py erlaubt gleiche Nachnamen, solange Vornamen/Jahr anders sind.
    datei = tmp_path / "dupes.json"
    persistence = JsonPersistence()
    
    reg = Buergerregister()
    reg.add(create_person("Tim", "Meyer"))
    reg.add(create_person("Susi", "Meyer")) # Gleicher Nachname, andere Person

    persistence.save(reg, str(datei))
    reg_loaded = persistence.load(str(datei))

    # Beide Meyers sollten da sein
    assert len(reg_loaded.list_all()) == 2
    # Optional: Suche testen
    meyers = reg_loaded.find_by_lastname("Meyer")
    assert len(meyers) == 2