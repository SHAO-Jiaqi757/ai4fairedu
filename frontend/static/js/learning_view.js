/**
 * AI4FairEdu Learning View JavaScript
 * Handles all interactive functionality for the learning view page
 */

document.addEventListener('DOMContentLoaded', function() {
    // View Controls
    const viewButtons = document.querySelectorAll('.view-btn');
    const contentViews = document.querySelectorAll('.content-view');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            
            // Update active button
            viewButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show selected view
            contentViews.forEach(view => view.classList.remove('active'));
            document.querySelector(`.${view}-view`).classList.add('active');
        });
    });
    
    // Section Navigation
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            
            // Update active nav item
            navItems.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
            
            // Show selected section
            contentSections.forEach(section => section.classList.remove('active'));
            document.getElementById(`section-${sectionId}`).classList.add('active');
        });
    });
    
    // Tool Buttons
    const toolButtons = document.querySelectorAll('.tool-btn');
    const toolPanels = document.querySelectorAll('.tool-panel');
    
    toolButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tool = this.getAttribute('data-tool');
            const panel = document.getElementById(`${tool}-panel`);
            
            // Toggle active state
            this.classList.toggle('active');
            panel.classList.toggle('active');
        });
    });
    
    // Focus Mode
    const highlightStyle = document.getElementById('highlight-style');
    const dimLevel = document.getElementById('dim-level');
    let focusModeActive = false;
    
    function toggleFocusMode(active) {
        const contentArea = document.querySelector('.content-area');
        focusModeActive = active;
        
        if (active) {
            contentArea.classList.add('focus-mode');
            contentArea.style.setProperty('--dim-level', `${dimLevel.value}%`);
        } else {
            contentArea.classList.remove('focus-mode');
        }
    }
    
    highlightStyle.addEventListener('change', function() {
        const contentArea = document.querySelector('.content-area');
        contentArea.setAttribute('data-highlight', this.value);
    });
    
    dimLevel.addEventListener('input', function() {
        if (focusModeActive) {
            document.querySelector('.content-area').style.setProperty('--dim-level', `${this.value}%`);
        }
    });
    
    // Text to Speech
    const voiceSelect = document.getElementById('voice-select');
    const speechRate = document.getElementById('speech-rate');
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const stopBtn = document.getElementById('stop-btn');
    let speechSynth = window.speechSynthesis;
    let currentUtterance = null;
    
    // Populate voice select
    function loadVoices() {
        const voices = speechSynth.getVoices();
        voiceSelect.innerHTML = voices.map(voice => 
            `<option value="${voice.name}">${voice.name} (${voice.lang})</option>`
        ).join('');
    }
    
    speechSynth.onvoiceschanged = loadVoices;
    loadVoices();
    
    function speak(text) {
        if (currentUtterance) {
            speechSynth.cancel();
        }
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = speechSynth.getVoices().find(voice => voice.name === voiceSelect.value);
        utterance.rate = parseFloat(speechRate.value);
        
        currentUtterance = utterance;
        speechSynth.speak(utterance);
    }
    
    playBtn.addEventListener('click', function() {
        const activeSection = document.querySelector('.content-section.active');
        if (activeSection) {
            speak(activeSection.textContent);
        }
    });
    
    pauseBtn.addEventListener('click', function() {
        speechSynth.pause();
    });
    
    stopBtn.addEventListener('click', function() {
        speechSynth.cancel();
        currentUtterance = null;
    });
    
    // Notes
    const notesArea = document.getElementById('notes-area');
    const saveNotesBtn = document.getElementById('save-notes');
    const clearNotesBtn = document.getElementById('clear-notes');
    
    // Load saved notes
    const savedNotes = localStorage.getItem('learning_notes');
    if (savedNotes) {
        notesArea.value = savedNotes;
    }
    
    saveNotesBtn.addEventListener('click', function() {
        localStorage.setItem('learning_notes', notesArea.value);
        alert('Notes saved successfully!');
    });
    
    clearNotesBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear your notes?')) {
            notesArea.value = '';
            localStorage.removeItem('learning_notes');
        }
    });
    
    // Timer
    const timerDisplay = {
        minutes: document.getElementById('minutes'),
        seconds: document.getElementById('seconds')
    };
    const timerControls = {
        start: document.getElementById('start-timer'),
        pause: document.getElementById('pause-timer'),
        reset: document.getElementById('reset-timer')
    };
    const timerPresets = document.querySelectorAll('.timer-presets button');
    
    let timerInterval;
    let remainingSeconds = 25 * 60;
    let isTimerRunning = false;
    
    function updateTimerDisplay() {
        const minutes = Math.floor(remainingSeconds / 60);
        const seconds = remainingSeconds % 60;
        timerDisplay.minutes.textContent = minutes.toString().padStart(2, '0');
        timerDisplay.seconds.textContent = seconds.toString().padStart(2, '0');
    }
    
    function startTimer() {
        if (!isTimerRunning) {
            isTimerRunning = true;
            timerControls.start.disabled = true;
            timerControls.pause.disabled = false;
            
            timerInterval = setInterval(() => {
                remainingSeconds--;
                updateTimerDisplay();
                
                if (remainingSeconds <= 0) {
                    stopTimer();
                    alert('Timer complete!');
                }
            }, 1000);
        }
    }
    
    function pauseTimer() {
        clearInterval(timerInterval);
        isTimerRunning = false;
        timerControls.start.disabled = false;
        timerControls.pause.disabled = true;
    }
    
    function stopTimer() {
        clearInterval(timerInterval);
        isTimerRunning = false;
        timerControls.start.disabled = false;
        timerControls.pause.disabled = true;
    }
    
    function resetTimer() {
        stopTimer();
        remainingSeconds = 25 * 60;
        updateTimerDisplay();
    }
    
    timerControls.start.addEventListener('click', startTimer);
    timerControls.pause.addEventListener('click', pauseTimer);
    timerControls.reset.addEventListener('click', resetTimer);
    
    timerPresets.forEach(preset => {
        preset.addEventListener('click', function() {
            const minutes = parseInt(this.getAttribute('data-time'));
            remainingSeconds = minutes * 60;
            updateTimerDisplay();
            stopTimer();
            
            // Update active preset
            timerPresets.forEach(p => p.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Micro-unit interaction
    const microUnits = document.querySelectorAll('.micro-unit');
    const readMoreBtns = document.querySelectorAll('.read-more-btn');
    
    // Function to toggle micro-unit expansion
    function toggleMicroUnit(microUnit) {
        // Close any other expanded units
        document.querySelectorAll('.micro-unit.expanded').forEach(unit => {
            if (unit !== microUnit) {
                unit.classList.remove('expanded');
                unit.querySelector('.unit-content').classList.add('collapsed');
            }
        });
        
        // Toggle current unit
        microUnit.classList.toggle('expanded');
        microUnit.querySelector('.unit-content').classList.toggle('collapsed');
        
        // Scroll to the unit if it's expanded
        if (microUnit.classList.contains('expanded')) {
            microUnit.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    // Add click event to micro-units
    microUnits.forEach(microUnit => {
        microUnit.addEventListener('click', function(e) {
            // Don't toggle if clicking on a button or link inside the unit
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A' || 
                e.target.closest('button') || e.target.closest('a')) {
                return;
            }
            
            toggleMicroUnit(this);
        });
    });
    
    // Add click event to read more buttons
    readMoreBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent the micro-unit click event
            const microUnit = this.closest('.micro-unit');
            toggleMicroUnit(microUnit);
        });
    });
    
    // Add click event to close buttons
    const closeButtons = document.querySelectorAll('.close-unit-btn');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent the micro-unit click event
            const microUnit = this.closest('.micro-unit');
            if (microUnit.classList.contains('expanded')) {
                microUnit.classList.remove('expanded');
                microUnit.querySelector('.unit-content').classList.add('collapsed');
            }
        });
    });
    
    // Add click event to mark complete buttons
    const markCompleteButtons = document.querySelectorAll('.mark-complete-btn');
    markCompleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent the micro-unit click event
            const microUnit = this.closest('.micro-unit');
            const completionStatus = microUnit.querySelector('.completion-status');
            
            // Toggle completed state
            if (microUnit.classList.contains('completed')) {
                microUnit.classList.remove('completed');
                this.classList.remove('completed');
                this.textContent = 'Mark as Complete';
                completionStatus.textContent = 'In progress';
            } else {
                microUnit.classList.add('completed');
                this.classList.add('completed');
                this.textContent = 'Completed';
                completionStatus.textContent = 'Completed';
                
                // Save completion status to localStorage
                const unitId = microUnit.closest('.content-section').id + '-' + 
                               microUnit.querySelector('.unit-number').textContent.replace('Unit ', '');
                saveUnitProgress(unitId, true);
                
                // Check if all units in the section are completed
                checkSectionCompletion(microUnit.closest('.content-section'));
            }
        });
    });
    
    // Function to save unit progress to localStorage
    function saveUnitProgress(unitId, completed) {
        const userId = document.body.dataset.userId || 'anonymous';
        const storageKey = `ai4fairedu_progress_${userId}`;
        
        let progress = JSON.parse(localStorage.getItem(storageKey) || '{}');
        progress[unitId] = {
            completed: completed,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem(storageKey, JSON.stringify(progress));
    }
    
    // Function to check if all units in a section are completed
    function checkSectionCompletion(section) {
        const totalUnits = section.querySelectorAll('.micro-unit').length;
        const completedUnits = section.querySelectorAll('.micro-unit.completed').length;
        
        const sectionNav = document.querySelector(`.nav-item[data-section="${section.id.replace('section-', '')}"]`);
        if (sectionNav) {
            if (completedUnits === totalUnits) {
                sectionNav.classList.add('completed');
            } else {
                sectionNav.classList.remove('completed');
            }
        }
    }
    
    // Load saved progress on page load
    function loadSavedProgress() {
        const userId = document.body.dataset.userId || 'anonymous';
        const storageKey = `ai4fairedu_progress_${userId}`;
        
        let progress = JSON.parse(localStorage.getItem(storageKey) || '{}');
        
        // Apply saved progress to units
        Object.keys(progress).forEach(unitId => {
            const [sectionId, unitNum] = unitId.split('-');
            const section = document.getElementById(`section-${sectionId}`);
            
            if (section) {
                const units = section.querySelectorAll('.micro-unit');
                if (units[unitNum - 1] && progress[unitId].completed) {
                    const unit = units[unitNum - 1];
                    const completeBtn = unit.querySelector('.mark-complete-btn');
                    const completionStatus = unit.querySelector('.completion-status');
                    
                    unit.classList.add('completed');
                    if (completeBtn) {
                        completeBtn.classList.add('completed');
                        completeBtn.textContent = 'Completed';
                    }
                    if (completionStatus) {
                        completionStatus.textContent = 'Completed';
                    }
                }
            }
        });
        
        // Check section completion
        document.querySelectorAll('.content-section').forEach(section => {
            checkSectionCompletion(section);
        });
    }
    
    // Load saved progress on page load
    loadSavedProgress();
}); 