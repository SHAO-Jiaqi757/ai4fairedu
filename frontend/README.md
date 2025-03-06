# AI4FairEdu Frontend

This directory contains the frontend components of the AI4FairEdu system, a learning support platform designed for students with ADHD and dyslexia.

## Directory Structure

```
frontend/
├── app.py                 # Main Flask application
├── static/                # Static assets
│   ├── css/               # CSS stylesheets
│   │   ├── main.css       # Main stylesheet for all pages
│   │   └── learning_view.css  # Specific styles for learning view
│   ├── js/                # JavaScript files
│   │   ├── main.js        # Main JavaScript for all pages
│   │   └── learning_view.js   # Specific scripts for learning view
│   ├── images/            # Image assets
│   └── sounds/            # Sound files for notifications
└── templates/             # HTML templates
    ├── base.html          # Base template with common elements
    ├── index.html         # Landing page
    ├── about.html         # About page
    ├── questionnaire.html # User questionnaire
    ├── dashboard.html     # User dashboard
    ├── material_upload.html # Material upload page
    └── learning_view.html # Learning view page
```

## Pages

1. **Landing Page (index.html)**
   - Introduction to the AI4FairEdu system
   - Call-to-action to start the questionnaire

2. **About Page (about.html)**
   - Information about the project
   - Explanation of how the system helps students with ADHD and dyslexia

3. **Questionnaire (questionnaire.html)**
   - Collects information about the user's learning difficulties and preferences
   - Used to personalize the learning experience

4. **Dashboard (dashboard.html)**
   - Displays the user's profile analysis
   - Shows recommended support strategies
   - Provides access to learning materials

5. **Material Upload (material_upload.html)**
   - Allows users to upload learning materials
   - Processes the materials for adaptation

6. **Learning View (learning_view.html)**
   - Displays the processed learning materials
   - Provides different views based on the user's learning difficulties:
     - Original text
     - Micro content units (for ADHD)
     - Simplified text (for dyslexia)
   - Includes learning tools:
     - Study timer
     - Notes
     - Feedback mechanism

## Features

### Accessibility Features
- Dyslexic-friendly font option
- High contrast mode
- Adjustable font size
- Line spacing control

### ADHD Support
- Content broken down into micro units
- Estimated time for each unit
- Key points highlighted
- Progress tracking

### Dyslexia Support
- Simplified syntax
- Vocabulary assistance
- Bionic reading mode
- Text-to-speech functionality

### Learning Tools
- Pomodoro-style study timer
- Note-taking capability with auto-save
- Feedback system for continuous improvement

## Development

### Requirements
- Python 3.10+
- Flask 3.1.0+
- Flask-WTF 1.2.1+

### Running the Application
1. Install dependencies using Poetry:
   ```
   poetry install
   ```

2. Run the Flask application:
   ```
   poetry run python frontend/app.py
   ```

3. Access the application at http://localhost:5000

## Contributing
Contributions to improve the frontend are welcome. Please ensure that any changes maintain or enhance the accessibility features for students with ADHD and dyslexia. 