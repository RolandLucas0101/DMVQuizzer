/**
 * DMVNavigator NJ - New Jersey DMV Practice Test Application
 * Main application logic and state management
 */

// Application State
let currentQuestionIndex = 0;
let userAnswers = {};
let filteredQuestions = [];
let isReviewMode = false;
let testStartTime = null;
let testEndTime = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set up filtered questions (initially all questions)
    filteredQuestions = [...questions];
    
    // Shuffle questions for random order
    shuffleArray(filteredQuestions);
    
    // Initialize UI components
    updateProgressDisplay();
    setupEventListeners();
    
    console.log('DMVNavigator NJ initialized with', filteredQuestions.length, 'questions');
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (document.getElementById('test-screen').classList.contains('d-none')) return;
        
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                previousQuestion();
                break;
            case 'ArrowRight':
                e.preventDefault();
                nextQuestion();
                break;
            case '1':
            case '2':
            case '3':
            case '4':
                e.preventDefault();
                selectAnswer(parseInt(e.key) - 1);
                break;
        }
    });

    // Handle page visibility change
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            saveProgressToStorage();
        }
    });

    // Handle page unload
    window.addEventListener('beforeunload', function() {
        saveProgressToStorage();
    });
}

/**
 * Start the practice test
 */
function startTest() {
    testStartTime = new Date();
    showScreen('test-screen');
    loadQuestion(0);
    generateQuestionGrid();
    updateProgressDisplay();
    
    // Load saved progress if available
    loadProgressFromStorage();
}

/**
 * Show a specific screen
 */
function showScreen(screenId) {
    const screens = ['welcome-screen', 'test-screen', 'results-screen'];
    screens.forEach(screen => {
        document.getElementById(screen).classList.add('d-none');
    });
    document.getElementById(screenId).classList.remove('d-none');
}

/**
 * Load a question by index
 */
function loadQuestion(index) {
    if (index < 0 || index >= filteredQuestions.length) return;
    
    currentQuestionIndex = index;
    const question = filteredQuestions[index];
    
    // Update question display
    document.getElementById('question-number').textContent = `Question ${index + 1}`;
    document.getElementById('question-category').textContent = question.category;
    document.getElementById('question-text').textContent = question.question;
    
    // Update progress text
    document.getElementById('progress-text').textContent = `Question ${index + 1} of ${filteredQuestions.length}`;
    
    // Generate answer options
    generateAnswerOptions(question, index);
    
    // Update navigation buttons
    updateNavigationButtons();
    
    // Update question grid
    updateQuestionGrid();
    
    // Update progress
    updateProgressDisplay();
    
    // Scroll to top
    window.scrollTo(0, 0);
}

/**
 * Generate answer options for a question
 */
function generateAnswerOptions(question, questionIndex) {
    const container = document.getElementById('answer-options');
    container.innerHTML = '';
    
    const letters = ['A', 'B', 'C', 'D'];
    const userAnswer = userAnswers[questionIndex];
    const isAnswered = userAnswer !== undefined;
    
    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'answer-option';
        optionDiv.onclick = () => selectAnswer(index);
        
        // Add selection state
        if (userAnswer === index) {
            optionDiv.classList.add('selected');
        }
        
        // Add correct/incorrect state if answered and in review mode
        if (isAnswered && isReviewMode) {
            optionDiv.classList.add('disabled');
            if (index === question.correct) {
                optionDiv.classList.add('correct');
            } else if (userAnswer === index && userAnswer !== question.correct) {
                optionDiv.classList.add('incorrect');
            }
        }
        
        optionDiv.innerHTML = `
            <span class="answer-letter">${letters[index]}</span>
            <span class="answer-text">${option}</span>
        `;
        
        container.appendChild(optionDiv);
    });
    
    // Show feedback if answered
    if (isAnswered) {
        showAnswerFeedback(question, userAnswer);
    } else {
        hideAnswerFeedback();
    }
}

/**
 * Select an answer for the current question
 */
function selectAnswer(answerIndex) {
    if (isReviewMode) return;
    
    const question = filteredQuestions[currentQuestionIndex];
    userAnswers[currentQuestionIndex] = answerIndex;
    
    // Update UI
    generateAnswerOptions(question, currentQuestionIndex);
    updateQuestionGrid();
    updateProgressDisplay();
    
    // Save progress
    saveProgressToStorage();
    
    // Auto-advance after short delay
    setTimeout(() => {
        if (currentQuestionIndex < filteredQuestions.length - 1) {
            nextQuestion();
        }
    }, 1500);
}

/**
 * Show answer feedback
 */
function showAnswerFeedback(question, userAnswer) {
    const container = document.getElementById('answer-feedback');
    const isCorrect = userAnswer === question.correct;
    
    container.className = `alert ${isCorrect ? 'feedback-correct' : 'feedback-incorrect'}`;
    container.innerHTML = `
        <div class="d-flex align-items-start">
            <i class="fas ${isCorrect ? 'fa-check-circle' : 'fa-times-circle'} me-3 mt-1"></i>
            <div>
                <h6 class="mb-2">${isCorrect ? 'Correct!' : 'Incorrect'}</h6>
                <p class="mb-0">${question.explanation}</p>
                ${!isCorrect ? `<p class="mb-0 mt-2"><strong>Correct answer:</strong> ${String.fromCharCode(65 + question.correct)}. ${question.options[question.correct]}</p>` : ''}
            </div>
        </div>
    `;
    
    container.classList.remove('d-none');
}

