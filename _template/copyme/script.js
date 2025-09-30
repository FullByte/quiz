// Main JavaScript File

class QuizApp {
  constructor() {
    this.quizData = null;
    this.currentQuestionIndex = 0;
    this.score = 0;
    this.totalQuestions = 10;
    this.selectedQuestions = [];
    this.userAnswers = [];
    this.isQuizActive = false;

    // DOM Elements
    this.screens = {
      start: document.getElementById("start-screen"),
      quiz: document.getElementById("quiz-screen"),
      results: document.getElementById("results-screen"),
      pdf: document.getElementById("pdf-screen"),
    };

    this.elements = {
      // Start screen
      quizTitle: document.getElementById("quiz-title"),
      quizDescription: document.getElementById("quiz-description"),
      startBtn: document.getElementById("start-quiz-btn"),
      viewPdfBtn: document.getElementById("view-pdf-btn"),
      questionPoolCount: document.getElementById("question-pool-count"),

      // Quiz screen
      currentQuestion: document.getElementById("current-question"),
      totalQuestionsSpan: document.getElementById("total-questions"),
      progressFill: document.getElementById("progress-fill"),
      currentScore: document.getElementById("current-score"),
      maxScore: document.getElementById("max-score"),
      questionText: document.getElementById("question-text"),
      optionsContainer: document.getElementById("options-container"),
      feedbackContainer: document.getElementById("feedback-container"),
      feedbackContent: document.getElementById("feedback-content"),
      feedbackIcon: document.getElementById("feedback-icon"),
      feedbackText: document.getElementById("feedback-text"),
      explanationText: document.getElementById("explanation-text"),
      nextBtn: document.getElementById("next-question-btn"),
      nextBtnText: document.getElementById("next-btn-text"),

      // Results screen
      finalScore: document.getElementById("final-score"),
      finalTotal: document.getElementById("final-total"),
      scorePercentage: document.getElementById("score-percentage"),
      scoreMessage: document.getElementById("score-message"),
      resultsList: document.getElementById("results-list"),
      restartBtn: document.getElementById("restart-quiz-btn"),

      // PDF screen
      closePdfBtn: document.getElementById("close-pdf-btn"),

      // Loading
      loading: document.getElementById("loading"),
    };

    this.init();
  }

  async init() {
    this.showLoading();

    try {
      await this.loadQuizData();
      this.setupEventListeners();
      this.updateUI();
      this.hideLoading();
    } catch (error) {
      console.error("Error initializing quiz:", error);
      this.showError(
        "Fehler beim Laden des Quiz. Bitte versuchen Sie es erneut.",
      );
    }
  }

  async loadQuizData() {
    try {
      const response = await fetch("./quiz.json");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      this.quizData = data.quiz;
      this.totalQuestions = Math.min(
        this.totalQuestions,
        this.quizData.questions.length,
      );

      // Update UI with quiz data
      if (this.elements.quizTitle) {
        this.elements.quizTitle.textContent = this.quizData.title;
      }

      // Update browser tab title
      if (this.quizData.title) {
        document.title = this.quizData.title;
      }

      // Update description with dynamic question count
      if (this.elements.quizDescription && this.quizData.description) {
        const questionCount = this.quizData.questions.length;
        const description = this.quizData.description.replace(
          "{questionCount}",
          questionCount,
        );
        this.elements.quizDescription.textContent = description;
      }

      // Update PDF links with dynamic filename
      if (
        this.quizData.sourceDocument &&
        this.quizData.sourceDocument.pdfFilename
      ) {
        this.updatePdfLinks(this.quizData.sourceDocument.pdfFilename);
      }

      // Update question pool count immediately
      this.updateQuestionPoolCount();

      // quiz data loaded
    } catch (error) {
      console.error("Error loading quiz data:", error);
      throw error;
    }
  }

  updateQuestionPoolCount() {
    if (this.quizData && this.elements.questionPoolCount) {
      const totalAvailableQuestions = this.quizData.questions.length;
      this.elements.questionPoolCount.textContent = totalAvailableQuestions;
    }
  }

  updatePdfLinks(pdfFilename) {
    // Update all PDF download links - target by class and download attribute
    const pdfDownloadLinks = document.querySelectorAll(
      "a[download].btn-outline, a[download]",
    );
    pdfDownloadLinks.forEach((link) => {
      link.href = pdfFilename;
    });

    // Update PDF viewer iframe specifically
    const pdfFrame = document.getElementById("pdf-frame");
    if (pdfFrame) {
      pdfFrame.src = pdfFilename;
    }
  }

