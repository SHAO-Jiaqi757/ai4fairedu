/**
 * AI4FairEdu Learning View JavaScript
 * Handles all interactive functionality for the learning view page
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("Learning view script loaded");
    
    // Function to populate all detailed content elements
    function populateAllDetailedContent() {
        // First check if we have detailed_units in window.processedContent
        if (!window.processedContent || !window.processedContent.detailed_units) {
            return;
        }
        
        // Force populate all detailed content elements
        const microUnits = document.querySelectorAll('.micro-unit');
        let populatedCount = 0;
        
        microUnits.forEach(unit => {
            const unitNumber = unit.getAttribute('data-unit-number');
            
            if (!unitNumber) {
                return;
            }
            
            // Get the detailed-content element
            let detailedContent = unit.querySelector('.detailed-content');
            
            // Check if the detailed content already exists and has content
            if (detailedContent && detailedContent.innerHTML.length > 100 && 
                !detailedContent.innerHTML.includes('No detailed content available')) {
                populatedCount++;
                return;
            }
            
            // Find the matching detailed unit
            const detailedUnit = window.processedContent.detailed_units.find(
                du => du.unit_number.toString() === unitNumber
            );
            
            if (!detailedUnit) {
                return;
            }
            
            // Create the detailed-content element if it doesn't exist
            if (!detailedContent) {
                detailedContent = document.createElement('div');
                detailedContent.className = 'detailed-content';
                detailedContent.style.display = 'none';
                
                // Insert it after the unit-content
                const unitContent = unit.querySelector('.unit-content');
                if (unitContent) {
                    unitContent.insertAdjacentElement('afterend', detailedContent);
                } else {
                    unit.appendChild(detailedContent);
                }
            }
            
            // Set the content
            if (detailedUnit.detailed_content) {
                detailedContent.innerHTML = `<h3>Detailed Content</h3>${detailedUnit.detailed_content}`;
                populatedCount++;
            } else {
                detailedContent.innerHTML = '<h3>Detailed Content</h3><p>No detailed content available for this unit.</p>';
            }
        });
    }

    // Debug: Check for detailed units in the processed_content
    if (window.processedContent) {
        console.log("Processed content available in JS:", Object.keys(window.processedContent));
        
        // Check for detailed_units
        if (window.processedContent.detailed_units) {
            console.log("Detailed units found in window.processedContent:", window.processedContent.detailed_units.length);
            console.log("First detailed unit:", window.processedContent.detailed_units[0]);
            
            // Check if the detailed_units have unit_number and detailed_content
            const firstUnit = window.processedContent.detailed_units[0];
            if (firstUnit) {
                console.log("First unit number:", firstUnit.unit_number);
                console.log("First unit detailed_content length:", firstUnit.detailed_content ? firstUnit.detailed_content.length : 0);
            }
        } else {
            console.log("No detailed_units found in window.processedContent");
        }
        
        // Check for sections
        if (window.processedContent.sections) {
            console.log("Sections found in window.processedContent:", window.processedContent.sections.length);
            
            // Check if the sections have detailed_units
            const firstSection = window.processedContent.sections[0];
            if (firstSection) {
                console.log("First section keys:", Object.keys(firstSection));
                
                if (firstSection.detailed_units) {
                    console.log("First section has detailed_units:", firstSection.detailed_units.length);
                    console.log("First section's first detailed unit:", firstSection.detailed_units[0]);
                } else {
                    console.log("No detailed_units found in first section");
                }
                
                // Check if the section has micro_units
                if (firstSection.micro_units) {
                    console.log("First section has micro_units:", firstSection.micro_units.length);
                    console.log("First section's first micro unit:", firstSection.micro_units[0]);
                    
                    // Check if the micro_units have unit_number
                    const firstMicroUnit = firstSection.micro_units[0];
                    if (firstMicroUnit) {
                        console.log("First micro unit number:", firstMicroUnit.unit_number);
                    }
                } else {
                    console.log("No micro_units found in first section");
                }
            }
        } else {
            console.log("No sections found in window.processedContent");
        }
    } else {
        console.log("No processed content available in JS");
    }
    
    // Directly check the detailed content elements
    const detailedContents = document.querySelectorAll('.detailed-content');
    console.log(`Found ${detailedContents.length} detailed content elements in the DOM`);
    detailedContents.forEach((content, index) => {
        const parentUnit = content.closest('.micro-unit');
        const unitNumber = parentUnit ? parentUnit.getAttribute('data-unit-number') : 'unknown';
        console.log(`Detailed content ${index + 1} for unit ${unitNumber}:`);
        console.log(`  - HTML length: ${content.innerHTML.length}`);
        console.log(`  - Display: ${window.getComputedStyle(content).display}`);
        console.log(`  - First 100 chars: ${content.innerHTML.substring(0, 100)}...`);
    });
    
    // Check all micro-units in the DOM
    const allMicroUnits = document.querySelectorAll('.micro-unit');
    console.log(`Found ${allMicroUnits.length} micro-units in the DOM`);
    allMicroUnits.forEach((unit, index) => {
        const unitNumber = unit.getAttribute('data-unit-number');
        console.log(`Micro-unit ${index + 1}:`);
        console.log(`  - data-unit-number: ${unitNumber}`);
        
        // Check if this unit has a detailed-content element
        const detailedContent = unit.querySelector('.detailed-content');
        if (detailedContent) {
            console.log(`  - Has detailed-content: Yes (length: ${detailedContent.innerHTML.length})`);
        } else {
            console.log(`  - Has detailed-content: No`);
        }
        
        // Check if there's a matching detailed unit in window.processedContent
        if (window.processedContent && window.processedContent.detailed_units) {
            const matchingUnit = window.processedContent.detailed_units.find(
                du => du.unit_number.toString() === unitNumber
            );
            if (matchingUnit) {
                console.log(`  - Matching detailed unit found in window.processedContent: Yes`);
                console.log(`  - Matching unit detailed_content length: ${matchingUnit.detailed_content ? matchingUnit.detailed_content.length : 0}`);
            } else {
                console.log(`  - Matching detailed unit found in window.processedContent: No`);
            }
        }
    });
    
    // View Controls
    const viewButtons = document.querySelectorAll('.view-btn');
    const contentViews = document.querySelectorAll('.content-view');
    
    // Original Content Modal
    const toggleOriginalBtn = document.getElementById('toggle-original');
    const originalContentModal = document.getElementById('original-content-modal');
    const closeModalBtn = document.querySelector('.close-modal');
    
    // Show original content in modal when button is clicked
    if (toggleOriginalBtn) {
        toggleOriginalBtn.addEventListener('click', function() {
            originalContentModal.style.display = 'block';
            document.body.style.overflow = 'hidden'; // Prevent scrolling behind modal
        });
    }
    
    // Close modal when close button is clicked
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            originalContentModal.style.display = 'none';
            document.body.style.overflow = ''; // Restore scrolling
        });
    }
    
    // Close modal when clicking outside the modal content
    window.addEventListener('click', function(event) {
        if (event.target === originalContentModal) {
            originalContentModal.style.display = 'none';
            document.body.style.overflow = ''; // Restore scrolling
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && originalContentModal.style.display === 'block') {
            originalContentModal.style.display = 'none';
            document.body.style.overflow = ''; // Restore scrolling
        }
    });
    
    // Call populateAllDetailedContent with a delay to ensure the DOM is fully loaded
    setTimeout(populateAllDetailedContent, 1000);
    
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
    const toolsSidebar = document.querySelector('.tools-sidebar');
    const contentArea = document.querySelector('.content-area');
    
    // Track active tools
    const activeTools = new Set();
    
    // Function to toggle a specific tool panel
    function toggleToolPanel(toolName) {
        console.log(`Toggling tool panel: ${toolName}`);
        const panel = document.getElementById(`${toolName}-panel`);
        
        if (!panel) return;
        
        // Check if this tool is already active
        if (activeTools.has(toolName)) {
            // Deactivate this tool
            activeTools.delete(toolName);
            
            // Hide this panel with a transition
            panel.classList.add('hidden');
            setTimeout(() => {
                panel.style.display = 'none';
            }, 300);
            
            // Update button state
            const button = document.querySelector(`.tool-btn[data-tool="${toolName}"]`);
            if (button) {
                button.classList.remove('active');
            }
            
            // If no tools are active, hide the sidebar
            if (activeTools.size === 0) {
                hideSidebar();
            }
        } else {
            // Activate this tool
            activeTools.add(toolName);
            
            // Show the sidebar if it's hidden
            showSidebar();
            
            // Show this panel
            panel.style.display = 'block';
            setTimeout(() => {
                panel.classList.remove('hidden');
            }, 10);
            
            // Update button state
            const button = document.querySelector(`.tool-btn[data-tool="${toolName}"]`);
            if (button) {
                button.classList.add('active');
            }
        }
    }
    
    // Function to show the sidebar
    function showSidebar() {
        if (!toolsSidebar) return;
        
        // Show the sidebar
        toolsSidebar.style.display = 'block';
        setTimeout(() => {
            toolsSidebar.style.opacity = '1';
            toolsSidebar.style.transform = 'translateX(0)';
        }, 10);
        
        // Update content area
        if (contentArea) {
            contentArea.classList.remove('sidebar-hidden');
        }
    }
    
    // Function to hide the sidebar
    function hideSidebar() {
        if (!toolsSidebar) return;
        
        // Hide the sidebar with a transition
        toolsSidebar.style.opacity = '0';
        toolsSidebar.style.transform = 'translateX(20px)';
        setTimeout(() => {
            toolsSidebar.style.display = 'none';
        }, 300);
        
        // Update content area
        if (contentArea) {
            contentArea.classList.add('sidebar-hidden');
        }
    }
    
    // Hide all tool panels and sidebar initially
    toolPanels.forEach(panel => {
        panel.classList.add('hidden');
        panel.style.display = 'none';
    });
    
    // Hide the sidebar initially
    if (toolsSidebar) {
        toolsSidebar.style.display = 'none';
        
        // Add a class to the content area to indicate sidebar is hidden
        if (contentArea) {
            contentArea.classList.add('sidebar-hidden');
        }
    }
    
    // Add click event listeners to tool buttons
    toolButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tool = this.getAttribute('data-tool');
            toggleToolPanel(tool);
        });
    });
    
    // // Focus Mode
    // const highlightStyle = document.getElementById('highlight-style');
    // const dimLevel = document.getElementById('dim-level');
    // let focusModeActive = false;
    
    // function toggleFocusMode(active) {
    //     const contentArea = document.querySelector('.content-area');
    //     focusModeActive = active;
        
    //     if (active) {
    //         contentArea.classList.add('focus-mode');
    //         contentArea.style.setProperty('--dim-level', `${dimLevel.value}%`);
    //     } else {
    //         contentArea.classList.remove('focus-mode');
    //     }
    // }
    
    // highlightStyle.addEventListener('change', function() {
    //     const contentArea = document.querySelector('.content-area');
    //     contentArea.setAttribute('data-highlight', this.value);
    // });
    
    // dimLevel.addEventListener('input', function() {
    //     if (focusModeActive) {
    //         document.querySelector('.content-area').style.setProperty('--dim-level', `${this.value}%`);
    //     }
    // });
    
    // // Text to Speech
    // const voiceSelect = document.getElementById('voice-select');
    // const speechRate = document.getElementById('speech-rate');
    // const playBtn = document.getElementById('play-btn');
    // const pauseBtn = document.getElementById('pause-btn');
    // const stopBtn = document.getElementById('stop-btn');
    // let speechSynth = window.speechSynthesis;
    // let currentUtterance = null;
    
    // // Populate voice select
    // function loadVoices() {
    //     const voices = speechSynth.getVoices();
    //     voiceSelect.innerHTML = voices.map(voice => 
    //         `<option value="${voice.name}">${voice.name} (${voice.lang})</option>`
    //     ).join('');
    // }
    
    // speechSynth.onvoiceschanged = loadVoices;
    // loadVoices();
    
    // function speak(text) {
    //     if (currentUtterance) {
    //         speechSynth.cancel();
    //     }
        
    //     const utterance = new SpeechSynthesisUtterance(text);
    //     utterance.voice = speechSynth.getVoices().find(voice => voice.name === voiceSelect.value);
    //     utterance.rate = parseFloat(speechRate.value);
        
    //     currentUtterance = utterance;
    //     speechSynth.speak(utterance);
    // }
    
    // playBtn.addEventListener('click', function() {
    //     const activeSection = document.querySelector('.content-section.active');
    //     if (activeSection) {
    //         speak(activeSection.textContent);
    //     }
    // });
    
    // pauseBtn.addEventListener('click', function() {
    //     speechSynth.pause();
    // });
    
    // stopBtn.addEventListener('click', function() {
    //     speechSynth.cancel();
    //     currentUtterance = null;
    // });
    
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
        const unitNumber = microUnit.getAttribute('data-unit-number');
        
        // Close any other expanded units
        document.querySelectorAll('.micro-unit.expanded').forEach(unit => {
            if (unit !== microUnit) {
                unit.classList.remove('expanded');
                unit.querySelector('.unit-content').classList.add('collapsed');
                // Hide detailed content for other units
                const detailedContent = unit.querySelector('.detailed-content');
                if (detailedContent) {
                    detailedContent.style.display = 'none';
                }
                // Reset read more button text
                const readMoreBtn = unit.querySelector('.read-more-btn');
                if (readMoreBtn) {
                    readMoreBtn.textContent = 'Read More';
                }
            }
        });
        
        // Toggle current unit
        const isExpanding = !microUnit.classList.contains('expanded');
        microUnit.classList.toggle('expanded');
        microUnit.querySelector('.unit-content').classList.toggle('collapsed');
        
        // Toggle detailed content visibility
        let detailedContent = microUnit.querySelector('.detailed-content');
        const readMoreBtn = microUnit.querySelector('.read-more-btn');
        
        if (isExpanding) {
            // Check if the detailed content element exists and has content
            if (detailedContent && detailedContent.innerHTML.length > 100) {
                // The detailed content already exists in the DOM, just show it
                detailedContent.style.display = 'block';
            } else {
                // If we don't have a detailed content element or it's empty, try to create/populate it
                
                // If we don't have a detailed content element, create one
                if (!detailedContent) {
                    detailedContent = document.createElement('div');
                    detailedContent.className = 'detailed-content';
                    
                    // Insert it after the unit-content and before the read-more-btn
                    const unitContent = microUnit.querySelector('.unit-content');
                    if (unitContent && readMoreBtn) {
                        readMoreBtn.insertAdjacentElement('beforebegin', detailedContent);
                    } else {
                        microUnit.appendChild(detailedContent);
                    }
                }
                
                // Find the matching detailed unit
                if (window.processedContent && window.processedContent.detailed_units) {
                    const detailedUnit = window.processedContent.detailed_units.find(
                        du => du.unit_number.toString() === unitNumber
                    );
                    
                    if (detailedUnit && detailedUnit.detailed_content) {
                        detailedContent.innerHTML = `<h3>Detailed Content</h3>${detailedUnit.detailed_content}`;
                    } else {
                        detailedContent.innerHTML = '<h3>Detailed Content</h3><p>No detailed content available for this unit.</p>';
                    }
                } else {
                    detailedContent.innerHTML = '<h3>Detailed Content</h3><p>No detailed content available.</p>';
                }
                
                // Show the detailed content
                detailedContent.style.display = 'block';
            }
            
            // Update read more button text
            if (readMoreBtn) {
                readMoreBtn.textContent = 'Show Less';
            }
        } else {
            // Hide the detailed content
            if (detailedContent) {
                detailedContent.style.display = 'none';
            }
            
            // Update read more button text
            if (readMoreBtn) {
                readMoreBtn.textContent = 'Read More';
            }
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
        btn.addEventListener('click', function() {
            const microUnit = this.closest('.micro-unit');
            const unitNumber = microUnit.getAttribute('data-unit-number');
            
            // Force populate the detailed content before toggling
            if (window.processedContent && window.processedContent.detailed_units) {
                const detailedUnit = window.processedContent.detailed_units.find(
                    du => du.unit_number.toString() === unitNumber
                );
                
                if (detailedUnit && detailedUnit.detailed_content) {
                    // Get or create the detailed-content element
                    let detailedContent = microUnit.querySelector('.detailed-content');
                    
                    if (!detailedContent) {
                        detailedContent = document.createElement('div');
                        detailedContent.className = 'detailed-content';
                        detailedContent.style.display = 'none';
                        
                        // Insert it before the read-more button
                        this.insertAdjacentElement('beforebegin', detailedContent);
                    }
                    
                    // Set the content if it's empty or minimal
                    if (detailedContent.innerHTML.trim() === '' || 
                        detailedContent.innerHTML.trim() === '<h3>Detailed Content</h3>' ||
                        detailedContent.innerHTML.includes('No detailed content available')) {
                        
                        detailedContent.innerHTML = `<h3>Detailed Content</h3>${detailedUnit.detailed_content}`;
                    }
                }
            }
            
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