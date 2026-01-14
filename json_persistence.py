import json
from pathlib import Path
from registry import Buergerregister
from person import Person

class JsonPersistence:
    """Persistenzmodul für das Bürgerregister auf Basis von JSON."""

    def save(self, register: Buergerregister, filename: str) -> None:
        """
        Speichert alle Personen des übergebenen Registers in einer JSON-Datei [cite: 55-56].
        """
        personen = register.list_all()
        daten = []

        # 1. Daten serialisieren
        for p in personen:
            # Da Person eine Dataclass ist, greifen wir direkt auf die Attribute zu
            daten.append({
                "vorname": p.vorname,
                "nachname": p.nachname,
                "geburtsjahr": p.geburtsjahr,
                "wohnort": p.wohnort
            })

        # 2. JSON-Datei schreiben 
        path = Path(filename)
        try:
            with path.open("w", encoding="utf-8") as f:
                # ensure_ascii=False sorgt dafür, dass Umlaute lesbar bleiben
                # indent=2 macht die Datei für Menschen schön lesbar
                json.dump(daten, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def load(self, filename: str) -> Buergerregister:
        """
        Lädt Personen aus einer JSON-Datei und gibt ein neues Buergerregister zurück.
        """
        path = Path(filename)
        reg = Buergerregister()

        # Randfall 1: Datei existiert nicht -> Leeres Register zurückgeben
        if not path.exists():
            return reg

        try:
            text = path.read_text(encoding="utf-8")
            
            # Randfall 2: Datei ist leer (nur Whitespace) -> Leeres Register
            if not text.strip():
                return reg

            # JSON parsen
            data = json.loads(text)

            # Randfall 3: Validierung der JSON-Struktur
            # Wenn die JSON-Wurzel keine Liste ist -> Leeres Register
            if not isinstance(data, list):
                return reg

            # Personen erzeugen und einfügen
            for entry in data:
                try:
                    # Wir nutzen .get(), um Abstürze bei fehlenden Feldern zu vermeiden
                    vorname = entry.get("vorname", "")
                    nachname = entry.get("nachname", "")
                    geburtsjahr = entry.get("geburtsjahr", 0)
                    wohnort = entry.get("wohnort", "")

                    # Neues Person-Objekt erstellen
                    p = Person(vorname, nachname, geburtsjahr, wohnort)

                    # Prüfen, ob die Person valide ist (nutzt deine Logik aus person.py)
                    is_valid, _ = p.is_valid()
                    
                    if is_valid:
                        # Ins Register einfügen (nutzt deine Logik aus registry.py inkl. Duplikatscheck)
                        reg.add(p)
                        
                except Exception:
                    # Wenn ein einzelner Eintrag komplett kaputt ist, diesen überspringen
                    continue

        except json.JSONDecodeError:
            # Falls die Datei existiert, aber kein gültiges JSON enthält
            pass
        except Exception as e:
            print(f"Unerwarteter Fehler beim Laden: {e}")

        return reg