from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules from the main application
from src.user_profile import analyze_user_profile
from src.adhd_support import micro_content_divider
from src.dyslexia_support import syntax_simplifier
from src.config import SystemConfig
from src.dashboard_analyzer import analyze_dashboard_data

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_key_for_testing')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize configuration
config = SystemConfig()

# Set default language in session
@app.before_request
def set_default_language():
    if 'language' not in session:
        session['language'] = config.get("system.language")

@app.route('/')
def index():
    """Render the landing page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@app.route('/questionnaire')
def questionnaire():
    """Render the user questionnaire page"""
    return render_template('questionnaire.html')

@app.route('/submit-questionnaire', methods=['POST'])
def submit_questionnaire():
    """Process the questionnaire submission"""
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Remove CSRF token from data before processing
        data.pop('csrf_token', None)
        
        # Process nested form data
        questionnaire_answers = {
            "personal_info": {
                "age": int(data.get('age', 0)),
                "education_level": data.get('education_level', ''),
                "subject_interests": data.get('subject_interests', '').split(',')
            },
            "learning_difficulties": {
                "diagnosed_conditions": data.get('diagnosed_conditions', '').split(','),
                "self_reported_challenges": data.get('self_reported_challenges', '').split(',')
            },
            "attention_patterns": {
                "average_focus_duration_minutes": int(data.get('average_focus_duration', 0)),
                "best_focus_time_of_day": data.get('best_focus_time', '').split(','),
                "distraction_triggers": data.get('distraction_triggers', '').split(','),
                "hyperfocus_activities": data.get('hyperfocus_activities', '').split(',')
            },
            "reading_patterns": {
                "reading_speed": data.get('reading_speed', ''),
                "difficult_text_features": data.get('difficult_text_features', '').split(','),
                "preferred_text_format": {
                    "font": data.get('preferred_font', ''),
                    "size": data.get('preferred_size', ''),
                    "spacing": data.get('preferred_spacing', ''),
                    "background": data.get('preferred_background', '')
                },
                "comprehension_aids": data.get('comprehension_aids', '').split(',')
            },
            "learning_preferences": {
                "modality_preference": {
                    "visual": float(data.get('visual_preference', 0.5)),
                    "auditory": float(data.get('auditory_preference', 0.5)),
                    "kinesthetic": float(data.get('kinesthetic_preference', 0.5))
                },
                "feedback_preference": data.get('feedback_preference', ''),
                "group_vs_individual": data.get('group_vs_individual', ''),
                "technology_comfort": data.get('technology_comfort', '')
            },
            "previous_strategies": {
                strategy: {
                    "effectiveness": int(data.get(f'{strategy}_effectiveness', 0)),
                    "notes": data.get(f'{strategy}_notes', '')
                } for strategy in ['task_breakdown', 'pomodoro_technique', 'text_to_speech', 'concept_mapping']
                if data.get(f'{strategy}_effectiveness')
            }
        }
        
        # Save to session
        session['questionnaire_answers'] = questionnaire_answers
        
        # Clear any existing analysis results
        if 'dashboard_analysis' in session:
            session.pop('dashboard_analysis')
        if 'user_analysis' in session:
            session.pop('user_analysis')
        if 'support_strategies' in session:
            session.pop('support_strategies')
        
        # Save to file for future use
        user_id = datetime.now().strftime("%Y%m%d%H%M%S")
        session['user_id'] = user_id
        
        profile_dir = os.path.join(config.get("storage.user_profiles_path"))
        os.makedirs(profile_dir, exist_ok=True)
        
        with open(os.path.join(profile_dir, f"{user_id}.json"), 'w') as f:
            json.dump({"questionnaire_answers": questionnaire_answers}, f, indent=2)
        
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/dashboard')
def dashboard():
    """Render the user dashboard"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    # Get language setting
    language = session.get('language', config.get("system.language"))
    
    # Check if analysis is already in progress or completed
    user_id = session.get('user_id', 'anonymous')
    analysis_dir = os.path.join(config.get("storage.results_path"), "analysis")
    analysis_file = os.path.join(analysis_dir, f"{user_id}_dashboard_analysis.json")
    analysis_in_progress_file = os.path.join(analysis_dir, f"{user_id}_analysis_in_progress")
    
    # If analysis file exists, try to load it
    if os.path.exists(analysis_file):
        try:
            with open(analysis_file, 'r') as f:
                dashboard_data = json.load(f)
            
            # Store in session and remove the file
            session['dashboard_analysis'] = dashboard_data
            os.remove(analysis_file)
        except Exception as e:
            print(f"Error loading analysis file: {e}")
    
    # Check if we already have analysis results in the session
    if 'dashboard_analysis' not in session:
        # If analysis is not already in progress, start it
        if not os.path.exists(analysis_in_progress_file):
            # Create a file to indicate analysis is in progress
            os.makedirs(analysis_dir, exist_ok=True)
            with open(analysis_in_progress_file, 'w') as f:
                f.write(datetime.now().isoformat())
            
            # Save questionnaire data to a file for the background process to use
            questionnaire_data = session['questionnaire_answers']
            with open(os.path.join(analysis_dir, f"{user_id}_questionnaire.json"), 'w') as f:
                json.dump(questionnaire_data, f, indent=2)
            
            # Start the analysis process using a separate script
            import subprocess
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'run_analysis.py')
            subprocess.Popen([
                sys.executable, 
                script_path, 
                '--user_id', user_id,
                '--language', language
            ])
        
        # Return a template with placeholder data
        return render_template('dashboard.html',
                              analysis={"difficulty_type": "Analysis Pending"},
                              strategies={"primary": [], "secondary": []})
    
    # Get the analysis and strategies from the session
    dashboard_data = session['dashboard_analysis']
    analysis = dashboard_data.get('analysis', {})
    strategies = dashboard_data.get('strategies', {'primary': [], 'secondary': []})
    
    return render_template('dashboard.html', 
                          analysis=analysis,
                          strategies=strategies)