  setupEventListeners() {
    // Start button
    this.elements.startBtn?.addEventListener("click", () => this.startQuiz());

    // PDF buttons
    this.elements.viewPdfBtn?.addEventListener("click", () => this.showPdf());
    this.elements.closePdfBtn?.addEventListener("click", () => this.closePdf());

    // Next question button
    this.elements.nextBtn?.addEventListener("click", () => this.nextQuestion());

    // Restart button
    this.elements.restartBtn?.addEventListener("click", () =>
      this.restartQuiz(),
    );

    // Keyboard navigation
    document.addEventListener("keydown", (e) => this.handleKeyPress(e));
  }

  handleKeyPress(e) {
    // Check which screen is currently active
    const isOnStartScreen = this.screens.start.classList.contains("active");
    const isOnResultsScreen = this.screens.results.classList.contains("active");

    // Only handle keys during quiz or on start/results screen
    if (!this.isQuizActive && !isOnResultsScreen && !isOnStartScreen) return;

    // Prevent default behavior for handled keys
    const handledKeys = [
      "1",
      "2",
      "3",
      "4",
      "a",
      "b",
      "c",
      "d",
      "A",
      "B",
      "C",
      "D",
      "Enter",
      "n",
      "N",
    ];
    if (handledKeys.includes(e.key)) {
      e.preventDefault();
    }

    // Handle Enter on start screen to start quiz
    if (isOnStartScreen && e.key === "Enter") {
      this.startQuiz();
      return;
    }

    // Handle Enter on results screen to restart quiz
    if (isOnResultsScreen && e.key === "Enter") {
      this.restartQuiz();
      return;
    }

    // Quiz navigation (only during active quiz)
    if (!this.isQuizActive) return;

    // Handle number keys 1-4 for option selection
    if (e.key >= "1" && e.key <= "4") {
      const optionIndex = parseInt(e.key) - 1;
      const options = document.querySelectorAll(".option");
      if (
        options[optionIndex] &&
        !options[optionIndex].classList.contains("disabled")
      ) {
        this.selectOption(optionIndex);
      }
    }

    // Handle letter keys a-d for option selection (case insensitive)
    if (["a", "b", "c", "d", "A", "B", "C", "D"].includes(e.key)) {
      const letter = e.key.toLowerCase();
      const optionIndex = letter.charCodeAt(0) - "a".charCodeAt(0); // Convert a=0, b=1, c=2, d=3
      const options = document.querySelectorAll(".option");
      if (
        options[optionIndex] &&
        !options[optionIndex].classList.contains("disabled")
      ) {
        this.selectOption(optionIndex);
      }
    }

    // Handle Enter and 'n' for next question
    if (
      (e.key === "Enter" || e.key === "n" || e.key === "N") &&
      !this.elements.feedbackContainer.classList.contains("hidden")
    ) {
      this.nextQuestion();
    }
  }

  startQuiz() {
    this.showLoading();

    // Reset quiz state
    this.currentQuestionIndex = 0;
    this.score = 0;
    this.userAnswers = [];
    this.isQuizActive = true;

    // Select and shuffle questions
    this.selectQuestions();

    // Update UI
    this.elements.totalQuestionsSpan.textContent = this.totalQuestions;
    this.elements.maxScore.textContent = this.totalQuestions;
    this.elements.finalTotal.textContent = this.totalQuestions;

    setTimeout(() => {
      this.hideLoading();
      this.showScreen("quiz");
      this.displayQuestion();
    }, 500);
  }

  selectQuestions() {
    const allQuestions = [...this.quizData.questions];

    if (this.quizData.settings.shuffleQuestions) {
      this.shuffleArray(allQuestions);
    }

    this.selectedQuestions = allQuestions.slice(0, this.totalQuestions);
  }

  shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }

  displayQuestion() {
    const question = this.selectedQuestions[this.currentQuestionIndex];

    // Update progress
    this.updateProgress();

    // Display question text
    this.elements.questionText.textContent = question.text;

    // Create options
    this.createOptions(question);

    // Hide feedback
    this.elements.feedbackContainer.classList.add("hidden");

    // Update question counter
    this.elements.currentQuestion.textContent = this.currentQuestionIndex + 1;
  }

  createOptions(question) {
    this.elements.optionsContainer.innerHTML = "";

    const options = [...question.options];
    const correctIndex = question.correctIndex;

    // Create mapping for shuffled options
    let optionMapping = options.map((option, index) => ({
      text: option,
      originalIndex: index,
    }));

    if (this.quizData.settings.shuffleOptions) {
      this.shuffleArray(optionMapping);
    }

    optionMapping.forEach((option, index) => {
      const optionElement = this.createOptionElement(
        option.text,
        index,
        option.originalIndex === correctIndex,
      );
      this.elements.optionsContainer.appendChild(optionElement);
    });
  }

  createOptionElement(text, index, isCorrect) {
    const optionDiv = document.createElement("div");
    optionDiv.className = "option";
    optionDiv.dataset.index = index;
    optionDiv.dataset.correct = isCorrect;

    const letterSpan = document.createElement("span");
    letterSpan.className = "option-letter";
    letterSpan.textContent = String.fromCharCode(65 + index); // A, B, C, D

    const textSpan = document.createElement("span");
    textSpan.className = "option-text";
    textSpan.textContent = text;

    optionDiv.appendChild(letterSpan);
    optionDiv.appendChild(textSpan);

    optionDiv.addEventListener("click", () => this.selectOption(index));

    return optionDiv;
  }

  selectOption(selectedIndex) {
    const options = document.querySelectorAll(".option");

    // Check if options are already disabled (answer already selected)
    if (options[0]?.classList.contains("disabled")) return;

    // Disable all options
    options.forEach((option) => option.classList.add("disabled"));

    // Find correct option
    let correctOption = null;
    let selectedOption = options[selectedIndex];

    options.forEach((option) => {
      if (option.dataset.correct === "true") {
        correctOption = option;
        option.classList.add("correct");
      }
    });

    // Mark selected option
    selectedOption.classList.add("selected");

    const isCorrect = selectedOption.dataset.correct === "true";

    if (!isCorrect) {
      selectedOption.classList.add("incorrect");
    }

    // Update score
    if (isCorrect) {
      this.score++;
      this.elements.currentScore.textContent = this.score;
    }

    // Store user answer
    const question = this.selectedQuestions[this.currentQuestionIndex];
    this.userAnswers.push({
      question: question,
      selectedIndex: selectedIndex,
      selectedText: selectedOption.querySelector(".option-text").textContent,
      correctIndex: Array.from(options).findIndex(
        (opt) => opt.dataset.correct === "true",
      ),
      correctText: correctOption.querySelector(".option-text").textContent,
      isCorrect: isCorrect,
    });

    // Show feedback
    this.showFeedback(isCorrect, question);
  }

  showFeedback(isCorrect, question) {
    const feedbackContent = this.elements.feedbackContent;
    const feedbackIcon = this.elements.feedbackIcon;
    const feedbackText = this.elements.feedbackText;
    const explanationText = this.elements.explanationText;
    const lastAnswer = this.userAnswers[this.userAnswers.length - 1];

    // Reset classes
    feedbackContent.className = "feedback-content";

    const statusSymbol = isCorrect ? "✅" : "❌";
    const statusText = isCorrect ? "Richtig!" : "Leider falsch!";

    if (isCorrect) {
      feedbackContent.classList.add("correct");
    } else {
      feedbackContent.classList.add("incorrect");
    }

    // Build structured HTML for better formatting
    let htmlContent = '';
    
    const correctAnswerText = lastAnswer?.correctText || "-";
    htmlContent += `<div class="feedback-answer">
      <strong>Richtige Antwort:</strong> ${correctAnswerText}
    </div>`;
    
    htmlContent += `<div class="feedback-explanation">
      <strong>Erklärung:</strong> ${question.explanation}
    </div>`;

    const sourceText = this.formatSource(question.source);
    if (sourceText) {
      htmlContent += `<div class="feedback-source">
        <i class="fas fa-book"></i>
        <span><strong>Quelle:</strong> ${sourceText}</span>
      </div>`;
    }

    const tags = question.tags;
    if (tags && Array.isArray(tags) && tags.length > 0) {
      htmlContent += `<div class="feedback-tags">
        <span class="tags-label">
          <i class="fas fa-tags"></i>
          <strong>Tags:</strong>
        </span>`;
      tags.forEach(tag => {
        htmlContent += `<span class="feedback-tag">${tag}</span>`;
      });
      htmlContent += `</div>`;
    }

    const difficultyLabel = this.formatDifficultyLabel(question.difficulty);
    if (difficultyLabel) {
      const levelClass = question.difficulty?.toLowerCase() || 'medium';
      htmlContent += `<div class="feedback-level">
        <span class="level-label">
          <i class="fas fa-signal"></i>
          <strong>Level:</strong>
        </span>
        <span class="level-chip ${levelClass}">${difficultyLabel}</span>
      </div>`;
    }

    feedbackIcon.innerHTML = "";
    feedbackText.textContent = `${statusSymbol} ${statusText}`;
    explanationText.innerHTML = htmlContent;

    if (this.currentQuestionIndex < this.totalQuestions - 1) {
      this.elements.nextBtnText.textContent = "Nächste Frage";
    } else {
      this.elements.nextBtnText.textContent = "Ergebnis anzeigen";
    }

    this.elements.feedbackContainer.classList.remove("hidden");
  }

  nextQuestion() {
    if (this.currentQuestionIndex < this.totalQuestions - 1) {
      this.currentQuestionIndex++;
      this.displayQuestion();
    } else {
      this.showResults();
    }
  }

  showResults() {
    this.isQuizActive = false;

    // Calculate percentage
    const percentage = Math.round((this.score / this.totalQuestions) * 100);

    // Update results UI
    this.elements.finalScore.textContent = this.score;
    this.elements.scorePercentage.textContent = `${percentage}%`;

    // Set score message
    let message = "";
    if (percentage >= 90) {
        message =
        "Ausgezeichnet! Du beherrschst den Quizinhalt souverän! 🏆";
    } else if (percentage >= 70) {
      message =
        "Sehr gut! Du verfügst über ein solides Verständnis der Inhalte! 🎉";
    } else if (percentage >= 50) {
      message =
        "Nicht schlecht! Mit etwas mehr Übung festigst du dein Wissen! 📚";
    } else {
      message =
        "Das war ein guter Anfang! Wiederhole die Inhalte und versuche es erneut! 💪";
    }

    this.elements.scoreMessage.textContent = message;

    // Generate detailed results
    this.generateDetailedResults();

    // Show results screen
    this.showScreen("results");

    // Scroll to top
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  generateDetailedResults() {
    this.elements.resultsList.innerHTML = "";

    this.userAnswers.forEach((answer, index) => {
      const resultItem = document.createElement("div");
      resultItem.className = `result-item ${answer.isCorrect ? "correct" : "incorrect"}`;

      const statusSymbol = answer.isCorrect ? "✅" : "❌";
      const statusText = answer.isCorrect ? "Richtig" : "Falsch";
      const lines = [];
      lines.push(`Richtige Antwort: ${answer.correctText}`);
      lines.push(`Erklärung: ${answer.question.explanation}`);

      const sourceText = this.formatSource(answer.question.source);
      if (sourceText) {
        lines.push(`Quelle: ${sourceText}`);
      }

      const tagsText = this.formatTagsPlain(answer.question.tags);
      if (tagsText) {
        lines.push(`Tags: ${tagsText}`);
      }

      const difficultyLabel = this.formatDifficultyLabel(answer.question.difficulty);
      if (difficultyLabel) {
        lines.push(`Level: ${difficultyLabel}`);
      }

      resultItem.innerHTML = `
                <div class="result-question">
                    <strong>Frage ${index + 1}:</strong> ${answer.question.text}
                </div>
                <div class="result-answer">
                    <span class="answer-status ${answer.isCorrect ? "correct" : "incorrect"}">
                        ${statusSymbol} ${statusText}
                    </span>
                    - Deine Antwort: <strong>${answer.selectedText}</strong>
                </div>
                <div class="result-explanation">
                    ${lines.join("<br>")}
                </div>
            `;

      this.elements.resultsList.appendChild(resultItem);
    });
  }

  updateProgress() {
    const progressPercentage =
      (this.currentQuestionIndex / this.totalQuestions) * 100;
    this.elements.progressFill.style.width = `${progressPercentage}%`;
  }

  restartQuiz() {
    this.showScreen("start");

    // Reset UI
    this.elements.currentScore.textContent = "0";
    this.elements.progressFill.style.width = "0%";
  }

  showPdf() {
    // Load PDF into iframe only when requested
    const pdfFrame = document.getElementById("pdf-frame");
    const pdfFilename =
      this.quizData?.sourceDocument?.pdfFilename ||
      "LLM_Engineers_Handbook.pdf";

    if (pdfFrame && !pdfFrame.src) {
      pdfFrame.src = pdfFilename;
    }

    this.showScreen("pdf");

    // PDF viewer opened
  }

  closePdf() {
    this.showScreen("start");

    // PDF viewer closed
  }

  showScreen(screenName) {
    // Hide all screens
    Object.values(this.screens).forEach((screen) => {
      screen.classList.remove("active");
    });

    // Show selected screen
    if (this.screens[screenName]) {
      this.screens[screenName].classList.add("active");
    }
  }

  showLoading() {
    this.elements.loading?.classList.remove("hidden");
  }

  hideLoading() {
    this.elements.loading?.classList.add("hidden");
  }

  showError(message) {
    this.hideLoading();
    alert(message); // Simple error handling - could be improved with custom modal
  }

  updateUI() {
    // Update any initial UI elements based on quiz data
    if (this.quizData) {
      document.title = `${this.quizData.title}`;

      // Update question pool count
      const totalAvailableQuestions = this.quizData.questions.length;
      if (this.elements.questionPoolCount) {
        this.elements.questionPoolCount.textContent = totalAvailableQuestions;
      }

      // total questions loaded
    }
  }

  formatSource(source) {
    if (!source || typeof source !== "object") {
      return "";
    }

    const parts = [];

    if (source.citation) {
      parts.push(source.citation);
    }

    if (source.chapter) {
      parts.push(`Kapitel: ${source.chapter}`);
    }

    if (source.articleOrSection) {
      parts.push(`Abschnitt: ${source.articleOrSection}`);
    }

    if (source.pages) {
      parts.push(source.pages);
    }

    return parts.join(" | ");
  }

  formatTags(tags) {
    if (!Array.isArray(tags) || tags.length === 0) {
      return "";
    }

    return tags.join(", ");
  }

  formatTagsPlain(tags) {
    if (!Array.isArray(tags) || tags.length === 0) {
      return "";
    }

    return tags.join(", ");
  }


  formatDifficultyLabel(difficulty) {
    if (!difficulty) return "";

    const normalized = difficulty.toLowerCase();
    if (normalized === "leicht") return "Leicht";
    if (normalized === "mittel") return "Mittel";
    if (normalized === "schwer") return "Schwer";
    return difficulty;
  }
}

