// Quiz Center - Hauptskript für automatische Erkennung aller Quiz

class QuizCenter {
    constructor() {
        this.categories = new Map();
        this.config = null;
        this.stats = null;
        
        this.init();
    }

    async init() {
        try {
            await this.loadConfig();
            await this.loadStats();
            await this.loadAllQuiz();
            this.renderCategories();
            this.hideLoading();
        } catch (error) {
            console.error('Fehler beim Initialisieren:', error);
            this.showError('Fehler beim Laden der Quiz-Daten: ' + error.message);
        }
    }

    async loadConfig() {
        try {
            const response = await fetch('config.json');
            if (!response.ok) {
                throw new Error(`Fehler beim Laden der Konfiguration: HTTP ${response.status}`);
            }
            
            this.config = await response.json();
            console.log('✅ Konfiguration geladen:', this.config);
            
            // Kategorien aus Config laden
            for (const [categoryKey, categoryData] of Object.entries(this.config.categories)) {
                this.categories.set(categoryKey, {
                    name: categoryData.name,
                    icon: categoryData.icon,
                    description: categoryData.description || '',
                    quiz: new Map()
                });
            }
            
            // App-Titel aktualisieren falls in Config definiert
            if (this.config.app?.title) {
                document.title = this.config.app.title;
                const headerTitle = document.querySelector('.header h1');
                if (headerTitle) {
                    headerTitle.innerHTML = `<i class="fas fa-graduation-cap"></i> ${this.config.app.title}`;
                }
            }
            
            // App-Beschreibung aktualisieren
            if (this.config.app?.description) {
                const headerDescription = document.querySelector('.header p');
                if (headerDescription) {
                    headerDescription.textContent = this.config.app.description;
                }
            }
            
        } catch (error) {
            console.error('Fehler beim Laden der Konfiguration:', error);
            throw new Error('Konfigurationsdatei (config.json) konnte nicht geladen werden.');
        }
    }

    async loadStats() {
        try {
            const response = await fetch('stats.json');
            if (!response.ok) {
                console.warn('Stats-Datei nicht gefunden, verwende Fallback-Berechnung');
                this.stats = null;
                return;
            }
            
            this.stats = await response.json();
            console.log('✅ Statistiken geladen:', this.stats.summary);
            
        } catch (error) {
            console.warn('Fehler beim Laden der Statistiken:', error);
            this.stats = null;
        }
    }

    // Kategorien werden jetzt aus config.json geladen - diese Methode ist nicht mehr erforderlich

    async loadAllQuiz() {
        const loadPromises = [];
        
        for (const [categoryKey, categoryData] of this.categories) {
            // Lade nur die in der Config definierten Quiz
            const configuredQuiz = this.config.categories[categoryKey]?.quiz || [];
            
            const quizPromises = configuredQuiz.map(async (quizName) => {
                try {
                    const quizData = await this.loadQuizData(categoryKey, quizName);
                    if (quizData) {
                        categoryData.quiz.set(quizName, quizData);
                        console.log(`✅ Quiz geladen: ${categoryKey}/${quizName}`);
                    }
                } catch (error) {
                    console.warn(`❌ Quiz ${quizName} in Kategorie ${categoryKey} konnte nicht geladen werden:`, error);
                }
            });
            
            loadPromises.push(...quizPromises);
        }

        await Promise.all(loadPromises);
        console.log(`📊 Insgesamt ${this.getTotalQuizCount()} Quiz in ${this.categories.size} Kategorien geladen.`);
    }

    getTotalQuizCount() {
        let total = 0;
        for (const [, categoryData] of this.categories) {
            total += categoryData.quiz.size;
        }
        return total;
    }

    // Automatische Quiz-Erkennung entfernt - Quiz werden jetzt aus config.json geladen

    async getKnownQuizForCategory(category) {
        // Versuche automatisch alle Quiz-Ordner in einer Kategorie zu finden
        const knownQuiz = {
            'ai': ['LLM-Enginee'],
            'sport': ['basketball']
        };
        
        // Füge hier weitere bekannte Quiz hinzu oder erweitere die Liste automatisch
        // Für neue Quiz einfach den Ordner erstellen - sie werden automatisch erkannt
        
        return knownQuiz[category] || [];
    }