/**
 * Hide answer feedback
 */
function hideAnswerFeedback() {
    document.getElementById('answer-feedback').classList.add('d-none');
}

/**
 * Navigate to next question
 */
function nextQuestion() {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
        loadQuestion(currentQuestionIndex + 1);
    }
}

/**
 * Navigate to previous question
 */
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        loadQuestion(currentQuestionIndex - 1);
    }
}

/**
 * Jump to a specific question
 */
function jumpToQuestion(index) {
    if (index >= 0 && index < filteredQuestions.length) {
        loadQuestion(index);
    }
}

/**
 * Update navigation buttons
 */
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.disabled = currentQuestionIndex === filteredQuestions.length - 1;
    
    // Update next button text
    if (currentQuestionIndex === filteredQuestions.length - 1) {
        nextBtn.innerHTML = '<i class="fas fa-flag-checkered me-1"></i>Finish';
        nextBtn.onclick = showResults;
    } else {
        nextBtn.innerHTML = 'Next<i class="fas fa-chevron-right ms-1"></i>';
        nextBtn.onclick = nextQuestion;
    }
}

/**
 * Generate question navigation grid
 */
function generateQuestionGrid() {
    const container = document.getElementById('question-grid');
    container.innerHTML = '';
    
    filteredQuestions.forEach((_, index) => {
        const button = document.createElement('button');
        button.className = 'question-btn';
        button.textContent = index + 1;
        button.onclick = () => jumpToQuestion(index);
        button.title = `Question ${index + 1}`;
        
        container.appendChild(button);
    });
    
    updateQuestionGrid();
}

/**
 * Update question grid state
 */
function updateQuestionGrid() {
    const buttons = document.querySelectorAll('.question-btn');
    
    buttons.forEach((button, index) => {
        button.className = 'question-btn';
        
        // Current question
        if (index === currentQuestionIndex) {
            button.classList.add('current');
        }
        
        // Answered questions
        const userAnswer = userAnswers[index];
        if (userAnswer !== undefined) {
            const question = filteredQuestions[index];
            if (userAnswer === question.correct) {
                button.classList.add('answered');
            } else {
                button.classList.add('incorrect');
            }
        }
    });
}

/**
 * Update progress display
 */
function updateProgressDisplay() {
    const totalQuestions = filteredQuestions.length;
    const answeredCount = Object.keys(userAnswers).length;
    const correctCount = getCorrectAnswersCount();
    const incorrectCount = answeredCount - correctCount;
    
    // Progress bar
    const progressPercent = (answeredCount / totalQuestions) * 100;
    document.getElementById('progress-bar').style.width = progressPercent + '%';
    document.getElementById('progress-percent').textContent = Math.round(progressPercent) + '%';
    
    // Score counters
    document.getElementById('correct-count').textContent = correctCount;
    document.getElementById('incorrect-count').textContent = incorrectCount;
}

/**
 * Get count of correct answers
 */
function getCorrectAnswersCount() {
    let correctCount = 0;
    Object.entries(userAnswers).forEach(([questionIndex, userAnswer]) => {
        const question = filteredQuestions[parseInt(questionIndex)];
        if (question && userAnswer === question.correct) {
            correctCount++;
        }
    });
    return correctCount;
}

/**
 * Filter questions by category
 */
function filterQuestions() {
    const selectedCategory = document.getElementById('category-filter').value;
    
    if (selectedCategory === 'all') {
        filteredQuestions = [...questions];
    } else {
        filteredQuestions = questions.filter(q => q.category === selectedCategory);
    }
    
    // Shuffle filtered questions
    shuffleArray(filteredQuestions);
    
    // Reset state
    currentQuestionIndex = 0;
    userAnswers = {};
    
    // Reload interface
    generateQuestionGrid();
    loadQuestion(0);
    updateProgressDisplay();
}

/**
 * Show test results
 */
function showResults() {
    testEndTime = new Date();
    isReviewMode = true;
    
    const totalQuestions = filteredQuestions.length;
    const answeredCount = Object.keys(userAnswers).length;
    const correctCount = getCorrectAnswersCount();
    const incorrectCount = answeredCount - correctCount;
    const unansweredCount = totalQuestions - answeredCount;
    const scorePercent = Math.round((correctCount / totalQuestions) * 100);
    const passed = scorePercent >= 80;
    
    // Update results display
    document.getElementById('final-score').textContent = scorePercent + '%';
    document.getElementById('final-correct').textContent = correctCount;
    document.getElementById('final-incorrect').textContent = incorrectCount;
    document.getElementById('final-unanswered').textContent = unansweredCount;
    
    // Update result message and icon
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    
    if (passed) {
        resultIcon.className = 'fas fa-trophy text-warning mb-3';
        resultTitle.textContent = 'Congratulations! You Passed!';
        resultTitle.className = 'result-pass';
        resultMessage.textContent = `You scored ${scorePercent}% and passed the New Jersey DMV practice test. You're ready for the real test!`;
    } else {
        resultIcon.className = 'fas fa-times-circle text-danger mb-3';
        resultTitle.textContent = 'Keep Studying';
        resultTitle.className = 'result-fail';
        resultMessage.textContent = `You scored ${scorePercent}%. You need 80% to pass. Review the questions and try again.`;
    }
    
    // Generate category breakdown
    generateCategoryBreakdown();
    
    // Show results screen
    showScreen('results-screen');
    
    // Clear saved progress
    clearProgressFromStorage();
}

