#!/usr/bin/env python3
"""
Quiz Config Generator - Automatische Validierung und Korrektur
Scannt automatisch alle Kategorien und Quiz-Ordner, validiert die Struktur 
und behebt Inkonsistenzen zwischen Dateisystem und config.json
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

class QuizConfigGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.config_file = self.base_path / "config.json"
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        
        # Standard-Icons für verschiedene Kategorien
        self.default_category_icons = {
            "ai": "fa-robot",
            "sport": "fa-football", 
            "science": "fa-microscope",
            "history": "fa-landmark",
            "geography": "fa-globe",
            "math": "fa-calculator",
            "literature": "fa-book",
            "music": "fa-music",
            "art": "fa-palette",
            "technology": "fa-laptop-code",
            "movies": "fa-film",
            "games": "fa-gamepad",
            "food": "fa-utensils",
            "nature": "fa-leaf",
            "languages": "fa-language",
            "business": "fa-briefcase",
            "medicine": "fa-stethoscope",
            "chemistry": "fa-flask",
            "physics": "fa-atom",
            "biology": "fa-dna",
            "default": "fa-question-circle"
        }
        
        # Deutsche Namen für Kategorien
        self.default_category_names = {
            "ai": "Künstliche Intelligenz",
            "sport": "Sport",
            "science": "Wissenschaft",
            "history": "Geschichte",
            "geography": "Geographie",
            "math": "Mathematik",
            "literature": "Literatur",
            "music": "Musik",
            "art": "Kunst",
            "technology": "Technologie",
            "movies": "Film & TV",
            "games": "Spiele",
            "food": "Kulinarik",
            "nature": "Natur",
            "languages": "Sprachen",
            "business": "Business",
            "medicine": "Medizin",
            "chemistry": "Chemie",
            "physics": "Physik",
            "biology": "Biologie"
        }

    def scan_directories(self) -> Dict[str, List[str]]:
        """Scannt alle Verzeichnisse und findet Kategorien und Quiz"""
        categories = {}
        
        print("🔍 Scanne Verzeichnisse...")
        
        # Durchsuche alle Ordner im Basisverzeichnis
        for item in self.base_path.iterdir():
            if not item.is_dir():
                continue
            # Überspringe Ordner die mit "_" beginnen oder spezielle Ordner
            if item.name.startswith("_") or item.name.startswith(".") or item.name in ["__pycache__", "node_modules"]:
                print(f"⏭️  Überspringe: {item.name}")
                continue
            
            category_name = item.name
            quiz_list = []
            
            print(f"📂 Gefundene Kategorie: {category_name}")
            
            # Durchsuche Quiz in der Kategorie
            for quiz_item in item.iterdir():
                if not quiz_item.is_dir():
                    continue
                    
                # Überspringe Ordner die mit "_" beginnen
                if quiz_item.name.startswith("_"):
                    print(f"   ⏭️  Überspringe Ordner: {quiz_item.name}")
                    continue
                if quiz_item.name.startswith("."):
                    continue
                quiz_json_path = quiz_item / "quiz.json"
                if quiz_json_path.exists():
                    quiz_list.append(quiz_item.name)
                    print(f"   ✅ Gefundenes Quiz: {quiz_item.name}")
                else:
                    print(f"   ⚠️  Kein Quiz (quiz.json fehlt): {quiz_item.name}")
            
            if quiz_list:  # Nur Kategorien mit mindestens einem Quiz hinzufügen
                categories[category_name] = quiz_list
        
        return categories

    def load_existing_config(self) -> Dict[str, Any]:
        """Lädt die bestehende config.json falls vorhanden"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print("📄 Bestehende config.json geladen")
                return config
            except Exception as e:
                print(f"⚠️  Fehler beim Laden der bestehenden config.json: {e}")
                return self.create_default_config()
        else:
            print("📄 Keine bestehende config.json gefunden, erstelle neue")
            return self.create_default_config()

    def create_default_config(self) -> Dict[str, Any]:
        """Erstellt eine Standard-Konfiguration"""
        return {
            "app": {
                "title": "Quiz Center",
                "description": "Entdecke und teste dein Wissen in verschiedenen Kategorien",
                "version": "1.0.0",
                "author": "Quiz Center Team",
                "language": "de"
            },
            "settings": {
                "autoDiscovery": True,
                "defaultQuizSettings": {
                    "shuffleQuestions": True,
                    "shuffleOptions": True,
                    "showExplanations": True,
                    "timePerQuestionSec": 60
                }
            },
            "categories": {},
            "categoryIcons": self.default_category_icons.copy(),
            "categoryNames": self.default_category_names.copy()
        }

    def update_config(self, scanned_categories: Dict[str, List[str]]) -> Dict[str, Any]:
        """Aktualisiert die Konfiguration mit gescannten Daten"""
        config = self.load_existing_config()
        
        print("\n🔄 Aktualisiere Konfiguration...")
        
        # Bestehende Kategorien sichern
        existing_categories = config.get("categories", {})
        
        # Neue Kategorien hinzufügen/aktualisieren
        for category_key, quiz_list in scanned_categories.items():
            if category_key in existing_categories:
                # Bestehende Kategorie: Quiz-Liste aktualisieren, aber Metadaten beibehalten
                existing_categories[category_key]["quiz"] = sorted(quiz_list)
                print(f"   ✏️  Aktualisiert: {category_key} ({len(quiz_list)} Quiz)")
            else:
                # Neue Kategorie: Vollständig erstellen
                existing_categories[category_key] = {
                    "name": self.default_category_names.get(category_key, category_key.title()),
                    "icon": self.default_category_icons.get(category_key, self.default_category_icons["default"]),
                    "description": f"Quiz und Wissen rund um {self.default_category_names.get(category_key, category_key)}",
                    "quiz": sorted(quiz_list)
                }
                print(f"   ➕ Neu hinzugefügt: {category_key} ({len(quiz_list)} Quiz)")
        
        # Entferne Kategorien die keine Quiz mehr haben
        categories_to_remove = []
        for category_key in existing_categories:
            if category_key not in scanned_categories:
                categories_to_remove.append(category_key)
        
        for category_key in categories_to_remove:
            del existing_categories[category_key]
            print(f"   ❌ Entfernt (keine Quiz gefunden): {category_key}")
        
        config["categories"] = existing_categories
        
        # Icons und Namen aktualisieren (neue hinzufügen, bestehende beibehalten)
        config["categoryIcons"].update(self.default_category_icons)
        config["categoryNames"].update(self.default_category_names)
        
        return config

    def save_config(self, config: Dict[str, Any]) -> None:
        """Speichert die Konfiguration in config.json"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Konfiguration gespeichert: {self.config_file}")
        except Exception as e:
            print(f"\n❌ Fehler beim Speichern: {e}")
            raise

    def generate_statistics(self, config: Dict[str, Any]) -> None:
        """Zeigt Statistiken über die generierte Konfiguration"""
        categories = config.get("categories", {})
        total_categories = len(categories)
        total_quiz = sum(len(cat.get("quiz", [])) for cat in categories.values())
        
        print(f"\n📊 Statistiken:")
        print(f"   📁 Kategorien: {total_categories}")
        print(f"   🎯 Quiz gesamt: {total_quiz}")
        print(f"\n📋 Kategorien-Übersicht:")
        
        for category_key, category_data in categories.items():
            quiz_count = len(category_data.get("quiz", []))
            category_name = category_data.get("name", category_key)
            icon = category_data.get("icon", "❓")
            print(f"   {icon} {category_name}: {quiz_count} Quiz")
            
            # Zeige Quiz-Namen bei wenigen Quiz
            if quiz_count <= 5:
                quiz_names = category_data.get("quiz", [])
                for quiz_name in quiz_names:
                    print(f"      • {quiz_name}")

    def run(self) -> None:
        """Hauptfunktion: Scannt Verzeichnisse und generiert config.json"""
        print("🚀 Quiz Config Generator gestartet\n")
        
        try:
            # Verzeichnisse scannen
            scanned_categories = self.scan_directories()
            
            if not scanned_categories:
                print("⚠️  Keine Quiz-Kategorien gefunden!")
                return
            
            # Konfiguration aktualisieren
            config = self.update_config(scanned_categories)
            
            # Konfiguration speichern
            self.save_config(config)
            
            # Statistiken anzeigen
            self.generate_statistics(config)
            
            print(f"\n🎉 Fertig! Die config.json wurde erfolgreich aktualisiert.")
            print(f"💡 Tipp: Starte den Browser neu (F5) um die Änderungen zu sehen.")
            
        except Exception as e:
            print(f"\n❌ Fehler: {e}")
            raise

    def validate_and_fix_config(self) -> bool:
        """Validiert config.json gegen Dateisystem und behebt Inkonsistenzen"""
        print("🔍 Validiere Konfiguration gegen Dateisystem...")
        
        # Aktuelle Struktur scannen
        actual_structure = self.scan_directories()
        
        # Config laden
        config = self.load_existing_config()
        config_categories = config.get("categories", {})
        
        # Inkonsistenzen finden
        inconsistencies_found = False
        
        for category_key, category_data in config_categories.items():
            config_quiz = set(category_data.get("quiz", []))
            actual_quiz = set(actual_structure.get(category_key, []))
            
            # Quiz in config.json aber nicht im Dateisystem
            missing_in_fs = config_quiz - actual_quiz
            if missing_in_fs:
                print(f"❌ Kategorie '{category_key}': Quiz in config.json nicht im Dateisystem gefunden: {list(missing_in_fs)}")
                self.fixes_applied.append(f"Entfernt verwaiste Quiz aus '{category_key}': {list(missing_in_fs)}")
                inconsistencies_found = True
            
            # Quiz im Dateisystem aber nicht in config.json
            missing_in_config = actual_quiz - config_quiz
            if missing_in_config:
                print(f"⚠️  Kategorie '{category_key}': Quiz im Dateisystem nicht in config.json: {list(missing_in_config)}")
                self.fixes_applied.append(f"Hinzugefügt fehlende Quiz zu '{category_key}': {list(missing_in_config)}")
                inconsistencies_found = True
        
        # Kategorien in config.json aber nicht im Dateisystem
        config_cats = set(config_categories.keys())
        actual_cats = set(actual_structure.keys())
        missing_cat_in_fs = config_cats - actual_cats
        
        if missing_cat_in_fs:
            print(f"❌ Kategorien in config.json nicht im Dateisystem: {list(missing_cat_in_fs)}")
            self.fixes_applied.append(f"Entfernt verwaiste Kategorien: {list(missing_cat_in_fs)}")
            inconsistencies_found = True
        
        # Neue Kategorien im Dateisystem
        new_cats = actual_cats - config_cats
        if new_cats:
            print(f"✅ Neue Kategorien gefunden: {list(new_cats)}")
            self.fixes_applied.append(f"Hinzugefügt neue Kategorien: {list(new_cats)}")
            inconsistencies_found = True
        
        return inconsistencies_found

    def run_full_cycle(self) -> None:
        """Führt kompletten Validierungs- und Korrekturzyklus durch"""
        print("🚀 Quiz Config Generator - Automatische Validierung gestartet\n")
        
        try:
            # 1. Initiale Validierung
            needs_update = self.validate_and_fix_config()
            
            if not needs_update:
                print("✅ Konfiguration ist bereits korrekt - keine Änderungen nötig!")
                return
            
            print("\n🔧 Behebe gefundene Inkonsistenzen...")
            
            # 2. Verzeichnisse neu scannen
            scanned_categories = self.scan_directories()
            
            if not scanned_categories:
                print("⚠️  Keine Quiz-Kategorien gefunden!")
                return
            
            # 3. Konfiguration komplett neu generieren
            config = self.update_config(scanned_categories)
            
            # 4. Konfiguration speichern
            self.save_config(config)
            
            # 5. Finale Validierung
            print("\n🔍 Finale Validierung...")
            final_issues = self.validate_and_fix_config()
            
            if final_issues:
                print("❌ Noch immer Probleme gefunden - manuelle Prüfung erforderlich!")
                return
            
            # 6. Statistiken anzeigen
            self.generate_statistics(config)
            
            # 7. Zusammenfassung der Korrekturen
            if self.fixes_applied:
                print(f"\n🔧 Angewendete Korrekturen:")
                for fix in self.fixes_applied:
                    print(f"   • {fix}")
            
            print(f"\n🎉 Konfiguration erfolgreich validiert und korrigiert!")
            print(f"💡 Tipp: Browser aktualisieren (F5) um Änderungen zu sehen.")
            
        except Exception as e:
            print(f"\n❌ Fehler: {e}")
            raise

def main():
    """Einstiegspunkt für das Script - läuft automatisch ohne Parameter"""
    import sys
    
    # Optional: Pfad als Argument übergeben
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    generator = QuizConfigGenerator(base_path)
    generator.run_full_cycle()

if __name__ == "__main__":
    main()