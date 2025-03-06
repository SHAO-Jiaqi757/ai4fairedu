from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

# 导入基础模块
from src.prompts.base import PromptTemplate

# 导入所有提示模板函数
from src.prompts.profile_analyzer import profile_analyzer_prompt
from src.prompts.profile_analyzer_en import profile_analyzer_en_prompt
from src.prompts.micro_content_divider import micro_content_divider_prompt
from src.prompts.syntax_simplifier import syntax_simplifier_prompt
from src.prompts.intervention_effectiveness import intervention_effectiveness_prompt

class PromptTemplate(BaseModel):
    """提示模板定义"""
    name: str
    description: str
    system_message: str
    few_shot_examples: Optional[List[Dict[str, str]]] = None
    
    def to_langchain_template(self) -> ChatPromptTemplate:
        """转换为LangChain ChatPromptTemplate"""
        messages = [("system", self.system_message)]
        
        # 添加few-shot examples
        if self.few_shot_examples:
            for example in self.few_shot_examples:
                for role, content in example.items():
                    messages.append((role, content))
        
        # 添加用户输入占位符
        messages.append(("human", "{input}"))
        
        return ChatPromptTemplate.from_messages(messages)

class PromptManager:
    """提示管理器"""
    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self):
        """加载所有预定义提示"""
        # 用户分析提示
        self.prompts["profile_analyzer"] = profile_analyzer_prompt()
        self.prompts["profile_analyzer_en"] = profile_analyzer_en_prompt()
        
        # ADHD支持提示
        self.prompts["micro_content_divider"] = micro_content_divider_prompt()
        
        # 阅读障碍支持提示
        self.prompts["syntax_simplifier"] = syntax_simplifier_prompt()
        
        # 评估提示
        self.prompts["intervention_effectiveness"] = intervention_effectiveness_prompt()
        
        # 注意：其他提示暂未实现，先注释掉
        # self.prompts["progressive_complexity"] = load_prompt("progressive_complexity")
        # self.prompts["attention_management"] = load_prompt("attention_management")
        # self.prompts["vocabulary_substitution"] = load_prompt("vocabulary_substitution")
        # self.prompts["phonological_awareness"] = load_prompt("phonological_awareness")
    
    def get_prompt(self, prompt_name: str) -> Optional[PromptTemplate]:
        """获取指定提示模板"""
        return self.prompts.get(prompt_name)
    
    def get_langchain_prompt(self, prompt_name: str) -> Optional[ChatPromptTemplate]:
        """获取LangChain格式的提示模板"""
        prompt = self.get_prompt(prompt_name)
        if prompt:
            return prompt.to_langchain_template()
        return None

def load_prompt(prompt_name: str) -> PromptTemplate:
    """从配置文件加载提示模板"""
    # 实际实现中应该从文件或数据库加载
    # 这里使用硬编码示例
    
    # 检查要加载的提示类型
    if prompt_name == "profile_analyzer":
        return profile_analyzer_prompt()
    elif prompt_name == "micro_content_divider":
        return micro_content_divider_prompt()
    # ... 其他提示加载逻辑
    
    raise ValueError(f"未知的提示模板: {prompt_name}") 