/**
 * Generate category performance breakdown
 */
function generateCategoryBreakdown() {
    const container = document.getElementById('category-breakdown');
    const categories = {};
    
    // Group questions by category
    filteredQuestions.forEach((question, index) => {
        if (!categories[question.category]) {
            categories[question.category] = {
                total: 0,
                correct: 0,
                answered: 0
            };
        }
        
        categories[question.category].total++;
        
        const userAnswer = userAnswers[index];
        if (userAnswer !== undefined) {
            categories[question.category].answered++;
            if (userAnswer === question.correct) {
                categories[question.category].correct++;
            }
        }
    });
    
    // Generate breakdown HTML
    container.innerHTML = '';
    Object.entries(categories).forEach(([category, stats]) => {
        const percentage = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
        const progressColor = percentage >= 80 ? 'bg-success' : percentage >= 60 ? 'bg-warning' : 'bg-danger';
        
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'category-item';
        categoryDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">${category}</h6>
                <span class="badge ${progressColor}">${percentage}%</span>
            </div>
            <div class="category-progress mb-2">
                <div class="category-progress-bar ${progressColor}" style="width: ${percentage}%"></div>
            </div>
            <small class="text-muted">
                ${stats.correct} correct out of ${stats.total} questions
                ${stats.answered < stats.total ? ` (${stats.total - stats.answered} unanswered)` : ''}
            </small>
        `;
        
        container.appendChild(categoryDiv);
    });
}

/**
 * Review questions mode
 */
function reviewQuestions() {
    isReviewMode = true;
    showScreen('test-screen');
    loadQuestion(0);
    
    // Find first incorrect answer
    const firstIncorrect = Object.entries(userAnswers).find(([index, answer]) => {
        const question = filteredQuestions[parseInt(index)];
        return question && answer !== question.correct;
    });
    
    if (firstIncorrect) {
        loadQuestion(parseInt(firstIncorrect[0]));
    }
}

/**
 * Reset the test
 */
function resetTest() {
    // Reset state
    currentQuestionIndex = 0;
    userAnswers = {};
    isReviewMode = false;
    testStartTime = null;
    testEndTime = null;
    
    // Reshuffle questions
    shuffleArray(filteredQuestions);
    
    // Reset UI
    document.getElementById('category-filter').value = 'all';
    
    // Clear saved progress
    clearProgressFromStorage();
    
    // Show welcome screen
    showScreen('welcome-screen');
}

/**
 * Go back to home screen
 */
function goHome() {
    resetTest();
}

/**
 * Utility function to shuffle array
 */
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

/**
 * Save progress to localStorage
 */
function saveProgressToStorage() {
    const progress = {
        currentQuestionIndex,
        userAnswers,
        filteredQuestions: filteredQuestions.map(q => q.id), // Save only IDs
        testStartTime,
        timestamp: new Date().toISOString()
    };
    
    try {
        localStorage.setItem('dmvnavigator_nj_progress', JSON.stringify(progress));
    } catch (error) {
        console.warn('Could not save progress to localStorage:', error);
    }
}

/**
 * Load progress from localStorage
 */
function loadProgressFromStorage() {
    try {
        const saved = localStorage.getItem('dmvnavigator_nj_progress');
        if (!saved) return;
        
        const progress = JSON.parse(saved);
        
        // Check if saved progress is recent (within 24 hours)
        const savedTime = new Date(progress.timestamp);
        const now = new Date();
        const hoursDiff = (now - savedTime) / (1000 * 60 * 60);
        
        if (hoursDiff > 24) {
            clearProgressFromStorage();
            return;
        }
        
        // Restore progress
        if (progress.userAnswers) {
            userAnswers = progress.userAnswers;
        }
        
        if (progress.currentQuestionIndex !== undefined) {
            loadQuestion(progress.currentQuestionIndex);
        }
        
        if (progress.testStartTime) {
            testStartTime = new Date(progress.testStartTime);
        }
        
        updateProgressDisplay();
        updateQuestionGrid();
        
    } catch (error) {
        console.warn('Could not load progress from localStorage:', error);
        clearProgressFromStorage();
    }
}

/**
 * Clear progress from localStorage
 */
function clearProgressFromStorage() {
    try {
        localStorage.removeItem('dmvnavigator_nj_progress');
    } catch (error) {
        console.warn('Could not clear progress from localStorage:', error);
    }
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        startTest,
        selectAnswer,
        nextQuestion,
        previousQuestion,
        showResults,
        resetTest
    };
}
