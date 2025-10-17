#!/usr/bin/env python3
"""
Quiz Banner Generator
Erstellt thematisch passende Banner für alle Quizze basierend auf instruction.md
"""

import os
import json
import requests
import base64
from typing import Dict, Optional
from PIL import Image
import io
from dotenv import load_dotenv

class BannerGenerator:
    def __init__(self, api_key: Optional[str] = None, service: str = "dalle"):
        self.api_key = api_key
        self.service = service
        self.config = self._load_config()
        self.banner_specs = self._load_banner_specs()
    
    def _load_config(self) -> Dict:
        """Lädt die Konfiguration aus config.json"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ config.json nicht gefunden")
            return {}
    
    def _load_banner_specs(self) -> Dict[str, Dict]:
        """Lädt die Banner-Spezifikationen basierend auf config.json Kategorien"""
        specs = {}
        
        # Lade Quizze aus config.json
        for category, data in self.config.get("categories", {}).items():
            for quiz in data.get("quiz", []):
                # Bestimme Kategorie-spezifische Eigenschaften
                if category == "ai":
                    specs[quiz] = {
                        "theme": f"{quiz} - Künstliche Intelligenz",
                        "colors": ["#546de5", "#3b82f6", "#60a5fa"],
                        "elements": ["Roboter", "KI-Symbol", "Technologie", "Daten"],
                        "style": "modern, technisch, futuristisch",
                        "emoji": "🤖"
                    }
                elif category == "sport":
                    specs[quiz] = {
                        "theme": f"{quiz} - Sport",
                        "colors": ["#059669", "#10b981", "#34d399"],
                        "elements": ["Sportgerät", "Bewegung", "Dynamik", "Aktivität"],
                        "style": "sportlich, dynamisch, aktiv",
                        "emoji": "⚽"
                    }
                elif category == "gesetze":
                    specs[quiz] = {
                        "theme": f"{quiz} - Rechtsvorschriften",
                        "colors": ["#7c2d12", "#dc2626", "#f87171"],
                        "elements": ["Gesetzbuch", "Waage", "Rechtssymbol", "Verfassung"],
                        "style": "rechtlich, seriös, professionell",
                        "emoji": "⚖️"
                    }
                elif category == "astro":
                    specs[quiz] = {
                        "theme": f"{quiz} - Astronomie",
                        "colors": ["#1e3a8a", "#3b82f6", "#60a5fa", "#93c5fd"],
                        "elements": ["Sterne", "Planeten", "Teleskop", "Galaxie", "Mond"],
                        "style": "kosmisch, mystisch, wissenschaftlich",
                        "emoji": "🌌"
                    }
                elif category == "lockpicking":
                    specs[quiz] = {
                        "theme": f"{quiz} - Lockpicking",
                        "colors": ["#2d2d2d", "#4a4a4a", "#666666", "#808080"],
                        "elements": ["Schloss", "Schlüssel", "Pick", "Tension Wrench", "Stifte"],
                        "style": "technisch, mechanisch, präzise",
                        "emoji": "🔓"
                    }
                elif category == "microsoft":
                    specs[quiz] = {
                        "theme": f"{quiz} - Microsoft Technologie",
                        "colors": ["#0078d4", "#106ebe", "#005a9e", "#ffffff"],
                        "elements": ["Microsoft Logo", "Cloud", "Server", "Code", "Azure"],
                        "style": "modern, professionell, technisch",
                        "emoji": "🪟"
                    }
        
        return specs
    
    def _compress_and_resize_image(self, image_bytes: bytes, output_path: str) -> None:
        """Komprimiert und reduziert die Auflösung des Bildes"""
        try:
            # Öffne das Bild
            image = Image.open(io.BytesIO(image_bytes))
            
            # Konvertiere von 1024x1024 zu 1200x300px (4:1 Verhältnis)
            target_size = (1200, 300)
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            
            # Konvertiere zu RGB falls nötig
            if image.mode in ('RGBA', 'LA', 'P'):
                # Für transparente Bilder: Verwende schwarzen Hintergrund statt weißem
                background = Image.new('RGB', image.size, (0, 0, 0))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Speichere mit Komprimierung
            image.save(output_path, 'PNG', optimize=True, quality=85)
            
        except (IOError, OSError, ValueError) as e:
            print(f"⚠️  Fehler bei Bildkomprimierung: {e}")
            # Fallback: Speichere Original
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
    
    def generate_banner_prompt(self, quiz_name: str) -> str:
        """Generiert einen detaillierten Prompt basierend auf instruction.md Kapitel 3"""
        spec = self.banner_specs.get(quiz_name, {})
        
        # Optimiert für GPT-Image-1: Einfacher, klarer Prompt
        prompt = f"""
        Simple banner design for {quiz_name} quiz header. 
        
        Requirements:
        - Clean background with no text
        - One simple thematic element only
        - No borders, no white space
        - Professional colors
        - Minimalist design
        
        Theme: {', '.join(spec.get('elements', ['Symbol', 'Illustration']))}
        Colors: {', '.join(spec.get('colors', ['#546de5']))}
        
        NO TEXT. NO BORDERS. SIMPLE BACKGROUND.
        """
        
        return prompt.strip()
    
    def generate_with_reference(self, quiz_name: str, output_path: str, reference_path: str = None) -> bool:
        """Generiert Banner mit Referenzbild"""
        prompt = self.generate_banner_prompt(quiz_name)
        
        # Verwende Template-Banner als Standard-Referenz
        if not reference_path:
            reference_path = "./_template/banner.png"
        
        if not os.path.exists(reference_path):
            print(f"Referenzbild nicht gefunden: {reference_path}")
            return self.generate_with_dalle(quiz_name, output_path)
        
        print(f"Verwende Referenzbild: {reference_path}")
        print("Sende Anfrage an OpenAI API...")
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            # Erweitere den Prompt für Referenzbild
            enhanced_prompt = f"""
            {prompt}
            
            Style Reference: Use the reference image as a style guide for:
            - Clean, minimal design approach
            - Professional banner layout
            - Appropriate text placement and typography
            - Color scheme and visual hierarchy
            - Overall composition and balance
            
            Create a similar clean, professional banner but with {quiz_name} theme instead.
            """
            
            print("Generiere Bild mit Referenz... (dies kann 30-60 Sekunden dauern)")
            
            with open(reference_path, "rb") as reference_file:
                result = client.images.edit(
                    model="gpt-image-1",
                    image=reference_file,
                    prompt=enhanced_prompt
                )
            
            print("Bild generiert, verarbeite Ergebnis...")
            
            # Verarbeite das Ergebnis
            if hasattr(result, 'data') and len(result.data) > 0:
                import base64
                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)
                
                # Komprimiere und konvertiere
                self._compress_and_resize_image(image_bytes, output_path)
                print(f"SUCCESS: Banner für {quiz_name} mit Referenz erstellt: {output_path}")
                return True
            else:
                print(f"ERROR: Keine gültige Antwort von API für {quiz_name}")
                return False
                
        except Exception as e:
            print(f"ERROR: Fehler bei Referenzbild-Generierung für {quiz_name}: {e}")
            print("Fallback zu Standard-Generierung...")
            return self.generate_with_dalle(quiz_name, output_path)
    
    def generate_with_dalle(self, quiz_name: str, output_path: str) -> bool:
        """Generiert Banner mit DALL-E API"""
        if not self.api_key:
            print("❌ Kein API-Key für DALL-E konfiguriert")
            return False
        
        prompt = self.generate_banner_prompt(quiz_name)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"  # GPT-Image-1 unterstützt andere Größen
        }
        
        try:
            print("Sende Anfrage an OpenAI API...")
            print("Generiere Bild... (dies kann 30-60 Sekunden dauern)")
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data,
                timeout=120
            )
            
            print("Bild generiert, verarbeite Ergebnis...")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response: {result}")  # Debug-Output
                
                # Prüfe ob 'url' oder 'b64_json' vorhanden ist
                if "data" in result and len(result["data"]) > 0:
                    if "url" in result["data"][0]:
                        image_url = result["data"][0]["url"]
                    elif "b64_json" in result["data"][0]:
                        # Handle base64 encoded image
                        import base64
                        image_data = base64.b64decode(result["data"][0]["b64_json"])
                        self._compress_and_resize_image(image_data, output_path)
                        print(f"Banner für {quiz_name} erstellt: {output_path}")
                        return True
                    else:
                        print(f"Keine gültige Bild-URL in API-Antwort: {result}")
                        return False
                else:
                    print(f"Keine Daten in API-Antwort: {result}")
                    return False
                
                # Lade das Bild herunter (nur wenn URL vorhanden)
                if 'image_url' in locals():
                    img_response = requests.get(image_url, timeout=60)
                    if img_response.status_code == 200:
                        # Komprimiere und reduziere Auflösung
                        self._compress_and_resize_image(img_response.content, output_path)
                        print(f"Banner für {quiz_name} erstellt: {output_path}")
                        return True
                    else:
                        print(f"Fehler beim Herunterladen des Bildes für {quiz_name}")
                        return False
            else:
                print(f"DALL-E API Fehler für {quiz_name}: {response.text}")
                return False
                
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"Fehler bei DALL-E Generation für {quiz_name}: {e}")
            return False
    
    def generate_with_stability(self, quiz_name: str, output_path: str) -> bool:
        """Generiert Banner mit Stability AI API"""
        if not self.api_key:
            print("❌ Kein API-Key für Stability AI konfiguriert")
            return False
        
        prompt = self.generate_banner_prompt(quiz_name)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 300,
            "width": 1200,
            "samples": 1,
            "steps": 30
        }
        
        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                image_data = result["artifacts"][0]["base64"]
                
                # Dekodiere und komprimiere das Bild
                image_bytes = base64.b64decode(image_data)
                self._compress_and_resize_image(image_bytes, output_path)
                print(f"✅ Banner für {quiz_name} erstellt: {output_path}")
                return True
            else:
                print(f"❌ Stability AI API Fehler für {quiz_name}: {response.text}")
                return False
                
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"❌ Fehler bei Stability AI Generation für {quiz_name}: {e}")
            return False
    
    def generate_banner(self, quiz_name: str, output_path: str, use_reference: bool = True) -> bool:
        """Generiert Banner mit dem konfigurierten Service"""
        # Versuche zuerst mit Referenzbild, falls gewünscht
        if use_reference and self.service == "dalle":
            success = self.generate_with_reference(quiz_name, output_path)
            if success:
                return True
            print("Referenzbild-Generierung fehlgeschlagen, verwende Standard-Methode...")
        
        # Standard-Generierung
        if self.service == "dalle":
            return self.generate_with_dalle(quiz_name, output_path)
        elif self.service == "stability":
            return self.generate_with_stability(quiz_name, output_path)
        else:
            print(f"❌ Unbekannter Service: {self.service}")
            return False
    
    def generate_all_banners(self, base_path: str = ".") -> None:
        """Generiert Banner für alle Quizze aus config.json"""
        print("Banner Generator gestartet")
        print("=" * 50)
        
        # Lade Quizze aus config.json
        quiz_paths = {}
        for category, data in self.config.get("categories", {}).items():
            for quiz in data.get("quiz", []):
                quiz_paths[quiz] = f"{base_path}/{category}/{quiz}/banner.png"
        
        success_count = 0
        total_count = len(quiz_paths)
        
        for quiz_name, output_path in quiz_paths.items():
            print(f"\nGeneriere Banner für: {quiz_name}")
            print(f"Ausgabe: {output_path}")
            
            # Erstelle Verzeichnis falls nicht vorhanden
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if self.generate_banner(quiz_name, output_path):
                success_count += 1
            else:
                print(f"Banner für {quiz_name} konnte nicht erstellt werden")
        
        print("\n" + "=" * 50)
        print(f"Ergebnis: {success_count}/{total_count} Banner erfolgreich erstellt")
        
        if success_count == total_count:
            print("Alle Banner erfolgreich generiert!")
        else:
            print("Einige Banner konnten nicht erstellt werden")

def main():
    """Hauptfunktion"""
    import sys
    
    print("Quiz Banner Generator")
    print("=" * 50)
    
    # Lade .env Datei
    load_dotenv()
    
    # Konfiguration
    api_key = os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("openai")
    service = os.getenv("AI_SERVICE", "dalle")  # "dalle" oder "stability"
    
    if not api_key:
        print("Kein API-Key gefunden!")
        print("Setzen Sie die Umgebungsvariable AI_API_KEY oder OPENAI_API_KEY")
        print("Beispiel: export AI_API_KEY='your-api-key-here'")
        print("Oder: set AI_API_KEY=your-api-key-here (Windows)")
        return
    
    print(f"API-Key konfiguriert")
    print(f"Service: {service}")
    
    # Banner Generator initialisieren
    generator = BannerGenerator(api_key=api_key, service=service)
    
    # Prüfe ob Quiz-Name als Parameter übergeben wurde
    if len(sys.argv) > 1:
        quiz_name = sys.argv[1]
        print(f"\nGeneriere Banner für: {quiz_name}")
        
        # Bestimme Kategorie und Pfad
        output_path = None
        for category, data in generator.config.get("categories", {}).items():
            if quiz_name in data.get("quiz", []):
                output_path = f"./{category}/{quiz_name}/banner.png"
                break
        
        if output_path:
            print(f"Ausgabe: {output_path}")
            # Erstelle Verzeichnis falls nicht vorhanden
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if generator.generate_banner(quiz_name, output_path):
                print(f"SUCCESS: Banner für {quiz_name} erfolgreich erstellt!")
            else:
                print(f"ERROR: Banner für {quiz_name} konnte nicht erstellt werden")
        else:
            print(f"ERROR: Quiz '{quiz_name}' nicht in config.json gefunden")
            print("Verfügbare Quizze:")
            for category, data in generator.config.get("categories", {}).items():
                for quiz in data.get("quiz", []):
                    print(f"  - {quiz}")
    else:
        print("\nVerwendung:")
        print("  python generate_banners.py <quiz_name>")
        print("\nVerfügbare Quizze:")
        for category, data in generator.config.get("categories", {}).items():
            for quiz in data.get("quiz", []):
                print(f"  - {quiz}")

if __name__ == "__main__":
    main()
