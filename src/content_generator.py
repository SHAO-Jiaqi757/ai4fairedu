from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager
from src.utils.text_highlighter import get_highlighter_for_user
from src.utils.content_analyzer import get_elements_to_highlight

# 初始化提示管理器和配置
prompt_manager = PromptManager()
config = SystemConfig()

def content_generator(state: Dict) -> Dict:
    """
    根据微内容单元和原始学习材料生成完整的学习内容
    
    具体功能:
    1. 使用微内容单元的结构和学习目标
    2. 从原始学习材料中提取相关内容
    3. 为每个单元生成详细的学习内容
    4. 保持与用户学习障碍类型相适应的格式
    5. 添加适当的视觉辅助和结构化元素
    """
    
    print("开始执行内容生成器...")
    print(f"当前状态: processed_content keys: {state.get('processed_content', {}).keys()}")
    
    # 获取LLM
    llm = get_llm(config)
    
    # 检查是否有微内容单元和原始学习材料
    if not state.get("processed_content", {}).get("micro_units") or not state.get("learning_materials"):
        print("缺少微内容单元或原始学习材料，无法生成完整内容")
        return state
    
    # 获取微内容单元和原始学习材料
    micro_units = state["processed_content"]["micro_units"]
    learning_materials = state["learning_materials"]
    
    print(f"找到 {len(micro_units)} 个微内容单元")
    
    # 获取用户配置文件以确定适当的格式
    user_profile = state.get("user_profile", {})
    
    # 为每个微内容单元生成详细内容
    detailed_units = []
    
    for unit in micro_units:
        # 创建提示以生成详细内容
        prompt_template = ChatPromptTemplate.from_template("""
        你是一个专门为有学习障碍的学生设计教育内容的AI助手。请根据以下微内容单元的概要和原始学习材料，生成详细的学习内容。

        ## 原始学习材料:
        {original_materials}
        
        ## 微内容单元概要:
        {unit_summary}
        
        ## 用户学习障碍信息:
        {user_profile}
        
        请生成详细的学习内容，满足以下要求:
        1. 内容应该完全覆盖单元概要中提到的所有关键点
        2. 使用清晰、简洁的语言，避免复杂的句式
        3. 包含适当的示例、类比或视觉描述以增强理解
        4. 保持内容的结构化，使用标题、项目符号和短段落
        5. 确保内容的长度适合单元的估计完成时间
        6. 在内容末尾包含单元概要中提到的理解检查问题，并提供简短的参考答案
        
        请以Markdown格式输出内容。
        """)
        
        # 准备提示输入
        prompt_input = {
            "original_materials": learning_materials.get("current_content", ""),
            "unit_summary": unit,
            "user_profile": user_profile.get("analysis", {})
        }
        
        # 调用LLM生成详细内容
        chain = prompt_template | llm
        result = chain.invoke(prompt_input)
        
        # 创建详细单元
        detailed_unit = {
            "unit_number": unit.get("unit_number"),
            "estimated_time_minutes": unit.get("estimated_time_minutes"),
            "summary": unit.get("content"),
            "detailed_content": result.content
        }
        
        detailed_units.append(detailed_unit)
    
    # 将详细单元添加到处理后的内容中
    state["processed_content"]["detailed_units"] = detailed_units
    
    # 更新当前焦点
    state["current_focus"] = "content_generation_complete"
    
    print(f"已为{len(detailed_units)}个微内容单元生成详细内容")
    print(f"详细单元示例: {detailed_units[0] if detailed_units else 'None'}")
    print(f"更新后的状态: processed_content keys: {state.get('processed_content', {}).keys()}")
    
    return state 