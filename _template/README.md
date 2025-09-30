# Quiz Template

Dieses Verzeichnis enthält die Template-Dateien für neue Quiz-Erstellung.

## 📁 Verzeichnis-Struktur

```
_template/
├── copyme/           # 📦 Template-Dateien zum Kopieren
│   ├── index.html    # 🌐 HTML-Struktur (neutral, bereit zum Anpassen)
│   ├── script.js     # ⚡ JavaScript-Logik (vollständig funktional)
│   ├── styles.css    # 🎨 CSS-Styles (alle Features included)
│   ├── fontawesome.css # 🎯 Icon-Bibliothek
│   └── quiz.json     # 📄 Beispiel-Quiz-Daten
├── schema.json       # ✅ JSON-Schema für Validierung
├── example.json      # 📋 Beispiel für korrekte quiz.json
└── instruction.md    # 📖 Komplette Anleitung
```

## 🚀 Template-Features

### ✅ **Vollständig vorbereitet:**
- **Responsive Design** - Funktioniert auf Desktop und Mobile
- **Erweiterte Feedback-Formatierung** - Strukturierte Antwort-Darstellung
- **Bounce-Animation** - Moderne Loading-Symbole
- **Emoji-basierte Icons** - Einfach anpassbare Favicons und Loader
- **Alle CSS-Klassen** - Tags, Difficulty-Level, Source-Formatting

### 🔧 **Anpassungen erforderlich:**
- **Titel** - `"Quiz App"` → `"[KATEGORIE] Quiz"`
- **Favicon** - `❓` → thematisches Emoji
- **Lade-Symbol** - `❓` → thematisches Emoji
- **quiz.json** - Beispiel-Daten durch echte Fragen ersetzen

## 💡 **Verwendung**

```bash
# 1. Template kopieren
cp -r _template/copyme/* [kategorie]/[neues_quiz]/

# 2. Config aktualisieren  
python update_config.py

# 3. Anpassungen nach instruction.md
```

## 📋 **Qualitätssicherung**

Das Template wurde gegen alle bestehenden Quiz abgeglichen und enthält:
- ✅ Alle aktuellen CSS-Features
- ✅ Erweiterte JavaScript-Funktionalität  
- ✅ Moderne Emoji-Icons statt FontAwesome
- ✅ Strukturiertes Feedback-System
- ✅ Responsive Mobile-Support

**Status**: ✅ Bereit für Production