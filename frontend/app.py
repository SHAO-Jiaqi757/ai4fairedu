#!/usr/bin/env python3
"""
Flask application for AI4FairEdu
"""

import os
import sys
import json
import uuid
import threading
import markdown
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules from the main application
from src.user_profile import analyze_user_profile
from src.adhd_support import micro_content_divider
from src.dyslexia_support import syntax_simplifier
from src.config import SystemConfig
from src.dashboard_analyzer import analyze_dashboard_data

# Initialize configuration
config = SystemConfig()

app = Flask(__name__)
app.secret_key = config.get("app.secret_key") or "dev_key"
app.config['UPLOAD_FOLDER'] = config.get("storage.upload_folder")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['DEBUG'] = True  # Enable debug mode

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Set default language in session
@app.before_request
def set_default_language():
    """Set default language in session if not already set"""
    if 'language' not in session:
        session['language'] = config.get("system.language") or "en"

# Pass debug flag to templates
@app.context_processor
def inject_debug():
    return dict(debug=app.debug)

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
    """Process the uploaded learning material using the AI support system workflow"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    try:
        # Get the material text and title
        material_text = request.form.get('material_text', '')
        material_title = request.form.get('material_title', 'Untitled Material')
        
        print(f"Processing material: {material_title} ({len(material_text)} bytes)")
        
        # Create a unique ID for this material
        user_id = session.get('user_id', datetime.now().strftime("%Y%m%d%H%M%S"))
        material_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Ensure storage directories exist
        material_dir = os.path.join(config.get("storage.learning_materials_path") or "data/materials")
        processing_dir = os.path.join(config.get("storage.results_path") or "data/results", "processing")
        results_dir = os.path.join(config.get("storage.results_path") or "data/results")
        
        os.makedirs(material_dir, exist_ok=True)
        os.makedirs(processing_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)
        
        # Save the material to a file
        material_file_path = os.path.join(material_dir, f"{user_id}_{material_id}.txt")
        with open(material_file_path, 'w') as f:
            f.write(material_text)
        
        # Store material metadata in session
        session['current_material'] = {
            'id': material_id,
            'user_id': user_id,
            'title': material_title,
            'file_path': material_file_path,
            'word_count': len(material_text.split()),
            'estimated_reading_time': len(material_text.split()) // 200
        }
        
        # Create initial processing status file
        processing_status_file = os.path.join(processing_dir, f"{user_id}_{material_id}_status.json")
        with open(processing_status_file, 'w') as f:
            json.dump({
                "status": "started",
                "timestamp": datetime.now().isoformat(),
                "progress": 0
            }, f, indent=2)
        
        # Get user profile data
        user_analysis = session.get('user_analysis', {})
        questionnaire_answers = session.get('questionnaire_answers', {})
        
        # Prepare initial state for the support system workflow
        initial_state = {
            "user_profile": {
                "questionnaire_answers": questionnaire_answers,
                "analysis": user_analysis
            },
            "learning_materials": {
                "title": material_title,
                "current_content": material_text,
                "type": "text",
                "difficulty_level": "intermediate",
                "estimated_reading_time_minutes": len(material_text.split()) // 200
            },
            "processed_content": {},
            "interaction_history": [],
            "current_focus": "start",
            "metadata": {
                "user_id": user_id,
                "material_id": material_id,
                "processing_status_file": processing_status_file,
                "results_dir": results_dir
            },
            "iteration_count": 0
        }
        
        # Import and run the support system workflow
        from src.architecture import build_support_system
        
        # Get the workflow
        workflow = build_support_system()
        
        # Run the workflow in a background thread to avoid blocking
        def process_in_background():
            try:
                print("Building support system workflow graph")
                # Execute the workflow
                # The CompiledStateGraph is not directly callable, we need to use the invoke method
                final_state = workflow.invoke(initial_state)
                
                # Print the raw processed content structure for debugging
                if "processed_content" in final_state:
                    print(f"Raw processed content from agent: {final_state['processed_content'].keys()}")
                else:
                    print("No processed_content in final_state")
                
                # Save the final results
                results_file = os.path.join(results_dir, f"{user_id}_{material_id}_results.json")
                with open(results_file, 'w') as f:
                    json.dump(final_state, f, indent=2)
                
                print(f"Processing complete, results saved to: {results_file}")
                
                # Update processing status to complete
                with open(processing_status_file, 'w') as f:
                    json.dump({
                        "status": "complete",
                        "timestamp": datetime.now().isoformat(),
                        "progress": 100,
                        "message": "Processing complete!",
                        "results_file": results_file
                    }, f, indent=2)
                
            except Exception as e:
                print(f"Error in background processing: {str(e)}")
                import traceback
                traceback.print_exc()
                
                # Update status to error
                with open(processing_status_file, 'w') as f:
                    json.dump({
                        "status": "error",
                        "timestamp": datetime.now().isoformat(),
                        "error": str(e)
                    }, f, indent=2)
        
        # Start background processing
        import threading
        processing_thread = threading.Thread(target=process_in_background)
        processing_thread.start()
        
        # Redirect to processing page
        return redirect(url_for('material_processing'))
        
    except Exception as e:
        print(f"Error processing material: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

@app.route('/learning-view')
def learning_view():
    """Render the learning view page with processed content"""
    if 'questionnaire_answers' not in session:
        return redirect(url_for('questionnaire'))
    
    # Get material_id from query string or session
    material_id = request.args.get('material_id')
    
    # If material_id is provided, use it; otherwise use the current_material from session
    if material_id:
        # Store the material_id in session for future use
        if 'current_material' not in session:
            session['current_material'] = {}
        session['current_material']['id'] = material_id
    elif 'current_material' not in session:
        return redirect(url_for('material_upload'))
    else:
        material_id = session.get('current_material', {}).get('id')
    
    if not material_id:
        flash('No material selected. Please upload a material first.', 'warning')
        return redirect(url_for('material_upload'))
    
    user_id = session.get('user_id', 'anonymous')
    
    # Load the material title from the results file
    results_dir = os.path.join(config.get("storage.results_path") or "data/results")
    results_file = os.path.join(results_dir, f"{user_id}_{material_id}_results.json")
    
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            material_title = results.get("learning_materials", {}).get("title", "Learning Material")
            session['current_material']['title'] = material_title
        except Exception as e:
            print(f"Error loading results file: {str(e)}")
            material_title = session.get('current_material', {}).get('title', 'Learning Material')
    else:
        material_title = session.get('current_material', {}).get('title', 'Learning Material')
    
    # Load processed content
    processed_content, original_content = load_processed_content(user_id, material_id)
    
    if not processed_content:
        flash('Material processing not complete. Please wait a moment.', 'info')
        return redirect(url_for('material_processing'))
    
    print(f"Loaded processed content for material {material_id}:")
    print(f"Processed content keys: {processed_content.keys()}")
    if "detailed_units" in processed_content:
        print(f"Found {len(processed_content['detailed_units'])} detailed units in processed_content")
        print(f"First detailed unit: {processed_content['detailed_units'][0] if processed_content['detailed_units'] else 'None'}")
    else:
        print("No detailed_units found in processed_content")
    
    print(f"Processed content sections: {len(processed_content.get('sections', []))}")
    
    # Get user profile
    user_profile = session.get('user_analysis', {})
    print(f"User profile: {user_profile}")
    
    # Get interaction history for agent explanation
    interaction_history = processed_content.get('interaction_history', [])
    
    # Handle different field names in the user profile
    if 'difficulty_type' not in user_profile and 'learning_disability' in user_profile:
        user_profile['difficulty_type'] = user_profile['learning_disability']
    
    if 'support_level' not in user_profile and 'severity_level' in user_profile:
        severity = user_profile.get('severity_level', 3)
        if severity <= 2:
            user_profile['support_level'] = 'minimal'
        elif severity <= 4:
            user_profile['support_level'] = 'moderate'
        else:
            user_profile['support_level'] = 'extensive'
    
    # Set default values if user profile is empty
    if not user_profile or 'difficulty_type' not in user_profile:
        # Check if we can infer from questionnaire answers
        questionnaire_answers = session.get('questionnaire_answers', {})
        learning_difficulties = questionnaire_answers.get('learning_difficulties', {})
        diagnosed_conditions = learning_difficulties.get('diagnosed_conditions', [])
        
        if 'ADHD' in diagnosed_conditions and 'Dyslexia' in diagnosed_conditions:
            user_profile['difficulty_type'] = 'Combined'
        elif 'ADHD' in diagnosed_conditions:
            user_profile['difficulty_type'] = 'ADHD'
        elif 'Dyslexia' in diagnosed_conditions:
            user_profile['difficulty_type'] = 'Dyslexia'
        else:
            user_profile['difficulty_type'] = 'Standard'
        
        if 'support_level' not in user_profile:
            user_profile['support_level'] = 'moderate'
    
    # Get agents used from the interaction history
    agents_used = []
    for interaction in interaction_history:
        if 'step' in interaction and interaction['step'] not in [agent['id'] for agent in agents_used]:
            agent_id = interaction['step']
            agent_name = agent_id.replace('_', ' ').title()
            
            # Determine agent icon and description
            icon = 'default.svg'
            description = 'Processed your content'
            
            if 'profile' in agent_id:
                icon = 'profile-analyzer.svg'
                description = 'Analyzed your learning profile'
            elif 'adhd' in agent_id:
                icon = 'adhd-support.svg'
                description = 'Created micro-content units for better focus'
            elif 'dyslexia' in agent_id:
                icon = 'dyslexia-support.svg'
                description = 'Simplified text for easier reading'
            elif 'highlight' in agent_id:
                icon = 'highlighter.svg'
                description = 'Highlighted important content'
            
            agents_used.append({
                'id': agent_id,
                'name': agent_name,
                'icon': url_for('static', filename=f'images/team/{icon}'),
                'description': description
            })
    
    # If no agents were found in the interaction history, add default agents based on user profile
    if not agents_used:
        if user_profile.get('difficulty_type') == 'ADHD' or user_profile.get('difficulty_type') == 'Combined':
            agents_used.append({
                'id': 'adhd_support',
                'name': 'Focus Enhancer',
                'icon': url_for('static', filename='images/team/adhd-support.svg'),
                'description': 'Created micro-content units for better focus'
            })
        
        if user_profile.get('difficulty_type') == 'Dyslexia' or user_profile.get('difficulty_type') == 'Combined':
            agents_used.append({
                'id': 'dyslexia_support',
                'name': 'Text Transformer',
                'icon': url_for('static', filename='images/team/dyslexia-support.svg'),
                'description': 'Simplified text for easier reading'
            })
    
    return render_template('learning_view.html',
                          material_title=material_title,
                          user_profile=user_profile,
                          processed_content=processed_content,
                          original_content=original_content,
                          agents_used=agents_used)

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

@app.route('/material-processing')
def material_processing():
    """Render the material processing page"""
    if 'questionnaire_answers' not in session or 'current_material' not in session:
        return redirect(url_for('material_upload'))
    
    return render_template('material_processing.html', 
                          material=session.get('current_material', {}),
                          user_analysis=session.get('user_analysis', {}))

@app.route('/api/check-processing-status')
def check_processing_status():
    """API endpoint to check the status of material processing"""
    if 'current_material' not in session:
        return jsonify({"error": "No material being processed"})
    
    material = session.get('current_material', {})
    material_id = material.get('id')
    user_id = session.get('user_id')
    
    if not material_id or not user_id:
        return jsonify({"error": "Invalid material or user ID"})
    
    # Check if processing status file exists
    processing_dir = os.path.join(config.get("storage.results_path") or "data/results", "processing")
    status_file = os.path.join(processing_dir, f"{user_id}_{material_id}_status.json")
    
    if not os.path.exists(status_file):
        return jsonify({"error": "Status file not found"}), 404
    
    try:
        with open(status_file, 'r') as f:
            status_data = json.load(f)
        
        # If processing is complete, include agent insights and file references
        if status_data.get('status') == 'complete':
            results_file = status_data.get('results_file')
            if results_file and os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    results_data = json.load(f)
                
                # Extract agent insights from processing history
                agent_insights = []
                for entry in results_data.get('processing_history', []):
                    if 'step' in entry and 'memory' in entry:
                        agent_insights.append({
                            'agent': entry.get('step', '').replace('_', ' ').title(),
                            'action': entry.get('memory', ['No action recorded'])[0]
                        })
                
                # Add agent insights to status data
                status_data['agent_insights'] = agent_insights
                
                # Add file references to status data
                status_data['file_references'] = {
                    'micro_units_file': results_data.get('processed_content', {}).get('micro_units_file'),
                    'simplified_text_file': results_data.get('processed_content', {}).get('simplified_text_file'),
                    'original_content_file': results_data.get('learning_materials', {}).get('file_path')
                }
                
                # Update session with file references
                micro_units_file = results_data.get('processed_content', {}).get('micro_units_file')
                simplified_text_file = results_data.get('processed_content', {}).get('simplified_text_file')
                original_content_file = results_data.get('learning_materials', {}).get('file_path')
                
                if micro_units_file:
                    session['micro_units_file'] = micro_units_file
                
                if simplified_text_file:
                    session['simplified_text_file'] = simplified_text_file
                
                if original_content_file:
                    session['original_content_file'] = original_content_file
        
        return jsonify(status_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def convert_markdown_to_html(content):
    """
    Convert markdown content to HTML.
    
    Args:
        content: The markdown content to convert
        
    Returns:
        HTML content
    """
    if not content or not isinstance(content, str):
        return content
    
    # Check if content is already HTML
    if content.strip().startswith('<') and ('</p>' in content or '</div>' in content or '</h' in content):
        return content
    
    # Check if content looks like markdown
    if '**' in content or '#' in content or '- ' in content or '1. ' in content or '```' in content:
        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['extra', 'nl2br'])
        return html_content
    
    # If not markdown or HTML, treat as plain text and convert paragraphs
    html_content = ""
    for paragraph in content.split('\n\n'):
        if paragraph.strip():
            html_content += f"<p>{paragraph.strip()}</p>\n"
    return html_content

def load_processed_content(user_id, material_id):
    """
    Load the processed content and original content for a given material.
    
    Args:
        user_id: The user ID
        material_id: The material ID
        
    Returns:
        Tuple of (processed_content, original_content)
    """
    try:
        # Get paths
        results_dir = os.path.join(config.get("storage.results_path") or "data/results")
        material_dir = os.path.join(config.get("storage.learning_materials_path") or "data/materials")
        
        # Load results file
        results_file = os.path.join(results_dir, f"{user_id}_{material_id}_results.json")
        if not os.path.exists(results_file):
            print(f"Results file not found: {results_file}")
            return None, None
            
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        # Extract processed content
        raw_processed_content = results.get("processed_content", {})
        print(f"Raw processed content structure: {raw_processed_content.keys() if raw_processed_content else 'None'}")
        
        # Transform the agent output structure into the format expected by the template
        processed_content = {}
        
        # Check if we have detailed_units directly in the raw_processed_content
        if "detailed_units" in raw_processed_content:
            detailed_units = raw_processed_content["detailed_units"]
            print(f"Found {len(detailed_units)} detailed units directly in raw_processed_content")
            
            # Process detailed_units content
            for unit in detailed_units:
                # Ensure detailed_content is HTML
                if "detailed_content" in unit and unit["detailed_content"] and isinstance(unit["detailed_content"], str):
                    unit["detailed_content"] = convert_markdown_to_html(unit["detailed_content"])
            
            # Add detailed_units to processed_content
            processed_content["detailed_units"] = detailed_units
            print(f"Added {len(detailed_units)} detailed units directly to processed_content")
        
        # Check if we have the raw agent output format (micro_units, simplified_text, etc.)
        if "micro_units" in raw_processed_content or "simplified_text" in raw_processed_content or "general_tools_applied" in raw_processed_content:
            # Create a sections array from the agent output
            sections = []
            
            # Get material info
            material_title = results.get("learning_materials", {}).get("title", "Content")
            original_text = results.get("learning_materials", {}).get("current_content", "")
            
            # Format original text as HTML if it's not already
            if original_text and isinstance(original_text, str):
                original_text = convert_markdown_to_html(original_text)
            
            # Create a section
            section = {
                "id": "section-1",
                "title": material_title,
                "content": original_text,
                "estimated_time": len(original_text.split()) // 200 if original_text else 5,
                "difficulty_level": "Standard"
            }
            
            # Add micro_units if available
            if "micro_units" in raw_processed_content:
                micro_units = raw_processed_content["micro_units"]
                
                # Normalize field names in micro units
                for unit in micro_units:
                    # Ensure estimated_time field exists
                    if "estimated_time" not in unit and "estimated_time_minutes" in unit:
                        unit["estimated_time"] = unit["estimated_time_minutes"]
                    elif "estimated_time" not in unit:
                        unit["estimated_time"] = 2  # Default value
                    
                    # Ensure check_points field exists
                    if "check_points" not in unit and "key_points" in unit:
                        unit["check_points"] = unit["key_points"]
                    elif "check_points" not in unit and "check_questions" in unit:
                        unit["check_points"] = unit["check_questions"]
                    
                    # Ensure content is HTML
                    if "content" in unit and unit["content"] and isinstance(unit["content"], str):
                        unit["content"] = convert_markdown_to_html(unit["content"])
                
                section["micro_units"] = micro_units
                
                # Extract key concepts from micro units if available
                key_concepts = set()
                for unit in micro_units:
                    points_list = []
                    if "key_points" in unit:
                        points_list.extend(unit["key_points"])
                    if "check_points" in unit:
                        points_list.extend(unit["check_points"])
                    
                    for point in points_list:
                        if isinstance(point, str):
                            # Extract potential key concepts (capitalized terms)
                            words = point.split()
                            for word in words:
                                if word and len(word) > 3 and word[0].isupper():
                                    key_concepts.add(word.strip('.,;:()[]{}'))
                
                if key_concepts:
                    section["key_concepts"] = list(key_concepts)
            
            # Add simplified_text if available
            if "simplified_text" in raw_processed_content:
                if isinstance(raw_processed_content["simplified_text"], dict):
                    if "content" in raw_processed_content["simplified_text"]:
                        simplified_content = raw_processed_content["simplified_text"]["content"]
                        # Ensure content is HTML
                        if simplified_content and isinstance(simplified_content, str):
                            simplified_content = convert_markdown_to_html(simplified_content)
                        section["simplified_content"] = simplified_content
                    
                    if "vocabulary" in raw_processed_content["simplified_text"]:
                        section["vocabulary"] = raw_processed_content["simplified_text"]["vocabulary"]
                else:
                    simplified_content = raw_processed_content["simplified_text"]
                    # Ensure content is HTML
                    if simplified_content and isinstance(simplified_content, str):
                        simplified_content = convert_markdown_to_html(simplified_content)
                    section["simplified_content"] = simplified_content
            
            # Add detailed_units to section if available
            if "detailed_units" in processed_content:
                section["detailed_units"] = processed_content["detailed_units"]
                print(f"Added {len(processed_content['detailed_units'])} detailed units to section")
            
            # Add the section to sections array
            sections.append(section)
            
            # Create the processed content structure expected by the template
            processed_content["sections"] = sections
        elif "sections" in raw_processed_content:
            # If the processed content already has a sections array, use it
            processed_content = raw_processed_content
            
            # Check if we need to add detailed_units to the sections
            if "detailed_units" in processed_content and "sections" in processed_content:
                for section in processed_content["sections"]:
                    if "detailed_units" not in section:
                        section["detailed_units"] = processed_content["detailed_units"]
                        print(f"Added {len(processed_content['detailed_units'])} detailed units to existing section")
        else:
            # Create a default structure if we don't have the expected format
            processed_content = {
                "sections": [{
                    "id": "section-1",
                    "title": "Content",
                    "content": original_text,
                    "estimated_time": 5,
                    "difficulty_level": "Standard"
                }]
            }
            
            # Add detailed_units if available
            if "detailed_units" in raw_processed_content:
                processed_content["detailed_units"] = raw_processed_content["detailed_units"]
                processed_content["sections"][0]["detailed_units"] = raw_processed_content["detailed_units"]
        
        # Add interaction history if available
        if "interaction_history" in raw_processed_content:
            processed_content["interaction_history"] = raw_processed_content["interaction_history"]
        
        # Get original content
        original_content = results.get("learning_materials", {}).get("current_content", "")
        
        # Format original content as HTML if it's not already
        if original_content and isinstance(original_content, str):
            original_content = convert_markdown_to_html(original_content)
        
        return processed_content, original_content
    except Exception as e:
        print(f"Error loading processed content: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

@app.route('/materials-history')
def materials_history():
    """Display the user's previously processed learning materials"""
    user_id = session.get('user_id', 'anonymous')
    
    # Get paths
    results_dir = os.path.join(config.get("storage.results_path") or "data/results")
    
    # Get all results files for this user
    materials = []
    if os.path.exists(results_dir):
        for filename in os.listdir(results_dir):
            if filename.startswith(f"{user_id}_") and filename.endswith("_results.json"):
                material_id = filename.replace(f"{user_id}_", "").replace("_results.json", "")
                
                # Load the results file to get material info
                results_file = os.path.join(results_dir, filename)
                try:
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Extract material info
                    material_title = results.get("learning_materials", {}).get("title", "Untitled Material")
                    processed_date = results.get("metadata", {}).get("processed_date", "Unknown date")
                    
                    # Format the date if it's a timestamp
                    try:
                        if isinstance(processed_date, (int, float)):
                            processed_date = datetime.fromtimestamp(processed_date).strftime('%Y-%m-%d %H:%M')
                    except:
                        pass
                    
                    # Get content length
                    content_length = len(results.get("learning_materials", {}).get("current_content", ""))
                    
                    # Add to materials list
                    materials.append({
                        "id": material_id,
                        "title": material_title,
                        "processed_date": processed_date,
                        "content_length": content_length,
                        "has_micro_units": "micro_units" in results.get("processed_content", {})
                    })
                except Exception as e:
                    print(f"Error loading results file {filename}: {str(e)}")
    
    # Sort materials by processed date (newest first)
    materials.sort(key=lambda x: x["processed_date"], reverse=True)
    
    return render_template('materials_history.html', materials=materials)

if __name__ == '__main__':
    # Exempt certain routes from CSRF protection (we'll handle it manually for AJAX)
    csrf.exempt(submit_feedback)
    csrf.exempt(set_language)
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
