# Quiz App

Eine interaktive Quiz-Anwendung zum Testen des Wissens aus dem LLM Engineer's Handbook.

## Funktionen

- 10 zufällig ausgewählte Fragen aus einem Fragenpool
- Multiple Choice mit 4 Antwortmöglichkeiten
- Sofortiges Feedback mit Erklärungen
- Detaillierte Ergebnisauswertung
- Responsive Design für Desktop und Mobile
- Tastatur-Navigation
- Integrierter PDF-Viewer für das Regelwerk

## Bedienung

### Quiz starten

1. "Quiz starten" klicken
2. Fragen beantworten durch Klick oder Tastatur
3. Ergebnisse am Ende einsehen

### Tastatur-Shortcuts

- **1-4** oder **A-D**: Antwort auswählen
- **Enter** oder **N**: Nächste Frage
- **ESC**: Zum Startbildschirm zurück

### Quelle

- "Quelle anzeigen" klicken, um das PDF einzusehen
- Download-Funktion verfügbar

## Host

**Mit Python:**
```bash
python -m http.server 8000
```

**Mit Node.js:**
```bash
npx serve .
```

**Mit PHP:**
```bash
php -S localhost:8000
```

Anschließend `http://localhost:8000` im Browser öffnen.

## Fragen anpassen

Die Fragen sind in `quiz.json` gespeichert. Neue Fragen können nach folgendem Schema hinzugefügt werden:

```json
{
  "id": "q_new",
  "text": "Fragetext",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correctIndex": 0,
  "explanation": "Erklärung mit Quellenangabe"
}
```

**Wichtig:** `correctIndex` ist 0-basiert (0 = erste Option).

## Technische Details

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Datenformat:** JSON
- **Kompatibilität:** Moderne Browser (ES6+ erforderlich)
- **Abhängigkeiten:** Keine externen Libraries
