// Main JavaScript for AI4FairEdu Frontend

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize CSRF protection for AJAX requests
    initCSRFProtection();
    
    // Initialize language switcher
    initLanguageSwitcher();
    
    // Initialize accessibility features
    initAccessibilityControls();
    
    // Initialize form handlers
    initForms();
    
    // Initialize material processing
    initMaterialProcessing();
    
    // Load sample materials if on the material page
    if (document.querySelector('.material-page')) {
        loadSampleMaterials();
    }
    
    // Initialize tooltips and other UI elements
    initUI();
});

// Language Switcher
function initLanguageSwitcher() {
    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        languageSelect.addEventListener('change', function() {
            // Get the CSRF token from the meta tag
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
            
            // Send the language preference to the server
            fetch('/set-language', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    language: this.value
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload the page to apply the language change
                    window.location.reload();
                } else {
                    console.error('Failed to set language:', data.error);
                }
            })
            .catch(error => {
                console.error('Error setting language:', error);
            });
        });
    }
}

// Set up CSRF protection for all AJAX requests
function initCSRFProtection() {
    // Get the CSRF token from the meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    
    if (csrfToken) {
        // Add the CSRF token to all fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            // Only add for same-origin requests
            if (url.startsWith('/') || url.startsWith(window.location.origin)) {
                options = options || {};
                options.headers = options.headers || {};
                
                // Add CSRF token to headers
                options.headers['X-CSRFToken'] = csrfToken;
                
                // If it's a POST request with JSON body, also include the token in the body
                if (options.method === 'POST' && options.body && 
                    options.headers['Content-Type'] === 'application/json') {
                    try {
                        const bodyData = JSON.parse(options.body);
                        bodyData.csrf_token = csrfToken;
                        options.body = JSON.stringify(bodyData);
                    } catch (e) {
                        console.error('Error adding CSRF token to request body:', e);
                    }
                }
            }
            
            return originalFetch(url, options);
        };
        
        console.log('CSRF protection initialized for AJAX requests');
    } else {
        console.warn('CSRF token not found in meta tag');
    }
}

// Accessibility Controls
function initAccessibilityControls() {
    // Font toggle
    const fontToggle = document.getElementById('font-toggle');
    if (fontToggle) {
        fontToggle.addEventListener('change', function() {
            document.body.classList.toggle('dyslexic-font', this.checked);
            localStorage.setItem('useDyslexicFont', this.checked);
        });
        
        // Check saved preference
        const useDyslexicFont = localStorage.getItem('useDyslexicFont') === 'true';
        fontToggle.checked = useDyslexicFont;
        document.body.classList.toggle('dyslexic-font', useDyslexicFont);
    }
    
    // High contrast toggle
    const contrastToggle = document.getElementById('contrast-toggle');
    if (contrastToggle) {
        contrastToggle.addEventListener('change', function() {
            document.body.classList.toggle('high-contrast', this.checked);
            localStorage.setItem('useHighContrast', this.checked);
        });
        
        // Check saved preference
        const useHighContrast = localStorage.getItem('useHighContrast') === 'true';
        contrastToggle.checked = useHighContrast;
        document.body.classList.toggle('high-contrast', useHighContrast);
    }
    
    // Text size toggle
    const textSizeToggle = document.getElementById('text-size-toggle');
    if (textSizeToggle) {
        textSizeToggle.addEventListener('change', function() {
            document.body.classList.toggle('large-text', this.checked);
            localStorage.setItem('useLargeText', this.checked);
        });
        
        // Check saved preference
        const useLargeText = localStorage.getItem('useLargeText') === 'true';
        textSizeToggle.checked = useLargeText;
        document.body.classList.toggle('large-text', useLargeText);
    }
    
    // Line spacing toggle
    const lineSpacingToggle = document.getElementById('line-spacing-toggle');
    if (lineSpacingToggle) {
        lineSpacingToggle.addEventListener('change', function() {
            document.body.classList.toggle('line-spacing', this.checked);
            localStorage.setItem('useLineSpacing', this.checked);
        });
        
        // Check saved preference
        const useLineSpacing = localStorage.getItem('useLineSpacing') === 'true';
        lineSpacingToggle.checked = useLineSpacing;
        document.body.classList.toggle('line-spacing', useLineSpacing);
    }
}

// Form Handlers
function initForms() {
    // Profile form submission
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = profileForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
            
            // Collect form data
            const formData = new FormData(profileForm);
            const profileData = {
                user_id: formData.get('user_id') || 'anonymous',
                name: formData.get('name'),
                age: parseInt(formData.get('age')),
                education_level: formData.get('education_level'),
                learning_preferences: {
                    visual_learner: formData.get('visual_learner') === 'on',
                    auditory_learner: formData.get('auditory_learner') === 'on',
                    kinesthetic_learner: formData.get('kinesthetic_learner') === 'on'
                },
                attention_challenges: {
                    difficulty_focusing: parseInt(formData.get('difficulty_focusing') || '0'),
                    easily_distracted: parseInt(formData.get('easily_distracted') || '0'),
                    fidgeting: parseInt(formData.get('fidgeting') || '0'),
                    task_completion: parseInt(formData.get('task_completion') || '0'),
                    forgetfulness: parseInt(formData.get('forgetfulness') || '0')
                },
                reading_challenges: {
                    reading_speed: parseInt(formData.get('reading_speed') || '0'),
                    comprehension: parseInt(formData.get('comprehension') || '0'),
                    word_recognition: parseInt(formData.get('word_recognition') || '0'),
                    pronunciation: parseInt(formData.get('pronunciation') || '0'),
                    tracking_lines: parseInt(formData.get('tracking_lines') || '0')
                },
                additional_info: formData.get('additional_info')
            };
            
            // Submit to API
            fetch('/api/submit-profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(profileData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showToast('Profile saved successfully!', 'success');
                    
                    // Redirect to dashboard
                    setTimeout(() => {
                        window.location.href = data.redirect || '/dashboard';
                    }, 1500);
                } else {
                    // Show error message
                    showToast('Error: ' + data.error, 'error');
                    
                    // Reset button
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An unexpected error occurred. Please try again.', 'error');
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            });
        });
    }
}

