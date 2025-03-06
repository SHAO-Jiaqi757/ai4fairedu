"""LLM配置与实例化工具"""

from langchain_openai import ChatOpenAI
from src.config import SystemConfig

def get_llm(config: SystemConfig = None):
    """
    根据配置获取LLM实例
    
    Args:
        config: 系统配置实例，如果为None则创建新实例
        
    Returns:
        初始化好的ChatOpenAI实例
    """
    if config is None:
        config = SystemConfig()
    
    # 从配置中获取LLM设置
    model = config.get("llm.model")
    temperature = config.get("llm.temperature")
    max_tokens = config.get("llm.max_tokens")
    base_url = config.get("llm.base_url")
    api_key = config.get("llm.api_key")

    # 创建并返回LLM实例
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url
    )