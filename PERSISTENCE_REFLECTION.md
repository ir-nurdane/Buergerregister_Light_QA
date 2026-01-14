# Reflexion zum JsonPersistence-Modul

### 1. Wesentlicher Nutzen
Das Persistenzmodul verwandelt das Programm von einem flüchtigen Skript in ein nutzbares System. Ohne Persistenz sind alle Eingaben nach dem Neustart verloren. Mit `save` und `load` kann der Zustand der Anwendung (die Liste der Bürger) dauerhaft auf der Festplatte gesichert und wiederhergestellt werden.

### 2. Warum JSON?
Für dieses Projekt ist JSON ideal, weil:
* **Lesbarkeit:** JSON ist textbasiert. Ich kann die gespeicherte Datei einfach im Editor öffnen und prüfen, ob die Daten korrekt aussehen.
* **Einfachheit:** Python bringt mit dem `json`-Modul bereits alles mit, was man braucht (keine externen Bibliotheken nötig).
* **Interoperabilität:** Falls wir später ein Web-Frontend bauen würden, könnte dieses das JSON-Format direkt verstehen.

### 3. Randfälle
Besonders wichtig waren:
* **Fehlende Datei:** Das Programm darf beim ersten Start (wenn noch keine Datei da ist) nicht abstürzen. Lösung: `path.exists()` prüfen und leeres Register zurückgeben.
* **Ungültige Daten:** Wenn jemand die JSON-Datei manuell editiert und Fehler einbaut (z.B. fehlender Name), darf das Programm dies nicht ungeprüft laden. Lösung: Ich nutze die bestehende `is_valid()`-Methode der Klasse `Person` beim Laden. Nur valide Objekte landen im Register.

### 4. Weiterentwicklung (Enterprise)
In einem großen System stößt JSON an Grenzen (Performance bei Millionen Einträgen, gleichzeitiger Zugriff). Man würde stattdessen:
* Eine **Datenbank** (SQL wie PostgreSQL oder NoSQL wie MongoDB) nutzen.
* Eine **REST-API** bauen, die JSON nur zur Übertragung nutzt, aber nicht zur Speicherung.
* Ein **Interface** definieren (z.B. `IPersistence`), damit man die Speicherart (Datei vs. Datenbank) austauschen kann, ohne den Rest des Codes zu ändern.

### 5. Abwärtskompatibilität
Wenn die Klasse `Person` ein neues Feld bekommt (z.B. `email`), haben alte JSON-Dateien dieses Feld noch nicht.
* **Lösung:** Beim Laden `.get("email", standardwert)` verwenden.
* **Testen:** Man schreibt einen Test, der eine "alte" JSON-Datei (ohne E-Mail) lädt und prüft, ob das Objekt trotzdem korrekt erstellt wird und das Feld einen sinnvollen Standardwert hat.