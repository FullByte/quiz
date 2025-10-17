#!/usr/bin/env python3
"""
Quiz Statistics Generator
Sammelt Statistiken über alle verfügbaren Quiz und speichert sie in /web/stats.json
"""

import json
import os
from pathlib import Path
from datetime import datetime

class QuizStatsGenerator:
    def __init__(self):
        self.base_path = Path('.')
        self.stats_file = Path('stats.json')
        
    def collect_stats(self):
        """Sammelt alle Quiz-Statistiken"""
        print("Sammle Quiz-Statistiken...")
        
        # Lade config.json
        config_path = self.base_path / 'config.json'
        if not config_path.exists():
            raise FileNotFoundError("config.json nicht gefunden")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        stats = {
            'generated_at': datetime.now().isoformat(),
            'categories': {},
            'summary': {
                'total_categories': 0,
                'total_quizzes': 0,
                'total_questions': 0,
                'categories_with_quizzes': 0
            }
        }
        
        total_questions = 0
        categories_with_quizzes = 0
        
        # Durchlaufe alle Kategorien
        for category_key, category_data in config.get('categories', {}).items():
            category_stats = {
                'name': category_data.get('name', category_key),
                'icon': category_data.get('icon', 'fa-question'),
                'description': category_data.get('description', ''),
                'quiz_count': 0,
                'total_questions': 0,
                'quizzes': {}
            }
            
            quiz_count = 0
            
            # Durchlaufe alle Quiz in der Kategorie
            for quiz_name in category_data.get('quiz', []):
                quiz_path = self.base_path / category_key / quiz_name
                quiz_json_path = quiz_path / 'quiz.json'
                
                if quiz_json_path.exists():
                    try:
                        with open(quiz_json_path, 'r', encoding='utf-8') as f:
                            quiz_data = json.load(f)
                        
                        questions = quiz_data.get('quiz', {}).get('questions', [])
                        question_count = len(questions)
                        
                        # Quiz-Statistiken
                        quiz_stats = {
                            'title': quiz_data.get('quiz', {}).get('title', quiz_name),
                            'description': quiz_data.get('quiz', {}).get('description', ''),
                            'language': quiz_data.get('quiz', {}).get('language', 'de'),
                            'version': quiz_data.get('quiz', {}).get('version', '1.0'),
                            'question_count': question_count,
                            'difficulty_distribution': self._analyze_difficulty(questions),
                            'has_banner': (quiz_path / 'banner.png').exists(),
                            'last_modified': datetime.fromtimestamp(quiz_json_path.stat().st_mtime).isoformat()
                        }
                        
                        category_stats['quizzes'][quiz_name] = quiz_stats
                        category_stats['total_questions'] += question_count
                        total_questions += question_count
                        quiz_count += 1
                        
                        print(f"  OK {category_key}/{quiz_name}: {question_count} Fragen")
                        
                    except Exception as e:
                        print(f"  FEHLER beim Laden von {category_key}/{quiz_name}: {e}")
                        continue
                else:
                    print(f"  WARNUNG: Quiz-Datei nicht gefunden: {quiz_json_path}")
            
            category_stats['quiz_count'] = quiz_count
            
            if quiz_count > 0:
                categories_with_quizzes += 1
            
            stats['categories'][category_key] = category_stats
        
        # Berechne Gesamtanzahl der Quiz
        total_quizzes = sum(cat['quiz_count'] for cat in stats['categories'].values())
        
        # Zusammenfassung
        stats['summary'] = {
            'total_categories': len(config.get('categories', {})),
            'total_quizzes': total_quizzes,
            'total_questions': total_questions,
            'categories_with_quizzes': categories_with_quizzes,
            'average_questions_per_quiz': round(total_questions / max(1, total_quizzes), 1),
            'average_quizzes_per_category': round(total_quizzes / max(1, categories_with_quizzes), 1)
        }
        
        return stats
    
    def _analyze_difficulty(self, questions):
        """Analysiert die Schwierigkeitsverteilung der Fragen"""
        difficulty_counts = {'leicht': 0, 'mittel': 0, 'schwer': 0, 'unbekannt': 0}
        
        for question in questions:
            difficulty = question.get('difficulty', 'unbekannt')
            if difficulty in difficulty_counts:
                difficulty_counts[difficulty] += 1
            else:
                difficulty_counts['unbekannt'] += 1
        
        return difficulty_counts
    
    def save_stats(self, stats):
        """Speichert die Statistiken in stats.json"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"Statistiken gespeichert: {self.stats_file}")
    
    def print_summary(self, stats):
        """Druckt eine Zusammenfassung der Statistiken"""
        summary = stats['summary']
        
        print("\n" + "="*60)
        print("QUIZ-STATISTIKEN")
        print("="*60)
        print(f"Kategorien: {summary['total_categories']}")
        print(f"Quiz: {summary['total_quizzes']}")
        print(f"Fragen: {summary['total_questions']}")
        print(f"Durchschnittliche Fragen pro Quiz: {summary['average_questions_per_quiz']}")
        print(f"Durchschnittliche Quiz pro Kategorie: {summary['average_quizzes_per_category']}")
        print("="*60)
        
        # Detaillierte Kategorien-Übersicht
        print("\nKATEGORIEN:")
        for category_key, category_data in stats['categories'].items():
            if category_data['quiz_count'] > 0:
                print(f"  {category_data['name']}: {category_data['quiz_count']} Quiz, {category_data['total_questions']} Fragen")
    
    def run(self):
        """Hauptfunktion"""
        try:
            print("Starte Quiz-Statistik-Generator...")
            
            stats = self.collect_stats()
            self.save_stats(stats)
            self.print_summary(stats)
            
            print(f"\nStatistiken erfolgreich generiert!")
            print(f"Datei: {self.stats_file}")
            
        except Exception as e:
            print(f"Fehler beim Generieren der Statistiken: {e}")
            return 1
        
        return 0

if __name__ == '__main__':
    generator = QuizStatsGenerator()
    exit(generator.run())
