# Arbeitsauftrag

Vier seperate Aufgaben um ein quiz zu erstellen

## 1. Quiz-Struktur erstellen

### Ordner-Setup

1. Template kopieren:

   ```bash
   # Bestimme die richtige Kategorie
   # Hauptkategorien: ai/ oder sport/
   
   # Kopiere Template-Dateien
   cp -r _template/copyme/* [kategorie]/[quiz_name]/
   ```

2. Ordnername festlegen:
   - Format: URL-freundlich, lowercase, kurz
   - Trennung: Unterstriche (_) zwischen Wörtern
   - Beispiele:
     - ✅ `basketball`, `tennis`, `fussball` 
     - ✅ `machine_learning`, `data_science`
     - ❌ `Hobbyhorsing Quiz`, `LLM-Engineer`

### Kategorie-Zuordnung

- `ai/`: Künstliche Intelligenz, Programmierung, Tech
- `sport/`: Alle Sportarten und körperliche Aktivitäten
- `gesetze/`: Rechtswissenschaften, Gesetze, Verordnungen, Verfassung
- Neue Kategorien: Bei Bedarf weitere Hauptkategorien anlegen

### Automatische Konfiguration

Nach dem Kopieren führe das Update-Script aus:

```bash
# Aktualisiert config.json automatisch (empfohlen)
python update_config.py
```

### Checkliste Ordner-Setup

- [ ] Template-Dateien kopiert (`index.html`, `styles.css`, `script.js`, etc.)
- [ ] Ordnername URL-freundlich gewählt
- [ ] Richtige Kategorie zugeordnet (`ai/` oder `sport/`)
- [ ] `update_config.py` erfolgreich ausgeführt
- [ ] Neues Quiz in `config.json` sichtbar
- [ ] Ordnerstruktur vollständig:

  ```txt
  [kategorie]/[quiz_name]/
  ├── index.html
  ├── styles.css  
  ├── script.js
  ├── fontawesome.css
  └── (banner.png - wird später hinzugefügt)
  ```

### Beispiel-Commands

```bash
# Für ein Basketball-Quiz
mkdir sport/basketball
cp -r _template/copyme/* sport/basketball/
python update_config.py

# Für ein Machine Learning Quiz  
mkdir ai/machine_learning
cp -r _template/copyme/* ai/machine_learning/
python update_config.py

# Für ein Grundgesetz Quiz
mkdir gesetze/grundgesetz
cp -r _template/copyme/* gesetze/grundgesetz/
python update_config.py
```

Das Quiz erscheint dann automatisch in der Hauptübersicht und ist bereit für die nächsten Schritte!

## 2. Erstelle quiz.json

Du bist ein „Quiz-Generator“ für Fachtexte und Regelwerke.  Erzeuge aus dem bereitgestellten PDF ein deutschsprachiges Multiple-Choice-Quiz. Wenn du kein PDF bekommen hast, frage zuerst danach, bevor du weiter machst.
Erstelle für das Quiz eine Frage und vier mögliche Antworten. Jede Frage hat genau eine richtige und drei falsche Antwortoptionen, eine Erklärung (warum richtig/falsch) und eine präzise Quellenangabe (Titel, Version, Kapitel/Abschnitt, Seitenzahl).  
Gib ausschließlich ein einzelnes JSON-Objekt zurück, das exakt dem unten definierten JSON-Schema entspricht. Erstelle um die 100 Fragen, wenn möglich und biete diese nach Schema Validierung als Download an. Sollte die Quelle nicht mehr Fragen hergeben dann erstelle so viele wie sinnvoll. Wenn du für 100 Fragen mehrmals den Prozess starten musst, dann teile diese Aufgabe in Zwischenschritte auf und liefere den ersten Inhalt vom Ergebnis "quiz.json" und fahre dann in einer zweiten Antwort Nahtlos fort.

### Dateien

- schema.json – JSON-Schema (Draft-07) für die Validierung der Quiz-Ausgabe.
- example.json – Beispielausgabe, die dem Schema entspricht.

### Anforderungen an die Fragen

- Factual only: Nur Informationen verwenden, die eindeutig im PDF stehen.  
- Fragetypen: Definitionen, Regeln, Schwellenwerte, Verfahren, Ausnahmen, Fristen, Verantwortlichkeiten.  
- Optionen: Immer 4, eine korrekt (`correctIndex`), drei plausible Distraktoren.  
- Erklärung: 1–3 Sätze, erklärt richtig und falsch.  
- Quelle: Muss Seitenzahl und Kapitel/Artikel enthalten.  
- Sprache: Deutsch, neutral, klar.  
- Abdeckung: Fragen über mehrere Kapitel streuen.  
- Qualitätscheck: Keine Dubletten, keine Tippfehler, keine Mehrdeutigkeiten.

### Weitere Anforderungen

- Schwierigkeitsmix: leicht/mittel/schwer  
- Tags hinzufügen (z. B. „Definition“, „Frist“, „Regel“)  
- Jede Quelle muss Seitenzahl + Kapitel enthalten  
- Output nur JSON

### Arbeitsablauf

1. PDF-Inhalt analysieren, relevante Wissensbits identifizieren.  
2. Frage formulieren.  
3. Richtige Antwort extrahieren.  
4. 3 Distraktoren erstellen (plausibel, aber falsch).  
5. Erklärung schreiben (warum richtig & warum falsch).  
6. Quelle formatieren (Titel, Version, Kapitel/Artikel, Seitenzahl).  
7. Validieren gegen `schema.json`.