// Utility Functions
// removed unused debounce utility

// Initialize quiz when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Check for required APIs
  if (!window.fetch) {
    alert(
      "Ihr Browser unterstützt nicht alle erforderlichen Funktionen. Bitte verwenden Sie einen moderneren Browser.",
    );
    return;
  }

  // Add back button to navigation overview
  addBackButtonToQuizPage();

  // Initialize the quiz app
    window.quizApp = new QuizApp();
});

// Add back button to quiz page
function addBackButtonToQuizPage() {
  const backButton = document.createElement('button');
  backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Zurück zur Übersicht';
  backButton.className = 'back-button';
  backButton.style.cssText = `
    position: fixed;
    top: 20px;
    left: 20px;
    background: rgba(255, 255, 255, 0.95);
    border: none;
    padding: 12px 18px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: #333;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    z-index: 1000;
    display: flex;
    align-items: center;
    gap: 8px;
  `;
  
  backButton.addEventListener('click', () => {
    // Navigate back to the main quiz overview
    const currentPath = window.location.pathname;
    if (currentPath.includes('/ai/') || currentPath.includes('/sport/')) {
      window.location.href = '../../index.html';
    } else {
      window.location.href = '/index.html';
    }
  });
  
  backButton.addEventListener('mouseenter', () => {
    backButton.style.background = 'rgba(255, 255, 255, 1)';
    backButton.style.transform = 'translateY(-2px)';
    backButton.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.15)';
  });
  
  backButton.addEventListener('mouseleave', () => {
    backButton.style.background = 'rgba(255, 255, 255, 0.95)';
    backButton.style.transform = 'translateY(0)';
    backButton.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
  });
  
  document.body.appendChild(backButton);
}

// removed visibilitychange listener (not used)

// removed global error listeners for production minimalism (browser default handling applies)

// Export for potential use in other scripts
if (typeof module !== "undefined" && module.exports) {
  module.exports = { QuizApp };
}
