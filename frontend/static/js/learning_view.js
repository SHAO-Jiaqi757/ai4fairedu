/**
 * AI4FairEdu Learning View JavaScript
 * Handles all interactive functionality for the learning view page
 */

document.addEventListener('DOMContentLoaded', function() {
    // ===== View Switching =====
    initViewSwitching();
    
    // ===== Reading Modes =====
    initReadingModes();
    
    // ===== Text-to-Speech =====
    initTextToSpeech();
    
    // ===== Study Timer =====
    initStudyTimer();
    
    // ===== Notes Functionality =====
    initNotes();
    
    // ===== Feedback System =====
    initFeedback();
    
    // ===== Micro Units Progress =====
    initMicroUnitProgress();
});

/**
 * Initialize view switching between original, micro units, and simplified text
 */
function initViewSwitching() {
    const viewButtons = document.querySelectorAll('.view-selector button');
    const contentViews = document.querySelectorAll('.content-view');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and views
            viewButtons.forEach(btn => btn.classList.remove('active'));
            contentViews.forEach(view => view.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Show corresponding view
            const viewId = this.id.replace('toggle-', '') + '-view';
            document.getElementById(viewId).classList.add('active');
        });
    });
}

/**
 * Initialize reading modes (normal, focus, bionic)
 */
function initReadingModes() {
    const readingModeSelect = document.getElementById('reading-mode');
    const contentContainers = document.querySelectorAll('.content-container');
    
    readingModeSelect.addEventListener('change', function() {
        const mode = this.value;
        
        contentContainers.forEach(container => {
            container.classList.remove('focus-mode', 'bionic-mode');
            
            // Remove any previously applied bionic reading spans
            const bionicSpans = container.querySelectorAll('.bionic-span');
            bionicSpans.forEach(span => {
                const parent = span.parentNode;
                const text = span.textContent;
                const textNode = document.createTextNode(text);
                parent.replaceChild(textNode, span);
            });
            
            if (mode === 'focus') {
                container.classList.add('focus-mode');
            } else if (mode === 'bionic') {
                container.classList.add('bionic-mode');
                applyBionicReading(container);
            }
        });
    });
}

/**
 * Apply bionic reading to text content
 * Bolds the first half of each word to improve reading speed and focus
 */
function applyBionicReading(container) {
    const textNodes = getTextNodes(container);
    
    textNodes.forEach(node => {
        if (node.nodeValue.trim() === '') return;
        
        const words = node.nodeValue.split(' ');
        const bionicWords = words.map(word => {
            if (word.length <= 1) return word;
            
            const midPoint = Math.ceil(word.length / 2);
            const firstHalf = word.substring(0, midPoint);
            const secondHalf = word.substring(midPoint);
            
            return `<strong>${firstHalf}</strong>${secondHalf}`;
        });
        
        const span = document.createElement('span');
        span.classList.add('bionic-span');
        span.innerHTML = bionicWords.join(' ');
        node.parentNode.replaceChild(span, node);
    });
}

/**
 * Get all text nodes within a container
 */
function getTextNodes(node) {
    const textNodes = [];
    
    function getNodes(node) {
        if (node.nodeType === 3) { // Text node
            textNodes.push(node);
        } else {
            for (let i = 0; i < node.childNodes.length; i++) {
                getNodes(node.childNodes[i]);
            }
        }
    }
    
    getNodes(node);
    return textNodes;
}

/**
 * Initialize text-to-speech functionality
 */