@app.route('/check-analysis')
def check_analysis():
    """Check if the analysis is complete and update the session"""
    if 'user_id' not in session:
        return jsonify({"complete": False})
    
    user_id = session.get('user_id')
    analysis_dir = os.path.join(config.get("storage.results_path"), "analysis")
    analysis_file = os.path.join(analysis_dir, f"{user_id}_dashboard_analysis.json")
    
    if os.path.exists(analysis_file):
        try:
            with open(analysis_file, 'r') as f:
                dashboard_data = json.load(f)
            
            # Store in session
            session['dashboard_analysis'] = dashboard_data
            
            # Remove the file
            os.remove(analysis_file)
            
            return jsonify({"complete": True})
        except Exception as e:
            return jsonify({"complete": False, "error": str(e)})
    
    return jsonify({"complete": False})

@app.route('/material-upload')
def material_upload():
    """Render the material upload page"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    return render_template('material_upload.html')

@app.route('/process-material', methods=['POST'])
def process_material():
    """Process the uploaded learning material"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    try:
        # Get the material text
        material_text = request.form.get('material_text', '')
        material_title = request.form.get('material_title', 'Untitled Material')
        
        # Save the material
        material_dir = os.path.join(config.get("storage.learning_materials_path"))
        os.makedirs(material_dir, exist_ok=True)
        
        user_id = session.get('user_id', datetime.now().strftime("%Y%m%d%H%M%S"))
        material_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        with open(os.path.join(material_dir, f"{user_id}_{material_id}.txt"), 'w') as f:
            f.write(material_text)
        
        # Process the material based on user's difficulty type
        difficulty_type = session.get('user_analysis', {}).get('difficulty_type', 'Unknown')
        
        state = {
            "user_profile": {
                "questionnaire_answers": session['questionnaire_answers'],
                "analysis": session.get('user_analysis', {})
            },
            "learning_materials": {
                "title": material_title,
                "current_content": material_text,
                "type": "text",
                "difficulty_level": "intermediate",
                "estimated_reading_time_minutes": len(material_text.split()) // 200  # Rough estimate
            },
            "processed_content": {},
            "current_focus": "start"
        }
        
        # Apply appropriate processing based on difficulty type
        if difficulty_type == "ADHD" or difficulty_type == "Combined":
            state = micro_content_divider(state)
            session['micro_units'] = state['processed_content'].get('micro_units', [])
        
        if difficulty_type == "Dyslexia" or difficulty_type == "Combined":
            state = syntax_simplifier(state)
            session['simplified_text'] = state['processed_content'].get('simplified_text', {})
        
        # Save the processed state
        results_dir = os.path.join(config.get("storage.results_path"))
        os.makedirs(results_dir, exist_ok=True)
        
        with open(os.path.join(results_dir, f"{user_id}_{material_id}_results.json"), 'w') as f:
            # Convert to serializable format
            serializable_state = {
                "user_profile": state["user_profile"],
                "learning_materials": state["learning_materials"],
                "processed_content": state["processed_content"],
                "current_focus": state["current_focus"]
            }
            json.dump(serializable_state, f, indent=2)
        
        return redirect(url_for('learning_view'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/learning-view')
def learning_view():
    """Render the learning view page"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    micro_units = session.get('micro_units', [])
    simplified_text = session.get('simplified_text', {})
    
    return render_template('learning_view.html', 
                          micro_units=micro_units,
                          simplified_text=simplified_text,
                          difficulty_type=session.get('user_analysis', {}).get('difficulty_type', 'Unknown'))

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback on the processed material"""
    try:
        data = request.json
        
        # Manually validate CSRF token
        csrf_token = data.get('csrf_token')
        if not csrf_token:
            return jsonify({"error": "CSRF token is missing"}), 400
            
        feedback_type = data.get('type')
        feedback_content = data.get('content')
        
        # Save feedback
        feedback_dir = os.path.join(config.get("storage.results_path"), "feedback")
        os.makedirs(feedback_dir, exist_ok=True)
        
        user_id = session.get('user_id', 'anonymous')
        feedback_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        with open(os.path.join(feedback_dir, f"{user_id}_{feedback_id}_feedback.json"), 'w') as f:
            json.dump({
                "type": feedback_type,
                "content": feedback_content,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/set-language', methods=['POST'])
def set_language():
    """Set the user's preferred language"""
    try:
        data = request.json
        language = data.get('language')
        
        # Validate language
        if language not in ['en', 'zh']:
            return jsonify({"error": "Invalid language"}), 400
        
        # Store in session
        session['language'] = language
        
        # Update system config
        config.update("system.language", language)
        
        # Clear any existing dashboard analysis to regenerate in the new language
        if 'dashboard_analysis' in session:
            session.pop('dashboard_analysis')
        
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/refresh-analysis')
def refresh_analysis():
    """Manually trigger a new analysis"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    # Clear any existing analysis results
    if 'dashboard_analysis' in session:
        session.pop('dashboard_analysis')
    
    # Redirect to dashboard to start a new analysis
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Exempt certain routes from CSRF protection (we'll handle it manually for AJAX)
    csrf.exempt(submit_feedback)
    csrf.exempt(set_language)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
