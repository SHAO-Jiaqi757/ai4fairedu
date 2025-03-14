# AI4FairEdu

A learning support system for students with ADHD and dyslexia.

## Features

- **User Profile Analysis**: Analyzes user questionnaire responses to identify learning difficulties and recommend support strategies.
- **Learning Material Adaptation**: Adapts learning materials based on the user's profile to make them more accessible.
- **Multilingual Support**: Supports English and Chinese languages throughout the application.
- **Accessibility Features**: Includes font size adjustment, dyslexic-friendly font, and high contrast mode.

## Language Support

The application supports the following languages:

- English (en)
- Chinese (zh)

Users can switch between languages using the language selector in the top-right corner of the application. The language preference is stored in the user's session and applied to all pages.

### Translation System

The application uses a translation system based on a dictionary of translations stored in `frontend/translations.py`. This file contains translations for all text displayed in the application, organized by section and language.

To add a new language, you need to:

1. Add the language code to the language selector in `frontend/templates/base.html`
2. Add translations for the language in `frontend/translations.py`
3. Update the language validation in `frontend/app.py` to include the new language code

### Dashboard Analysis

When a user changes the language, the dashboard analysis is not regenerated. Instead, the application uses the existing analysis results stored in the database-like structure. This improves performance and provides a better user experience.

## Database-like Storage

The application uses a file-based database-like storage system to store user analysis results. This allows the application to:

1. Store analysis results for multiple languages
2. Avoid regenerating analysis when the user changes language
3. Persist analysis results across sessions

The storage system is implemented in the `SystemConfig` class in `src/config.py`. It provides methods to save and retrieve user analysis results:

- `save_user_analysis(user_id, analysis_data, language)`: Saves analysis results for a user in a specific language
- `get_user_analysis(user_id, language)`: Retrieves analysis results for a user in a specific language

Analysis results are stored in JSON files in the `data/results/user_analysis` directory, with one file per user containing analysis results for all languages.

## Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/username/ai4fairedu.git
   cd ai4fairedu
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```
   OPENAI_API_KEY=your_api_key
   SYSTEM_LANGUAGE=en
   ```

### Running the Application

```
cd frontend
python app.py
```

The application will be available at http://localhost:5000.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 


## todo
[] translate http://10.201.8.114:5001/material-processing
[] progress bar in material processing