    async loadQuizData(category, quizName) {
        try {
            const response = await fetch(`${category}/${quizName}/quiz.json`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            // Banner-Bild-URL bestimmen
            const bannerUrl = `${category}/${quizName}/banner.png`;
            
            // Anzahl der Fragen zählen
            const questionCount = data.quiz?.questions?.length || 0;
            
            return {
                ...data.quiz,
                category: category,
                quizName: quizName,
                bannerUrl: bannerUrl,
                path: `${category}/${quizName}/`,
                questionCount: questionCount
            };
        } catch (error) {
            console.error(`Fehler beim Laden von ${category}/${quizName}:`, error);
            return null;
        }
    }

    formatCategoryName(category) {
        // Kategorie-Namen werden jetzt aus config.json geladen
        return this.config?.categoryNames?.[category] || 
               this.config?.categories?.[category]?.name ||
               category.charAt(0).toUpperCase() + category.slice(1);
    }

    renderCategories() {
        const categoriesContainer = document.getElementById('categories');
        const categoryCountElement = document.getElementById('categoryCount');
        const quizCountElement = document.getElementById('quizCount');
        const questionCountElement = document.getElementById('questionCount');
        
        if (!categoriesContainer) return;

        // Verwende vorgefertigte Statistiken falls verfügbar
        let totalQuizCount = 0;
        let totalQuestionCount = 0;
        let categoriesHTML = '';

        if (this.stats && this.stats.summary) {
            // Verwende vorgefertigte Statistiken
            totalQuizCount = this.stats.summary.total_quizzes;
            totalQuestionCount = this.stats.summary.total_questions;
            categoryCountElement.textContent = this.stats.summary.total_categories;
            quizCountElement.textContent = totalQuizCount;
            questionCountElement.textContent = totalQuestionCount;
        } else {
            // Fallback: Berechne Statistiken selbst
            for (const [categoryKey, categoryData] of this.categories) {
                if (categoryData.quiz.size === 0) continue;
                
                totalQuizCount += categoryData.quiz.size;
                
                for (const [quizKey, quizData] of categoryData.quiz) {
                    if (quizData.questionCount) {
                        totalQuestionCount += quizData.questionCount;
                    }
                }
            }
            
            categoryCountElement.textContent = this.categories.size;
            quizCountElement.textContent = totalQuizCount;
            questionCountElement.textContent = totalQuestionCount;
        }

        // Generiere Kategorien-HTML
        for (const [categoryKey, categoryData] of this.categories) {
            if (categoryData.quiz.size === 0) continue; // Zeige nur Kategorien mit Quiz
            
            categoriesHTML += `
                <div class="category-accordion">
                    <div class="category-header" data-category="${categoryKey}">
                        <div class="category-main">
                            <div class="category-icon">
                                <i class="fas ${categoryData.icon}"></i>
                            </div>
                            <div class="category-info">
                                <h2>${categoryData.name}</h2>
                                <div class="category-description">${categoryData.description || ''}</div>
                                <div class="category-count">${categoryData.quiz.size} Quiz verfügbar</div>
                            </div>
                        </div>
                        <div class="category-toggle">
                            <i class="fas fa-chevron-down"></i>
                        </div>
                    </div>
                    <div class="category-content" id="content-${categoryKey}">
                        <div class="quiz-grid">
                            ${this.renderQuizCards(categoryData.quiz)}
                        </div>
                    </div>
                </div>
            `;
        }

        categoriesContainer.innerHTML = categoriesHTML;

        // Event Listener für Quiz-Karten und Akkordeon hinzufügen
        this.attachQuizCardListeners();
        this.attachAccordionListeners();
    }

    renderQuizCards(quizMap) {
        let cardsHTML = '';
        
        for (const [quizName, quizData] of quizMap) {
            const truncatedDescription = this.truncateText(quizData.description, 100);
            const questionCount = quizData.questions ? quizData.questions.length : 0;
            const titleWithCount = `${quizData.title} (${questionCount} Fragen)`;
            
            cardsHTML += `
                <div class="quiz-card" data-quiz-path="${quizData.path}">
                    <div class="quiz-banner">
                        <img src="${quizData.bannerUrl}" alt="${quizData.title}" 
                             onerror="this.style.display='none'; this.parentElement.innerHTML='<i class=\\'fas fa-graduation-cap\\'></i>';">
                    </div>
                    <div class="quiz-content">
                        <div class="quiz-title">${titleWithCount}</div>
                        <div class="quiz-description">${truncatedDescription}</div>
                        <div class="quiz-meta">
                            <span class="quiz-language">
                                <i class="fas fa-language"></i> ${quizData.language?.toUpperCase() || 'DE'}
                            </span>
                            <span class="quiz-version">v${quizData.version || '1.0'}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        return cardsHTML;
    }

    attachQuizCardListeners() {
        const quizCards = document.querySelectorAll('.quiz-card');
        
        quizCards.forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                const quizPath = card.dataset.quizPath;
                if (quizPath) {
                    window.location.href = quizPath;
                }
            });
            
            // Keyboard navigation
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
            
            // Mache Cards fokussierbar
            card.setAttribute('tabindex', '0');
        });
    }

    attachAccordionListeners() {
        const categoryHeaders = document.querySelectorAll('.category-header[data-category]');
        
        categoryHeaders.forEach(header => {
            header.addEventListener('click', (e) => {
                e.preventDefault();
                const categoryKey = header.getAttribute('data-category');
                const content = document.getElementById(`content-${categoryKey}`);
                const toggleIcon = header.querySelector('.category-toggle i');
                
                if (content && toggleIcon) {
                    const isExpanded = content.classList.contains('expanded');
                    
                    if (isExpanded) {
                        // Schließen
                        content.classList.remove('expanded');
                        toggleIcon.classList.remove('fa-chevron-up');
                        toggleIcon.classList.add('fa-chevron-down');
                        header.classList.remove('active');
                    } else {
                        // Öffnen
                        content.classList.add('expanded');
                        toggleIcon.classList.remove('fa-chevron-down');
                        toggleIcon.classList.add('fa-chevron-up');
                        header.classList.add('active');
                    }
                }
            });

            // Keyboard support
            header.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    header.click();
                }
            });

            // Mache Header fokussierbar
            header.setAttribute('tabindex', '0');
        });
    }

    truncateText(text, maxLength) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength).trim() + '...';
    }

    hideLoading() {
        const loading = document.getElementById('loading');
        const quizOverview = document.getElementById('quizOverview');
        
        if (loading) loading.style.display = 'none';
        if (quizOverview) quizOverview.style.display = 'block';
    }

    showError(message) {
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const errorMessage = document.getElementById('errorMessage');
        
        if (loading) loading.style.display = 'none';
        if (error) error.style.display = 'block';
        if (errorMessage) errorMessage.textContent = message;
    }
}

// Utility Funktionen
function addBackButtonToQuiz() {
    // Diese Funktion wird in den Quiz-Seiten verwendet
    const backButton = document.createElement('button');
    backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Zurück zur Übersicht';
    backButton.className = 'back-button';
    backButton.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        background: rgba(255, 255, 255, 0.9);
        border: none;
        padding: 10px 15px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        z-index: 1000;
    `;
    
    backButton.addEventListener('click', () => {
        window.location.href = '/';
    });
    
    backButton.addEventListener('mouseenter', () => {
        backButton.style.background = 'rgba(255, 255, 255, 1)';
        backButton.style.transform = 'translateY(-2px)';
    });
    
    backButton.addEventListener('mouseleave', () => {
        backButton.style.background = 'rgba(255, 255, 255, 0.9)';
        backButton.style.transform = 'translateY(0)';
    });
    
    document.body.appendChild(backButton);
}

// Initialisierung wenn DOM geladen ist
document.addEventListener('DOMContentLoaded', () => {
    // Nur auf der Hauptseite initialisieren (wenn categories Container vorhanden)
    if (document.getElementById('categories')) {
        new QuizCenter();
    }
});

// Export für andere Skripte
window.QuizCenter = QuizCenter;
window.addBackButtonToQuiz = addBackButtonToQuiz;