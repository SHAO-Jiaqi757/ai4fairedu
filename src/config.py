from typing import Dict, Any
import os
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
        """更新配置项"""
        parts = path.split(".")
        config = self.config
        for part in parts[:-1]:
            if part not in config:
                config[part] = {}
            config = config[part]
        config[parts[-1]] = value 