function initTextToSpeech() {
    const playButton = document.getElementById('play-tts');
    const pauseButton = document.getElementById('pause-tts');
    const stopButton = document.getElementById('stop-tts');
    
    // Check if browser supports speech synthesis
    if ('speechSynthesis' in window) {
        const synth = window.speechSynthesis;
        let utterance = null;
        let currentText = '';
        
        playButton.addEventListener('click', function() {
            // Get text from active view
            const activeView = document.querySelector('.content-view.active');
            const textContainer = activeView.querySelector('.original-text') || 
                                  activeView.querySelector('.unit-content') || 
                                  activeView.querySelector('.simplified-content');
            
            if (textContainer) {
                const text = textContainer.textContent.trim();
                
                // If new text or no utterance, create new one
                if (text !== currentText || !utterance) {
                    currentText = text;
                    utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 1.0;
                    utterance.pitch = 1.0;
                }
                
                // If paused, resume, otherwise start new
                if (synth.paused) {
                    synth.resume();
                } else {
                    synth.speak(utterance);
                }
            }
        });
        
        pauseButton.addEventListener('click', function() {
            if (synth.speaking) {
                synth.pause();
            }
        });
        
        stopButton.addEventListener('click', function() {
            synth.cancel();
            utterance = null;
            currentText = '';
        });
    } else {
        // Hide TTS controls if not supported
        document.querySelector('.tool-group:has(#text-to-speech)').style.display = 'none';
    }
}

/**
 * Initialize study timer functionality
 */
function initStudyTimer() {
    const timerMinutes = document.getElementById('timer-minutes');
    const timerSeconds = document.getElementById('timer-seconds');
    const startTimerBtn = document.getElementById('start-timer');
    const pauseTimerBtn = document.getElementById('pause-timer');
    const resetTimerBtn = document.getElementById('reset-timer');
    const timerPresets = document.querySelectorAll('.timer-preset');
    
    let timer;
    let timeLeft = 25 * 60; // Default to 25 minutes
    let timerRunning = false;
    
    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        
        timerMinutes.textContent = minutes.toString().padStart(2, '0');
        timerSeconds.textContent = seconds.toString().padStart(2, '0');
    }
    
    function startTimer() {
        if (timerRunning) return;
        
        timerRunning = true;
        startTimerBtn.disabled = true;
        pauseTimerBtn.disabled = false;
        
        timer = setInterval(() => {
            timeLeft--;
            
            if (timeLeft <= 0) {
                clearInterval(timer);
                timerRunning = false;
                timeLeft = 0;
                
                // Play notification sound if available
                const audio = new Audio('/static/sounds/timer-end.mp3');
                audio.play().catch(err => {
                    console.log('Audio play failed:', err);
                });
                
                // Show notification
                showNotification('Time is up!', 'Your study session is complete.');
                
                startTimerBtn.disabled = false;
                pauseTimerBtn.disabled = true;
            }
            
            updateTimerDisplay();
        }, 1000);
    }
    
    function pauseTimer() {
        clearInterval(timer);
        timerRunning = false;
        startTimerBtn.disabled = false;
        pauseTimerBtn.disabled = true;
    }
    
    function resetTimer() {
        clearInterval(timer);
        timerRunning = false;
        timeLeft = 25 * 60;
        updateTimerDisplay();
        startTimerBtn.disabled = false;
        pauseTimerBtn.disabled = true;
    }
    
    startTimerBtn.addEventListener('click', startTimer);
    pauseTimerBtn.addEventListener('click', pauseTimer);
    resetTimerBtn.addEventListener('click', resetTimer);
    
    timerPresets.forEach(preset => {
        preset.addEventListener('click', function() {
            const minutes = parseInt(this.dataset.minutes);
            timeLeft = minutes * 60;
            updateTimerDisplay();
            
            if (timerRunning) {
                clearInterval(timer);
                startTimer();
            }
        });
    });
    
    // Initialize timer display
    updateTimerDisplay();
}

/**
 * Initialize notes functionality with local storage
 */
