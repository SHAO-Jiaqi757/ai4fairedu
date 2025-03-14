/**
 * AI4FairEdu Learning View JavaScript
 * Handles all interactive functionality for the learning view page
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("Learning view script loaded");
    
    // // Debug: Check content sections
    // const debugContentSections = document.querySelectorAll('.content-section');
    // console.log(`Found ${debugContentSections.length} content sections`);
    // debugContentSections.forEach((section, index) => {
    //     console.log(`Section ${index + 1}:`);
    //     console.log(`  - ID: ${section.id}`);
    //     console.log(`  - Classes: ${section.className}`);
    //     console.log(`  - Display: ${window.getComputedStyle(section).display}`);
    //     console.log(`  - Visibility: ${window.getComputedStyle(section).visibility}`);
    //     console.log(`  - Content HTML length: ${section.innerHTML.length}`);
    // });
    
    // Immediately ensure content sections are displayed
    ensureContentSectionsDisplayed();
    
    // Immediately populate detailed content
    populateAllDetailedContent();
    
    // // Debug: Check if processedContent is available
    // if (window.processedContent) {
    //     console.log("processedContent is available:", window.processedContent);
    //     if (window.processedContent.sections) {
    //         console.log("Sections found:", window.processedContent.sections.length);
    //     }
    //     if (window.processedContent.detailed_units) {
    //         console.log("Detailed units found:", window.processedContent.detailed_units.length);
    //     }
    // } else {
    //     console.log("processedContent is not available");
    // }
    
    // // Debug: Check content views
    // const debugContentViews = document.querySelectorAll('.content-view');
    // console.log(`Found ${debugContentViews.length} content views`);
    // debugContentViews.forEach((view, index) => {
    //     console.log(`View ${index + 1}:`);
    //     console.log(`  - Classes: ${view.className}`);
    //     console.log(`  - Display: ${window.getComputedStyle(view).display}`);
    //     console.log(`  - Visibility: ${window.getComputedStyle(view).visibility}`);
    //     console.log(`  - Content HTML length: ${view.innerHTML.length}`);
    // });
    
    // Function to populate all detailed content elements
    function populateAllDetailedContent() {
        console.log("Populating all detailed content elements");
        
        // First check if we have detailed_units in window.processedContent
        if (!window.processedContent || !window.processedContent.detailed_units) {
            console.log("No detailed_units found in window.processedContent");
            return;
        }
        
        console.log(`Found ${window.processedContent.detailed_units.length} detailed units in window.processedContent`);
        
        // Force populate all detailed content elements
        const microUnits = document.querySelectorAll('.micro-unit');
        console.log(`Found ${microUnits.length} micro-units in the DOM`);
        
        let populatedCount = 0;
        
        microUnits.forEach((unit, index) => {
            const unitNumber = unit.getAttribute('data-unit-number');
            console.log(`Processing micro-unit ${index + 1} with unit number ${unitNumber}`);
            
            if (!unitNumber) {
                console.log(`  - No unit number found, skipping`);
                return;
            }
            
            // Get the detailed-content element
            let detailedContent = unit.querySelector('.detailed-content');
            
            // Check if the detailed content already exists and has content
            if (detailedContent && detailedContent.innerHTML.length > 100 && 
                !detailedContent.innerHTML.includes('No detailed content available')) {
                console.log(`  - Detailed content already exists with length ${detailedContent.innerHTML.length}`);
                populatedCount++;
                return;
            }
            
            // Find the matching detailed unit
            const detailedUnit = window.processedContent.detailed_units.find(
                du => du.unit_number.toString() === unitNumber
            );
            
            if (!detailedUnit) {
                console.log(`  - No matching detailed unit found for unit number ${unitNumber}`);
                return;
            }
            
            console.log(`  - Found matching detailed unit with content length ${detailedUnit.detailed_content ? detailedUnit.detailed_content.length : 0}`);
            
            // Create the detailed-content element if it doesn't exist
            if (!detailedContent) {
                console.log(`  - Creating new detailed-content element`);
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
                console.log(`  - Populated detailed content with length ${detailedContent.innerHTML.length}`);
                populatedCount++;
            } else {
                detailedContent.innerHTML = '<h3>Detailed Content</h3><p>No detailed content available for this unit.</p>';
                console.log(`  - No detailed content available for this unit`);
            }
        });
        
        console.log(`Populated ${populatedCount} detailed content elements`);
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
    
    // Debug button
    const debugButton = document.getElementById('debug-content');
    if (debugButton) {
        debugButton.addEventListener('click', function() {
            console.log("Debug button clicked");
            
            // Check content sections
            const debugSections = document.querySelectorAll('.content-section');
            console.log(`Found ${debugSections.length} content sections`);
            
            if (debugSections.length === 0) {
                console.log("No content sections found. Creating a test section.");
                
                // Create a test section
                const contentView = document.querySelector('.content-view.active');
                if (contentView) {
                    const testSection = document.createElement('div');
                    testSection.className = 'content-section active';
                    testSection.id = 'test';  // Use simple ID without prefix
                    testSection.innerHTML = '<div class="section-header"><h2>Test Section</h2></div><div class="section-content"><p>This is a test section to debug the content display issue.</p></div>';
                    contentView.appendChild(testSection);
                    console.log("Test section created.");
                } else {
                    console.log("No active content view found.");
                }
            } else {
                // Make all sections visible for debugging
                debugSections.forEach(section => {
                    section.style.display = 'block';
                    section.style.visibility = 'visible';
                    console.log(`Made section ${section.id} visible.`);
                    
                    // Check for micro-units in this section
                    const sectionMicroUnits = section.querySelectorAll('.micro-unit');
                    if (sectionMicroUnits.length > 0) {
                        console.log(`Found ${sectionMicroUnits.length} micro-units in section ${section.id}`);
                        
                        // Make all micro-units visible
                        sectionMicroUnits.forEach((unit, index) => {
                            unit.style.display = 'block';
                            unit.style.visibility = 'visible';
                            console.log(`Made micro-unit ${index + 1} in section ${section.id} visible`);
                        });
                    } else {
                        console.log(`No micro-units found in section ${section.id}`);
                    }
                });
            }
            
            // Check processed content
            if (window.processedContent) {
                console.log("Processed content:", window.processedContent);
                
                // Check if sections exist
                if (window.processedContent.sections) {
                    console.log("Sections found:", window.processedContent.sections.length);
                    
                    // Check section IDs
                    window.processedContent.sections.forEach((section, index) => {
                        console.log(`Section ${index + 1} ID: ${section.id}`);
                        
                        // Check if the section element exists in the DOM
                        const sectionElement = document.getElementById(section.id);
                        if (sectionElement) {
                            console.log(`  - Section element found with ID: ${section.id}`);
                            
                            // Check if this section has micro_units in the processed content
                            if (section.micro_units) {
                                console.log(`  - Section has ${section.micro_units.length} micro_units in processed content`);
                                
                                // Check if micro-units exist in the DOM
                                const microUnits = sectionElement.querySelectorAll('.micro-unit');
                                console.log(`  - Section has ${microUnits.length} micro-units in the DOM`);
                                
                                // If there's a mismatch, try to create the missing micro-units
                                if (microUnits.length === 0 && section.micro_units.length > 0) {
                                    console.log(`  - Creating missing micro-units for section ${section.id}`);
                                    
                                    // Create a container for micro-units if it doesn't exist
                                    let microUnitsContainer = sectionElement.querySelector('.micro-units');
                                    if (!microUnitsContainer) {
                                        microUnitsContainer = document.createElement('div');
                                        microUnitsContainer.className = 'micro-units';
                                        sectionElement.appendChild(microUnitsContainer);
                                    }
                                    
                                    // Create micro-units
                                    section.micro_units.forEach((unit, unitIndex) => {
                                        const microUnit = document.createElement('div');
                                        microUnit.className = 'micro-unit';
                                        microUnit.setAttribute('data-unit-number', unit.unit_number);
                                        
                                        // Create unit header
                                        const unitHeader = document.createElement('div');
                                        unitHeader.className = 'unit-header';
                                        unitHeader.innerHTML = `
                                            <span class="unit-number">Unit ${unitIndex + 1}</span>
                                            <span class="unit-time">${unit.estimated_time || 2}min</span>
                                            <button class="close-unit-btn"><i class="fas fa-times"></i></button>
                                        `;
                                        
                                        // Create unit content
                                        const unitContent = document.createElement('div');
                                        unitContent.className = 'unit-content collapsed';
                                        unitContent.innerHTML = unit.content || 'No content available';
                                        
                                        // Create read more button
                                        const readMoreBtn = document.createElement('button');
                                        readMoreBtn.className = 'read-more-btn';
                                        readMoreBtn.textContent = 'Read More';
                                        
                                        // Create unit progress
                                        const unitProgress = document.createElement('div');
                                        unitProgress.className = 'unit-progress';
                                        unitProgress.innerHTML = `
                                            <button class="mark-complete-btn">Mark as Complete</button>
                                            <span class="completion-status">Not started</span>
                                        `;
                                        
                                        // Assemble micro-unit
                                        microUnit.appendChild(unitHeader);
                                        microUnit.appendChild(unitContent);
                                        microUnit.appendChild(readMoreBtn);
                                        microUnit.appendChild(unitProgress);
                                        
                                        // Add to container
                                        microUnitsContainer.appendChild(microUnit);
                                    });
                                    
                                    console.log(`  - Created ${section.micro_units.length} micro-units for section ${section.id}`);
                                }
                            }
                        } else {
                            console.log(`  - Section element NOT found with ID: ${section.id}`);
                        }
                    });
                }
                
                // Check for detailed units
                if (window.processedContent.detailed_units) {
                    console.log(`Found ${window.processedContent.detailed_units.length} detailed units in processed content`);
                    
                    // Force populate all detailed content
                    populateAllDetailedContent();
                }
            } else {
                console.log("No processed content available.");
            }
            
            // Ensure content sections are displayed
            ensureContentSectionsDisplayed();
        });
    }
    
    // Call populateAllDetailedContent with a delay to ensure the DOM is fully loaded
    setTimeout(populateAllDetailedContent, 1000);
    
    // Ensure content sections are properly displayed
    function ensureContentSectionsDisplayed() {
        console.log("Ensuring content sections are properly displayed");
        
        // Check if the content-area is properly displayed
        const contentArea = document.querySelector('.content-area');
        if (contentArea) {
            console.log("Content area found");
            contentArea.style.display = 'block';
            contentArea.style.visibility = 'visible';
        } else {
            console.log("Content area not found");
        }
        
        // Check if there are any content sections
        const sections = document.querySelectorAll('.content-section');
        console.log(`Found ${sections.length} content sections`);
        
        if (sections.length === 0) {
            console.log("No content sections found");
            
            // Create a default section if none exists
            const contentView = document.querySelector('.content-view.active');
            if (contentView) {
                console.log("Creating a default section");
                const defaultSection = document.createElement('div');
                defaultSection.className = 'content-section active';
                defaultSection.id = 'default';
                
                // Add content from original_content if available
                const originalContent = document.querySelector('#original-content-modal .modal-body');
                if (originalContent) {
                    defaultSection.innerHTML = `
                        <div class="section-header">
                            <h2>Content</h2>
                        </div>
                        <div class="section-content">
                            ${originalContent.innerHTML}
                        </div>
                    `;
                } else {
                    defaultSection.innerHTML = `
                        <div class="section-header">
                            <h2>Content</h2>
                        </div>
                        <div class="section-content">
                            <p>No content available. Please try refreshing the page.</p>
                        </div>
                    `;
                }
                
                contentView.appendChild(defaultSection);
                console.log("Default section created");
            }
            
            return;
        }
        
        // Make all sections visible for debugging
        sections.forEach(section => {
            console.log(`Processing section ${section.id}`);
            section.style.display = 'block';
            section.style.visibility = 'visible';
        });
        
        // Check if any section is active
        let activeSection = document.querySelector('.content-section.active');
        if (!activeSection) {
            console.log("No active section found, activating the first one");
            activeSection = sections[0];
            activeSection.classList.add('active');
        }
        
        // Make sure the active section is displayed
        activeSection.style.display = 'block';
        activeSection.style.visibility = 'visible';
        console.log(`Active section ${activeSection.id} is now visible`);
        
        // Make sure the content view is active
        const contentView = document.querySelector('.content-view');
        if (contentView) {
            contentView.classList.add('active');
            contentView.style.display = 'block';
            contentView.style.visibility = 'visible';
            console.log("Content view is now visible");
        }
        
        // Check for micro-units
        const microUnits = document.querySelectorAll('.micro-unit');
        console.log(`Found ${microUnits.length} micro-units`);
        
        if (microUnits.length > 0) {
            // Make sure micro-units are visible
            microUnits.forEach((unit, index) => {
                unit.style.display = 'block';
                unit.style.visibility = 'visible';
                console.log(`Made micro-unit ${index + 1} visible`);
            });
        }
    }
    
    // Call the function after a delay to ensure the DOM is fully loaded
    setTimeout(ensureContentSectionsDisplayed, 1500);
    
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
            console.log(`Navigation item clicked for section: ${sectionId}`);
            
            // Update active nav item
            navItems.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
            
            // Show selected section
            contentSections.forEach(section => {
                section.classList.remove('active');
                section.style.display = 'none';
            });
            
            // Use the section ID directly
            const targetSection = document.getElementById(sectionId);
            
            if (targetSection) {
                console.log(`Found target section with ID: ${sectionId}`);
                targetSection.classList.add('active');
                targetSection.style.display = 'block';
                targetSection.style.visibility = 'visible';
                
                // Check if this section has micro-units
                const microUnits = targetSection.querySelectorAll('.micro-unit');
                console.log(`Found ${microUnits.length} micro-units in section ${sectionId}`);
                
                // Make sure micro-units are visible
                microUnits.forEach(unit => {
                    unit.style.display = 'block';
                    unit.style.visibility = 'visible';
                });
            } else {
                console.error(`Section with ID ${sectionId} not found`);
                
                // Try with section- prefix as fallback
                const fallbackSection = document.getElementById(`section-${sectionId}`);
                if (fallbackSection) {
                    console.log(`Found fallback section with ID: section-${sectionId}`);
                    fallbackSection.classList.add('active');
                    fallbackSection.style.display = 'block';
                    fallbackSection.style.visibility = 'visible';
                }
            }
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