# Quiz Center - Interaktive Quiz-Plattform

Eine moderne Quiz-Anwendung mit automatischer Kategorieverwaltung und Python-basierten Management-Tools.

## Überblick

Das Quiz Center ist eine statische Web-Anwendung, die Quiz aus verschiedenen Kategorien organisiert und präsentiert. Die Anwendung unterstützt automatische Quiz-Erkennung und bietet Python-Scripts für einfache Verwaltung.

### Features

- **Responsive Design**: Funktioniert auf Desktop und mobilen Geräten
- **Automatische Quiz-Verwaltung**: Zentrale Konfiguration über config.json
- **Kategorisierung**: Übersichtliche Darstellung nach Themenbereichen
- **Python-Automation**: Scripts für Quiz-Erstellung und Wartung
- **Validierung**: Automatische Prüfung der Quiz-Struktur

## Projektstruktur

```txt
quiz/
├── config.json                 # Zentrale Konfiguration
├── index.html                  # Hauptseite
├── script.js                   # JavaScript-Logik
├── styles.css                  # Styling
├── update_config.py            # Config-Generator
├── quiz_tools.py               # Management-Tools
└── [kategorie]/
    └── [quiz-name]/
        ├── quiz.json           # Quiz-Daten
        ├── index.html          # Quiz-Seite
        ├── script.js           # Quiz-Logik
        ├── styles.css          # Quiz-Styling
        └── banner.png          # Banner-Bild
```

## Installation und Start

1. **Repository klonen oder Dateien herunterladen**

2. **HTTP-Server starten:**

   ```bash
   # Python 3
   python -m http.server 8000
   
   # Oder mit Live Server in VS Code
   ```

3. **Browser öffnen:**

   ```cmd
   http://localhost:8000
   ```

## Quiz hinzufügen

### Mit Python-Scripts (empfohlen)

```bash
# Neues Quiz erstellen
python quiz_tools.py create sport tennis

# Quiz-Daten anpassen (quiz.json bearbeiten)
# Banner-Bild ersetzen (banner.png)

# Konfiguration aktualisieren
python update_config.py
```

### Manuell

1. **Ordnerstruktur erstellen:**

   ```txt
   sport/tennis/
   ├── quiz.json
   ├── index.html
   ├── script.js
   ├── styles.css
   └── banner.png
   ```

2. **Config.json aktualisieren:**

   ```json
   {
     "categories": {
       "sport": {
         "name": "Sport",
         "icon": "fa-football", 
         "description": "Sportregeln und Wissenswertes",
         "quiz": ["basketball", "tennis"]
       }
     }
   }
   ```

## Python-Management-Tools

### update_config.py

Automatische Konfigurationsgenerierung:

```bash
# Verzeichnisse scannen und config.json aktualisieren
python update_config.py

# Mit spezifischem Pfad
python update_config.py /pfad/zum/quiz-verzeichnis
```

**Funktionen:**

- Scannt alle Kategorien-Ordner
- Erkennt vorhandene Quiz automatisch
- Aktualisiert config.json
- Behält bestehende Einstellungen bei
- Fügt Standard-Icons für neue Kategorien hinzu

### quiz_tools.py

Zusätzliche Verwaltungsfunktionen:

```bash
# Quiz erstellen
python quiz_tools.py create kategorie quiz-name

# Struktur validieren
python quiz_tools.py validate

# Leere Ordner aufräumen  
python quiz_tools.py cleanup
```

## Konfiguration

### config.json Struktur

```json
{
  "app": {
    "title": "Quiz Center",
    "description": "Quiz-Plattform Beschreibung",
    "version": "1.0.0",
    "language": "de"
  },
  "categories": {
    "kategorie-key": {
      "name": "Anzeigename",
      "icon": "fa-icon-name",
      "description": "Kategorie-Beschreibung", 
      "quiz": ["quiz1", "quiz2"]
    }
  }
}
```

### Quiz.json Format

```json
{
  "quiz": {
    "title": "Quiz-Titel",
    "description": "Quiz-Beschreibung",
    "language": "de",
    "version": "1.0",
    "questions": [
      {
        "id": "q1",
        "text": "Frage-Text",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correctIndex": 0,
        "explanation": "Erklärung der richtigen Antwort"
      }
    ]
  }
}
```

## Unterstützte Kategorien

Das System erkennt automatisch folgende Kategorien und weist passende Icons zu:

- **ai**: Künstliche Intelligenz (fa-robot)
- **sport**: Sport (fa-football)
- **science**: Wissenschaft (fa-microscope)
- **history**: Geschichte (fa-landmark)
- **geography**: Geographie (fa-globe)
- **math**: Mathematik (fa-calculator)
- **literature**: Literatur (fa-book)
- **music**: Musik (fa-music)
- **art**: Kunst (fa-palette)
- **technology**: Technologie (fa-laptop-code)

Neue Kategorien erhalten automatisch ein Standard-Icon (fa-question-circle).

## Workflow für neue Quiz

1. **Quiz erstellen:**

   ```bash
   python quiz_tools.py create science chemistry
   ```

2. **Inhalte anpassen:**
   - `quiz.json` mit Fragen füllen
   - `banner.png` ersetzen (400x200px empfohlen)

3. **Konfiguration aktualisieren:**

   ```bash
   python update_config.py
   ```

4. **Validieren:**

   ```bash
   python quiz_tools.py validate
   ```

5. **Browser aktualisieren** (F5)

## Wartung und Troubleshooting

### Häufige Befehle

```bash
# Vollständige Wartung
python quiz_tools.py validate && python quiz_tools.py cleanup && python update_config.py

# Status-Check
python update_config.py && python quiz_tools.py validate

# Neues Quiz + Config Update in einem
python quiz_tools.py create science physics && python update_config.py
```

### Problemlösung

- **Quiz wird nicht angezeigt**: `quiz.json` prüfen und `python quiz_tools.py validate` ausführen
- **Kategorie fehlt**: `python update_config.py` ausführen
- **Fehlerhafte config.json**: Backup wiederherstellen und erneut generieren
- **Scripts funktionieren nicht**: Python 3.6+ erforderlich

### Ausgeschlossene Ordner

Scripts ignorieren Ordner die beginnen mit:

- `_` (Templates, Backups)
- `.git`, `.vscode`, `__pycache__`, `node_modules`

## Technische Anforderungen

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Backend**: Python 3.6+ für Management-Scripts
- **Server**: HTTP-Server (Python, Live Server, etc.)
- **Browser**: Moderne Browser mit ES6-Unterstützung

Das Quiz Center ist als statische Web-App konzipiert und benötigt keine Datenbank oder Server-seitigen Code für den Betrieb.