### Output

Da wir etwa 100 Fragen anstreben, gehe folgendermaßen vor:

- Extrahiere relevante Inhalte (Definitionen, Regeln, Fristen, Verfahren, Verantwortlichkeiten) aus deinem Regelwerk.
- Baue Multiple-Choice-Fragen mit 4 Optionen, davon 1 richtig.
- Jede Frage erhält eine Erklärung und eine präzise Quelle (Titel, Version, Kapitel/Abschnitt, Seite).
- Halte dich strikt an das bereitgestellte schema.json.
- Erstelle, wegen der Gesamtlänge und Umfang, das Ergebnis in Batches (z. B. 20–30 Fragen pro Antwort).

Starte jetzt mit den ersten/nächsten 20 Fragen im quiz.json-Format. Danach fahre mit dem nächsten Block fort, bis wir die 100 erreicht haben. Biete die json als download an - wegen der Länge ist es ist nicht nötig sie im Chat auszugeben. Los geht's :)

## 3. Erstelle banner.png

[KATEGORIE_NAME] entspricht einem Quiz für Kategorie <Sport> und Thema <Handball>:

Erstelle ein kreatives, cooles und ansprechendes Banner für [KATEGORIE_NAME] als Logo/Header-Bild für ein Quiz zu diesem Thema.

### Design-Anforderungen

- Format: Breites Banner-Format (Verhältnis idealerweise 4:1)
- Auflösung: Mindestens 1200x300px für scharfe Darstellung
- Stil: Modern, freundlich und professionell, passend zur Zielgruppe
- Farbschema: Harmonisch mit der Quiz-App (Primärfarbe #546de5)

### Inhaltliche Gestaltung

- Hauptelement: Thematische Illustration zum Quiz-Inhalt
- Titel: "[KATEGORIE_NAME]" prominent aber elegant integriert. Keine langweilige Schriftart. Lieber stylisch, spray-paint oder logo mit Textur oder Graffiti.

### Qualitätskriterien

- [ ] Lesbar in verschiedenen Größen (Desktop bis Mobile)
- [ ] Thematisch eindeutig zuordenbar
- [ ] Kein Text auf dem Bild nötig. Im Zweifel nur das Thema (ohne Quiz)

### Integration

Das Banner wird als `banner.png` im jeweiligen Quiz-Ordner gespeichert und über `<img src="banner.png" alt="[KATEGORIE] Quiz Logo" class="logo-image">` eingebunden.

## 4. HTML und CSS Anpassung

Passe die Titel und Icons für die neue Quiz-Kategorie "[KATEGORIE_NAME]" an.

### Schritt-für-Schritt Anleitung

#### HTML-Titel korrigieren

Ändere im `<head>`-Bereich der `index.html`:

```html
<!-- Vorher -->
<title>Quiz App</title>

<!-- Nachher -->  
<title>[KATEGORIE_NAME] Quiz</title>
```

#### Favicon anpassen

Ersetze das Favicon mit einem thematisch passenden Emoji:

```html
<!-- Beispiel für Fußball -->
<link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚽</text></svg>">

<!-- Beispiel für Gesetze -->
<link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚖️</text></svg>">
```

#### Lade-Animation anpassen

Ersetze das Lade-Symbol und den Text im `#loading`-Bereich:

```html
<!-- Vorher -->
<div class="loading-spinner">🎓</div>
<p>Quiz wird geladen...</p>

<!-- Nachher für Sport -->
<div class="loading-spinner">⚽</div>
<p>[KATEGORIE_NAME] Quiz wird geladen...</p>

<!-- Nachher für Gesetze -->
<div class="loading-spinner">⚖️</div>
<p>[KATEGORIE_NAME] Quiz wird geladen...</p>
```

### Emoji-Zuordnung

| Kategorie | Emoji | Beispiel |
|-----------|-------|----------|
| Fußball | ⚽ | `Fußball Quiz` |
| Basketball | 🏀 | `Basketball Quiz` |
| Tennis | 🎾 | `Tennis Quiz` |
| Handball | 🤾 | `Handball Quiz` |  
| Hobbyhorsing | 🐎 | `Hobbyhorsing Quiz` |
| LLM Engineering | 🤖 | `LLM Engineer Quiz` |
| Gesetze | ⚖️ | `Gesetze Quiz` |
| Recht | ⚖️ | `Recht Quiz` |
| Verfassung | 📜 | `Verfassung Quiz` |
| Strafrecht | ⚖️ | `Strafrecht Quiz` |
| Zivilrecht | 📋 | `Zivilrecht Quiz` |

### Checkliste

- [ ] `<title>` Tag im `<head>` angepasst
- [ ] Favicon mit thematischem Emoji ersetzt
- [ ] Lade-Symbol (loading-spinner) angepasst  
- [ ] Lade-Text aktualisiert
- [ ] Browser-Test durchgeführt (Tab-Titel und Favicon prüfen)

### Betroffene Dateien

- `index.html` - Alle Titel und Icon-Änderungen, Analytics-Script bereits integriert
- `styles.css` - Bounce-Animation bereits vorhanden

## 5. Checks

### Schema validieren

Mit einem Validator prüfen, ob erzeugte JSON-Dateien korrekt sind.  
Beispiel (Node.js mit AJV):  

```bash
npx ajv validate -s schema.json -d example.json
```

### Config validieren

```bash
python update_config.py
```
