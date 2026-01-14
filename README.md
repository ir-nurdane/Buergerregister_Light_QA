# Bürgerregister Light - Qualitätssicherung

Dieses Projekt demonstriert einen ingenieurmäßigen Ansatz zur Qualitätssicherung eines Python-Prototyps. [cite_start]Es wurde im Rahmen der Portfolioprüfung Teil III im Modul Software Engineering II an der Hochschule Bremen entwickelt.

## 🚀 Projektübersicht
Das System verwaltet Bürgerdaten und stellt sicher, dass diese valide und konsistent gespeichert werden. Der Fokus liegt hierbei nicht auf neuen Features, sondern auf:
* [cite_start]**Automatisierter Testung** mit `pytest`.
* [cite_start]**Messung der Testabdeckung** mit `pytest-cov`.
* [cite_start]**Code-Metriken** zur Analyse der Wartbarkeit mit `radon`.
* [cite_start]**Continuous Integration** via GitHub Actions.

## 🛠 Installation
Um das Projekt lokal zu nutzen, klone das Repository und installiere die notwendigen Abhängigkeiten:

```bash
# Repository klonen
git clone [https://github.com/ir-nurdane/Buergerregister_Light_QA.git](https://github.com/ir-nurdane/Buergerregister_Light_QA.git)

# In das Verzeichnis wechseln
cd Buergerregister_Light_QA

# Abhängigkeiten installieren
pip install pytest pytest-cov radon