// Material Processing
function initMaterialProcessing() {
    const materialForm = document.getElementById('material-form');
    if (materialForm) {
        materialForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = materialForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
            
            // Get material text
            const materialText = document.getElementById('material-text').value;
            const materialFile = document.getElementById('material-file').files[0]?.name;
            
            if (!materialText && !materialFile) {
                showToast('Please enter text or select a file', 'warning');
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
                return;
            }
            
            // Submit to API
            fetch('/api/process-material', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    material_text: materialText,
                    material_file: materialFile
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showToast('Material processed successfully!', 'success');
                    
                    // Display the results
                    displayProcessedMaterial(materialText, data.result);
                } else {
                    // Show error message
                    showToast('Error: ' + data.error, 'error');
                }
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An unexpected error occurred. Please try again.', 'error');
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            });
        });
    }
}

// Display processed material
function displayProcessedMaterial(originalText, processedResult) {
    const resultsContainer = document.getElementById('results-container');
    if (!resultsContainer) return;
    
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    // Create material container
    const materialContainer = document.createElement('div');
    materialContainer.className = 'material-container fade-in';
    
    // Original material
    const originalMaterial = document.createElement('div');
    originalMaterial.className = 'original-material';
    originalMaterial.innerHTML = `
        <h3 class="material-title">Original Material</h3>
        <div class="material-content">${originalText}</div>
    `;
    
    // Adapted material
    const adaptedMaterial = document.createElement('div');
    adaptedMaterial.className = 'adapted-material';
    adaptedMaterial.innerHTML = `
        <h3 class="material-title">Adapted Material</h3>
        <div class="material-content">${processedResult.adapted_content || 'No adaptations made.'}</div>
    `;
    
    // Add to container
    materialContainer.appendChild(originalMaterial);
    materialContainer.appendChild(adaptedMaterial);
    
    // Add support strategies
    const strategiesContainer = document.createElement('div');
    strategiesContainer.className = 'card fade-in';
    strategiesContainer.innerHTML = `
        <h3 class="card-title">Support Strategies</h3>
        <div class="card-body">
            <ul>
                ${processedResult.support_strategies?.map(strategy => `<li>${strategy}</li>`).join('') || '<li>No specific strategies recommended.</li>'}
            </ul>
        </div>
    `;
    
    // Add to results container
    resultsContainer.appendChild(materialContainer);
    resultsContainer.appendChild(strategiesContainer);
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

// Load sample materials
function loadSampleMaterials() {
    const samplesContainer = document.getElementById('sample-materials');
    if (!samplesContainer) return;
    
    // Show loading state
    samplesContainer.innerHTML = '<div class="loading-container"><span class="spinner"></span><p>Loading samples...</p></div>';
    
    // Fetch samples from API
    fetch('/api/get-sample-materials')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.samples.length > 0) {
                // Clear loading state
                samplesContainer.innerHTML = '';
                
                // Create sample cards
                data.samples.forEach(sample => {
                    const sampleCard = document.createElement('div');
                    sampleCard.className = 'card';
                    sampleCard.innerHTML = `
                        <h3 class="card-title">${sample.name}</h3>
                        <div class="card-body">
                            <button class="btn load-sample" data-id="${sample.id}">Load Sample</button>
                        </div>
                    `;
                    samplesContainer.appendChild(sampleCard);
                });
                
                // Add event listeners to load buttons
                document.querySelectorAll('.load-sample').forEach(button => {
                    button.addEventListener('click', function() {
                        const sampleId = this.getAttribute('data-id');
                        loadSampleMaterial(sampleId);
                    });
                });
            } else {
                samplesContainer.innerHTML = '<p>No sample materials available.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            samplesContainer.innerHTML = '<p>Error loading samples. Please try again later.</p>';
        });
}

// Load a specific sample material
function loadSampleMaterial(sampleId) {
    const materialTextarea = document.getElementById('material-text');
    if (!materialTextarea) return;
    
    // Show loading state
    materialTextarea.value = 'Loading sample...';
    materialTextarea.disabled = true;
    
    // Fetch sample content
    fetch(`/api/get-sample-material/${sampleId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                materialTextarea.value = data.content;
                showToast('Sample loaded successfully!', 'success');
            } else {
                materialTextarea.value = '';
                showToast('Error: ' + data.error, 'error');
            }
            materialTextarea.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            materialTextarea.value = '';
            materialTextarea.disabled = false;
            showToast('An unexpected error occurred. Please try again.', 'error');
        });
}

// Initialize UI elements
function initUI() {
    // File input handling
    const fileInput = document.getElementById('material-file');
    const fileLabel = document.querySelector('.file-label');
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileLabel.textContent = this.files[0].name;
            } else {
                fileLabel.textContent = 'Choose a file';
            }
        });
    }
}

// Toast notification system
function showToast(message, type = 'info') {
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
        <span class="toast-icon">
            ${type === 'success' ? '✓' : type === 'error' ? '✗' : type === 'warning' ? '⚠' : 'ℹ'}
        </span>
        <span class="toast-message">${message}</span>
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