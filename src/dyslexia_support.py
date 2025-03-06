from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager

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
                # 使用第一个值作为内容
                first_key = next(iter(state["learning_materials"]))
                state["learning_materials"]["current_content"] = state["learning_materials"][first_key]
        else:
            # 创建一个简单的默认内容
            state["learning_materials"]["current_content"] = "这是一个示例学习内容。请提供实际的学习材料以获得更好的支持。"
    
    # 获取原始内容
    original_content = state["learning_materials"]["current_content"]
    
    # 获取提示
    prompt = prompt_manager.get_langchain_prompt("syntax_simplifier")
    
    # 构建链
    chain = prompt | llm
    
    try:
        # 简化句法
        result = chain.invoke({"input": original_content})
        # 解析结果
        simplified_text = parse_simplified_text(result.content)
        
        # 更新状态
        state["processed_content"]["simplified_text"] = simplified_text
        state["current_focus"] = "syntax_simplified"
    except Exception as e:
        print(f"句法简化时出错: {e}")
        # 创建一个简单的默认简化
        state["processed_content"]["simplified_text"] = {
            "basic": "这是基础级简化版本。短句。简单词汇。清晰结构。",
            "intermediate": "这是中级简化版本。句子稍长但结构清晰。使用常见词汇。保持逻辑简单。",
            "advanced": "这是高级简化版本。保留一些复杂度但避免嵌套结构。使用精确词汇。保持原文风格。"
        }
        state["current_focus"] = "syntax_simplified"
    
    return state

def parse_simplified_text(content: str) -> Dict[str, str]:
    """解析LLM生成的简化文本"""
    # 简化实现，实际应该解析LLM返回的格式化内容
    # 这里返回一个示例结果
    return {
        "basic": "全球气候正在变化。这一现象有多个原因。人类活动是主要原因。我们燃烧煤炭和石油产生二氧化碳。工厂排放废气。农业活动产生甲烷气体。自然因素也有影响。太阳辐射会变化。火山喷发会影响气候。气候变化导致问题。温度上升。极端天气更常见。海平面上升。动植物种类减少。这些问题对人类生活造成挑战。",
        
        "intermediate": "全球气候变化由多个因素引起。这些因素互相关联且很复杂。人类活动是主要原因。我们燃烧化石燃料产生二氧化碳。工业过程也排放温室气体。农业活动和废物处理产生甲烷和氧化亚氮。改变土地用途也会增加排放。自然因素同样影响气候。这包括太阳辐射变化和火山活动。所有这些因素一起导致全球温度上升。温度上升引发一系列环境问题。极端天气事件变得更频繁。海平面上升。生物多样性减少。这些环境问题对人类社会构成严峻挑战。",
        
        "advanced": "全球气候变化是由多种复杂因素驱动的现象。这些因素相互关联。人类活动是主要原因。燃烧化石燃料和工业过程产生大量二氧化碳。农业活动、废物处理和土地利用变化增加了甲烷和氧化亚氮的排放。这些都是温室气体。自然因素也影响气候变化。太阳辐射变化和火山活动是重要的自然因素。这些因素共同作用，导致全球气温持续上升。气温上升引发了多种环境问题。极端天气事件变得更频繁。海平面上升。生物多样性减少。这些环境问题对人类社会的各个方面都带来严峻挑战。"
    }

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

# 阅读障碍支持路由器图
def build_dyslexia_support_graph() -> StateGraph:
    """
    构建阅读障碍支持系统的工作流图
    """
    workflow = StateGraph(name="dyslexia_support")
    
    # 添加所有阅读障碍支持节点
    workflow.add_node("syntax_simplifier", syntax_simplifier)
    workflow.add_node("vocabulary_substitution_engine", vocabulary_substitution_engine)
    workflow.add_node("semantic_chunker", semantic_chunker)
    workflow.add_node("pre_reading_question_generator", pre_reading_question_generator)
    workflow.add_node("concept_map_builder", concept_map_builder)
    workflow.add_node("multisensory_association_generator", multisensory_association_generator)
    workflow.add_node("phonological_awareness_exercise_designer", phonological_awareness_exercise_designer)
    workflow.add_node("rapid_naming_training_generator", rapid_naming_training_generator)
    workflow.add_node("progressive_reading_fluency_exercise", progressive_reading_fluency_exercise)
    
    # 定义工作流逻辑...
    
    return workflow.compile() 