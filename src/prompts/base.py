from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

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