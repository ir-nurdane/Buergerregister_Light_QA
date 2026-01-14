from person import Person, normalize_text

class Buergerregister:
    def __init__(self):
        self._personen: list[Person] = []

    def add(self, p: Person):
        ok, errs = p.is_valid()
        if not ok:
            return False, errs
        if any(x.vorname == p.vorname and x.nachname == p.nachname and x.geburtsjahr == p.geburtsjahr for x in self._personen):
            return False, ["Duplikat."]
        self._personen.append(p)
        return True, []

    def list_all(self):
        return list(self._personen)

    def find_by_lastname(self, name: str):
        n = normalize_text(name)
        return [p for p in self._personen if normalize_text(p.nachname) == n]
