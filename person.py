from dataclasses import dataclass

def normalize_text(s: str | None) -> str:
    if s is None:
        return ""
    return str(s).strip().title()

def parse_geburtsjahr(y) -> int | None:
    try:
        y = int(y)
        return y if 1900 <= y <= 2025 else None
    except Exception:
        return None

@dataclass
class Person:
    vorname: str
    nachname: str
    geburtsjahr: int
    wohnort: str

    def is_valid(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not normalize_text(self.vorname):
            errors.append("Vorname fehlt.")
        if not normalize_text(self.nachname):
            errors.append("Nachname fehlt.")
        if parse_geburtsjahr(self.geburtsjahr) is None:
            errors.append("Geburtsjahr unplausibel.")
        if not normalize_text(self.wohnort):
            errors.append("Wohnort fehlt.")
        return len(errors) == 0, errors

    def __str__(self) -> str:
        return f"{normalize_text(self.vorname)} {normalize_text(self.nachname)} ({self.geburtsjahr}) – {normalize_text(self.wohnort)}"
