from typing import Dict, Any
import os
import json
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class SystemConfig:
    """系统配置管理"""
    
    def __init__(self):
        self.config = {
            "llm": {
                "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
                "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4000")),
                "base_url": os.getenv("OPENAI_BASE_URL")
            },
            "logging": {
                "level": os.getenv("LOG_LEVEL", "INFO"),
                "file": os.getenv("LOG_FILE", "support_system.log"),
                "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            },
            "storage": {
                "user_profiles_path": os.getenv("USER_PROFILES_PATH", "data/user_profiles"),
                "learning_materials_path": os.getenv("LEARNING_MATERIALS_PATH", "data/learning_materials"),
                "results_path": os.getenv("RESULTS_PATH", "data/results")
            },
            "system": {
                "max_concurrent_users": int(os.getenv("MAX_CONCURRENT_USERS", "10")),
                "session_timeout": int(os.getenv("SESSION_TIMEOUT", "3600")),
                "default_difficulty_type": os.getenv("DEFAULT_DIFFICULTY_TYPE", "auto_detect"),
                "language": os.getenv("SYSTEM_LANGUAGE", "en")  # Default to English
            }
        }
    
    def get(self, path: str) -> Any:
        """获取配置项，支持点号分隔的路径"""
        parts = path.split(".")
        value = self.config
        for part in parts:
            value = value.get(part)
            if value is None:
                return None
        return value
    
    def update(self, path: str, value: Any) -> None:
        """更新配置项，支持点号分隔的路径"""
        parts = path.split(".")
        config = self.config
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                config[part] = value
            else:
                if part not in config:
                    config[part] = {}
                config = config[part]
    
    def save_user_analysis(self, user_id: str, analysis_data: Dict[str, Any], language: str = "en") -> None:
        """
        Save user analysis results to a file
        
        Args:
            user_id: The user ID
            analysis_data: The analysis data to save
            language: The language of the analysis
        """
        # Create the directory if it doesn't exist
        analysis_dir = os.path.join(self.get("storage.results_path"), "user_analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Save the analysis data
        analysis_file = os.path.join(analysis_dir, f"{user_id}_analysis.json")
        
        # If the file exists, load it first
        existing_data = {}
        if os.path.exists(analysis_file):
            try:
                with open(analysis_file, 'r') as f:
                    existing_data = json.load(f)
            except Exception as e:
                print(f"Error loading existing analysis file: {e}")
        
        # Update the data with the new analysis
        existing_data[language] = analysis_data
        
        # Save the updated data
        with open(analysis_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
    
    def get_user_analysis(self, user_id: str, language: str = "en") -> Dict[str, Any]:
        """
        Get user analysis results from a file
        
        Args:
            user_id: The user ID
            language: The language of the analysis
            
        Returns:
            The analysis data, or None if not found
        """
        # Check if the file exists
        analysis_dir = os.path.join(self.get("storage.results_path"), "user_analysis")
        analysis_file = os.path.join(analysis_dir, f"{user_id}_analysis.json")
        
        if not os.path.exists(analysis_file):
            return None
        
        # Load the data
        try:
            with open(analysis_file, 'r') as f:
                data = json.load(f)
            
            # Return the analysis for the specified language, or None if not found
            return data.get(language)
        except Exception as e:
            print(f"Error loading analysis file: {e}")
            return None 