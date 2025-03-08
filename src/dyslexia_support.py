from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager
from src.utils.text_highlighter import TextHighlighter, get_highlighter_for_user
from src.utils.content_analyzer import get_elements_to_highlight

# 初始化提示管理器和配置
prompt_manager = PromptManager()
config = SystemConfig()

# 句法简化器
def syntax_simplifier(state: Dict) -> Dict:
    """
    重构复杂句式为简短、清晰的表达
    
    具体功能:
    1. 句法复杂度分析，识别嵌套从句和复杂结构
    2. 将长句分解为多个简短陈述句
    3. 优化句子结构，确保主谓宾清晰
    4. 保持原始语义的同时降低处理难度
    5. 生成多个简化级别供选择
    """
    
    # 获取LLM
    llm = get_llm(config)
    
    # 检查是否有学习材料
    if not state.get("learning_materials") or not state["learning_materials"]:
        # 如果没有学习材料，创建一个示例内容
        print("没有找到学习材料，使用示例内容")
        state["learning_materials"] = {
            "current_content": """
            全球气候变化是一个由多种复杂且相互关联的因素驱动的现象，这些因素包括但不限于大气中温室气体浓度的增加，
            这主要是由于化石燃料的燃烧和工业过程所产生的二氧化碳排放，以及由农业活动、废物处理和土地利用变化引起的
            其他温室气体如甲烷和氧化亚氮的排放增加所致，同时还受到太阳辐射变化、火山活动等自然因素的影响，所有这些
            因素共同作用，导致了全球气温的持续上升，进而引发了一系列环境问题，如极端天气事件频率增加、海平面上升、
            生物多样性减少等，这些问题对人类社会的各个方面都构成了严峻挑战。
            """,
            "title": "全球气候变化",
            "type": "text",
            "difficulty_level": "advanced",
            "estimated_reading_time_minutes": 20
        }
    elif "current_content" not in state["learning_materials"]:
        # 如果有学习材料但没有current_content，使用第一个可用的内容
        if isinstance(state["learning_materials"], dict) and len(state["learning_materials"]) > 0:
            # 尝试找到内容字段
            content_keys = [k for k in state["learning_materials"].keys() 
                           if k in ["content", "text", "material", "body"]]
            if content_keys:
                state["learning_materials"]["current_content"] = state["learning_materials"][content_keys[0]]
            else:
                # 如果找不到内容字段，使用第一个非标题、非类型的字段
                exclude_keys = ["title", "type", "difficulty_level", "estimated_reading_time_minutes"]
                content_keys = [k for k in state["learning_materials"].keys() if k not in exclude_keys]
                if content_keys:
                    state["learning_materials"]["current_content"] = state["learning_materials"][content_keys[0]]
                else:
                    # 如果还是找不到，使用示例内容
                    print("无法从学习材料中提取内容，使用示例内容")
                    state["learning_materials"]["current_content"] = """
                    全球气候变化是一个由多种复杂且相互关联的因素驱动的现象，这些因素包括但不限于大气中温室气体浓度的增加，
                    这主要是由于化石燃料的燃烧和工业过程所产生的二氧化碳排放，以及由农业活动、废物处理和土地利用变化引起的
                    其他温室气体如甲烷和氧化亚氮的排放增加所致，同时还受到太阳辐射变化、火山活动等自然因素的影响，所有这些
                    因素共同作用，导致了全球气温的持续上升，进而引发了一系列环境问题，如极端天气事件频率增加、海平面上升、
                    生物多样性减少等，这些问题对人类社会的各个方面都构成了严峻挑战。
                    """
    
    # 获取当前内容
    current_content = state["learning_materials"]["current_content"]
    
    # 获取用户分析结果
    user_analysis = state.get("user_profile", {}).get("analysis", {})
    difficulty_type = user_analysis.get("difficulty_type", "Dyslexia")
    
    # 获取用户问卷答案
    questionnaire_answers = state.get("user_profile", {}).get("questionnaire_answers", {})
    
    # 创建提示
    prompt = prompt_manager.get_prompt("dyslexia_simplification") or ChatPromptTemplate.from_messages([
        ("system", """你是一位专门为阅读障碍学生提供支持的教育内容适配专家。你的任务是将复杂的学习材料转化为更易于阅读和理解的形式，同时保留原始内容的教育价值。

请遵循以下原则：
1. 将长句分解为多个简短的陈述句
2. 使用简单、直接的句式结构（主语-谓语-宾语）
3. 避免使用复杂的从句和嵌套结构
4. 用更简单的词汇替换复杂或技术性词汇，但保留关键术语（并提供解释）
5. 保持段落结构和逻辑流程
6. 确保内容的准确性和完整性

对于每个复杂或技术性术语，请提供简短的定义或解释，这些将作为词汇表呈现给学生。

请输出：
1. 简化后的文本
2. 词汇表：包含关键术语及其简明定义"""),
        ("human", "请简化以下学习材料，使其更适合阅读障碍学生：\n\n{content}")
    ])
    
    # 调用LLM
    response = llm.invoke(prompt.format(content=current_content))
    
    # 解析响应
    simplified_text = ""
    vocabulary = {}
    
    # 尝试从响应中提取简化文本和词汇表
    import re
    
    # 查找简化文本部分
    simplified_match = re.search(r'(简化后的文本|Simplified Text):(.*?)(?=(词汇表|Vocabulary)|$)', response.content, re.DOTALL | re.IGNORECASE)
    if simplified_match:
        simplified_text = simplified_match.group(2).strip()
    else:
        # 如果找不到明确的标记，假设前半部分是简化文本
        content_parts = response.content.split('\n\n', 1)
        if len(content_parts) > 1:
            simplified_text = content_parts[0].strip()
        else:
            simplified_text = response.content.strip()
    
    # 查找词汇表部分
    vocabulary_match = re.search(r'(词汇表|Vocabulary):(.*)', response.content, re.DOTALL | re.IGNORECASE)
    if vocabulary_match:
        vocabulary_text = vocabulary_match.group(2).strip()
        
        # 解析词汇表项目
        vocab_items = re.findall(r'[•\-\*]?\s*([^:]+):\s*([^\n]+)', vocabulary_text)
        for term, definition in vocab_items:
            vocabulary[term.strip()] = definition.strip()
    
    # 检查是否需要应用高亮
    should_highlight = False
    reading_patterns = questionnaire_answers.get("reading_patterns", {})
    comprehension_aids = reading_patterns.get("comprehension_aids", [])
    
    if "highlighting" in comprehension_aids:
        should_highlight = True
    
    # 如果需要高亮，识别要高亮的元素并应用高亮
    if should_highlight:
        # 获取用户的高亮器
        highlighter = get_highlighter_for_user(questionnaire_answers)
        
        # 识别要高亮的元素
        elements_to_highlight = get_elements_to_highlight(simplified_text, difficulty_type)
        
        # 将词汇表中的术语添加到定义高亮中
        for term, definition in vocabulary.items():
            elements_to_highlight["definitions"].append({
                "text": term,
                "metadata": {"definition": definition}
            })
        
        # 应用高亮
        for highlight_type, elements in elements_to_highlight.items():
            simplified_text = highlighter.highlight_text(simplified_text, highlight_type, elements)
        
        # 添加CSS样式
        simplified_text = f"<style>{highlighter.get_css()}</style>\n{simplified_text}"
    
    # 更新状态
    if "processed_content" not in state:
        state["processed_content"] = {}
    
    state["processed_content"]["simplified_text"] = {
        "content": simplified_text,
        "vocabulary": vocabulary
    }
    
    # 记录处理历史
    if "interaction_history" not in state:
        state["interaction_history"] = []
    
    state["interaction_history"].append({
        "step": "dyslexia_support_processor",
        "tool": "syntax_simplifier",
        "memory": ["完成阅读障碍支持处理"]
    })
    
    return state

# 词汇替换引擎
def vocabulary_substitution_engine(state: Dict) -> Dict:
    """
    识别潜在困难词汇，提供同义替换或简化解释
    
    具体功能:
    1. 复杂词汇识别算法
    2. 同义词库和简化词汇对照表
    3. 上下文感知的词汇替换
    4. 生成带有词汇解释的增强版本
    5. 支持渐进式词汇学习
    """
    # 实现细节...
    return state