function initNotes() {
    const notesArea = document.getElementById('notes-area');
    const saveNotesBtn = document.getElementById('save-notes');
    const clearNotesBtn = document.getElementById('clear-notes');
    
    // Generate a unique key for this learning material
    const materialId = window.location.pathname.split('/').pop() || 'default';
    const storageKey = `learning_notes_${materialId}`;
    
    // Load saved notes if any
    const savedNotes = localStorage.getItem(storageKey);
    if (savedNotes) {
        notesArea.value = savedNotes;
    }
    
    // Auto-save notes every 30 seconds
    const autoSaveInterval = setInterval(() => {
        if (notesArea.value) {
            localStorage.setItem(storageKey, notesArea.value);
        }
    }, 30000);
    
    saveNotesBtn.addEventListener('click', function() {
        localStorage.setItem(storageKey, notesArea.value);
        showNotification('Success', 'Notes saved successfully!');
    });
    
    clearNotesBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear your notes?')) {
            notesArea.value = '';
            localStorage.removeItem(storageKey);
        }
    });
}

/**
 * Initialize feedback system
 */
function initFeedback() {
    const stars = document.querySelectorAll('.feedback-stars .star');
    const feedbackText = document.getElementById('feedback-text');
    const submitFeedbackBtn = document.getElementById('submit-feedback');
    let currentRating = 0;
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.dataset.rating);
            currentRating = rating;
            
            // Update star display
            stars.forEach(s => {
                const starRating = parseInt(s.dataset.rating);
                s.classList.toggle('active', starRating <= rating);
            });
        });
        
        // Hover effect
        star.addEventListener('mouseenter', function() {
            const rating = parseInt(this.dataset.rating);
            
            stars.forEach(s => {
                const starRating = parseInt(s.dataset.rating);
                if (starRating <= rating) {
                    s.classList.add('hover');
                }
            });
        });
        
        star.addEventListener('mouseleave', function() {
            stars.forEach(s => s.classList.remove('hover'));
        });
    });
    
    submitFeedbackBtn.addEventListener('click', function() {
        if (currentRating === 0) {
            showNotification('Error', 'Please select a rating before submitting feedback.', 'error');
            return;
        }
        
        // Get the CSRF token from meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
        
        // Send feedback to server
        fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                type: 'learning_material',
                content: {
                    rating: currentRating,
                    comments: feedbackText.value,
                    material_id: window.location.pathname.split('/').pop() || 'unknown',
                    timestamp: new Date().toISOString()
                },
                csrf_token: csrfToken
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Success', 'Thank you for your feedback!', 'success');
                // Reset form
                currentRating = 0;
                feedbackText.value = '';
                stars.forEach(s => s.classList.remove('active'));
            } else {
                showNotification('Error', 'There was an error submitting your feedback.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error', 'There was an error submitting your feedback.', 'error');
        });
    });
}

/**
 * Initialize micro unit progress tracking
 */
function initMicroUnitProgress() {
    const completeButtons = document.querySelectorAll('.mark-complete');
    
    // Generate a unique key for this learning material
    const materialId = window.location.pathname.split('/').pop() || 'default';
    const storageKey = `micro_units_progress_${materialId}`;
    
    // Load saved progress if any
    const savedProgress = JSON.parse(localStorage.getItem(storageKey) || '{}');
    
    completeButtons.forEach((button, index) => {
        const microUnit = button.closest('.micro-unit');
        const unitId = `unit_${index}`;
        
        // Apply saved progress
        if (savedProgress[unitId]) {
            microUnit.classList.add('completed');
            button.textContent = 'Completed';
            button.classList.add('completed');
        }
        
        button.addEventListener('click', function() {
            microUnit.classList.toggle('completed');
            
            if (microUnit.classList.contains('completed')) {
                button.textContent = 'Completed';
                button.classList.add('completed');
                savedProgress[unitId] = true;
            } else {
                button.textContent = 'Mark as Complete';
                button.classList.remove('completed');
                delete savedProgress[unitId];
            }
            
            // Save progress to local storage
            localStorage.setItem(storageKey, JSON.stringify(savedProgress));
        });
    });
}

/**
 * Show notification toast
 */
function showNotification(title, message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <strong>${title}</strong>
        <span>${message}</span>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Remove after 5 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 5000);
} 