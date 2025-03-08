from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager
from src.utils.text_highlighter import TextHighlighter, get_highlighter_for_user
from src.utils.content_analyzer import get_elements_to_highlight

# 初始化提示管理器
prompt_manager = PromptManager()
config = SystemConfig()

# 微内容分割器
def micro_content_divider(state: Dict) -> Dict:
    """
    将长篇内容分解为5-10分钟可完成的学习单元
    
    具体功能:
    1. 内容语义分析，识别自然断点
    2. 按认知负荷估算每个单元完成时间
    3. 为每个单元创建明确的学习目标
    4. 设计即时反馈机制检查理解
    5. 记录用户完成情况以优化未来分割
    """
    
    # 获取LLM
    llm = get_llm(config)
    
    # 检查是否有学习材料
    if not state.get("learning_materials") or not state["learning_materials"]:
        # 如果没有学习材料，创建一个示例内容
        print("没有找到学习材料，使用示例内容")
        state["learning_materials"] = {
            "current_content": """
            数据结构基础 - 链表
            
            链表是一种常见的线性数据结构，由一系列节点组成，每个节点包含数据字段和指向下一个节点的引用。
            与数组不同，链表元素在内存中不是连续存储的，而是通过指针连接。
            
            链表主要分为三种类型：单链表、双向链表和循环链表。单链表中的节点只有一个指向下一节点的指针；
            双向链表的节点有两个指针，分别指向前驱和后继节点；循环链表是首尾相连的链表，最后一个节点指向第一个节点。
            
            链表操作包括：插入、删除、查找和遍历。与数组相比，链表在插入和删除操作上更高效，
            时间复杂度为O(1)，但查找操作效率较低，时间复杂度为O(n)。
            """,
            "title": "数据结构基础 - 链表",
            "type": "text",
            "difficulty_level": "intermediate",
            "estimated_reading_time_minutes": 15
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
                    数据结构基础 - 链表
                    
                    链表是一种常见的线性数据结构，由一系列节点组成，每个节点包含数据字段和指向下一个节点的引用。
                    与数组不同，链表元素在内存中不是连续存储的，而是通过指针连接。
                    
                    链表主要分为三种类型：单链表、双向链表和循环链表。单链表中的节点只有一个指向下一节点的指针；
                    双向链表的节点有两个指针，分别指向前驱和后继节点；循环链表是首尾相连的链表，最后一个节点指向第一个节点。
                    
                    链表操作包括：插入、删除、查找和遍历。与数组相比，链表在插入和删除操作上更高效，
                    时间复杂度为O(1)，但查找操作效率较低，时间复杂度为O(n)。
                    """
    
    # 获取当前内容
    current_content = state["learning_materials"]["current_content"]
    
    # 获取用户分析结果
    user_analysis = state.get("user_profile", {}).get("analysis", {})
    difficulty_type = user_analysis.get("difficulty_type", "ADHD")
    
    # 获取用户问卷答案
    questionnaire_answers = state.get("user_profile", {}).get("questionnaire_answers", {})
    attention_span_minutes = questionnaire_answers.get("attention_span_minutes", 10)
    # 创建提示
    prompt = prompt_manager.get_prompt("micro_content_division") or ChatPromptTemplate.from_messages([
        ("system", """你是一位专门为ADHD学生提供支持的教育内容适配专家。你的任务是将长篇学习材料分解为更小、更易于管理的学习单元，以帮助学生保持注意力和提高学习效果。

请遵循以下原则：
1. 将内容分解为{attention_span_minutes}分钟可完成的学习单元
2. 每个单元应该有明确的焦点和学习目标
3. 识别内容的自然断点和主题转换
4. 为每个单元提取3-5个关键点
5. 估计每个单元的完成时间（基于平均阅读速度）

请输出：
1. 微内容单元列表，每个单元包含：
   - 单元内容
   - 学习目标
   - 关键点列表
   - 估计完成时间（分钟）
   - 理解检查问题（1-2个简短问题)"""),
        ("human", "请将以下学习材料分解为微内容单元，以帮助ADHD学生更好地学习：\n\n{content}")
    ])
    
    # 调用LLM
    response = llm.invoke(prompt.format(attention_span_minutes=attention_span_minutes, content=current_content))
    
    # 解析响应
    micro_units = parse_micro_units(response.content)
    
    # 检查是否需要应用高亮
    should_highlight = False
    reading_patterns = questionnaire_answers.get("reading_patterns", {})
    comprehension_aids = reading_patterns.get("comprehension_aids", [])
    
    if "highlighting" in comprehension_aids:
        should_highlight = True
    
    # 如果需要高亮，为每个微内容单元应用高亮
    if should_highlight:
        # 获取用户的高亮器
        highlighter = get_highlighter_for_user(questionnaire_answers)
        
        # 为每个微内容单元应用高亮
        for unit in micro_units:
            # 识别要高亮的元素
            elements_to_highlight = get_elements_to_highlight(unit["content"], difficulty_type)
            
            # 将关键点添加到主要高亮中
            if "key_points" in unit:
                for point in unit["key_points"]:
                    elements_to_highlight["primary"].append({
                        "text": point,
                        "metadata": {"importance": "high"}
                    })
            
            # 应用高亮
            highlighted_content = unit["content"]
            for highlight_type, elements in elements_to_highlight.items():
                highlighted_content = highlighter.highlight_text(highlighted_content, highlight_type, elements)
            
            # 更新单元内容
            unit["content"] = highlighted_content
            
            # 如果是第一个单元，添加CSS样式
            if unit == micro_units[0]:
                unit["content"] = f"<style>{highlighter.get_css()}</style>\n{unit['content']}"
    
    # 更新状态
    if "processed_content" not in state:
        state["processed_content"] = {}
    
    state["processed_content"]["micro_units"] = micro_units
    
    # 记录处理历史
    if "interaction_history" not in state:
        state["interaction_history"] = []
    
    state["interaction_history"].append({
        "step": "adhd_support_processor",
        "tool": "micro_content_divider",
        "memory": ["完成ADHD支持处理"]
    })
    
    return state

def parse_micro_units(content: str) -> List[Dict[str, Any]]:
    """
    解析LLM生成的微内容单元
    
    Args:
        content: LLM生成的响应内容
    
    Returns:
        微内容单元列表
    """
    import re
    
    # 初始化结果列表
    micro_units = []
    
    # 尝试识别单元分隔符
    unit_patterns = [
        r'单元\s*(\d+)',
        r'微内容单元\s*(\d+)',
        r'学习单元\s*(\d+)',
        r'Unit\s*(\d+)',
        r'Part\s*(\d+)',
        r'Section\s*(\d+)'
    ]
    
    # 查找所有可能的单元分隔点
    unit_boundaries = []
    for pattern in unit_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            unit_boundaries.append((match.start(), int(match.group(1))))
    
    # 按位置排序
    unit_boundaries.sort()
    
    # 如果找不到明确的单元分隔符，尝试按段落分割
    if not unit_boundaries:
        paragraphs = re.split(r'\n\s*\n', content)
        if len(paragraphs) >= 3:  # 至少需要3个段落才考虑按段落分割
            for i, para in enumerate(paragraphs):
                if i == 0 and len(para.strip()) < 100:  # 跳过可能的介绍段落
                    continue
                unit_boundaries.append((content.find(para), i))
    
    # 如果仍然找不到分隔点，将整个内容作为一个单元
    if not unit_boundaries:
        return [{
            "content": content,
            "estimated_time_minutes": 10,
            "key_points": ["请仔细阅读内容以提取关键点"]
        }]
    
    # 提取每个单元的内容
    for i in range(len(unit_boundaries)):
        start_pos = unit_boundaries[i][0]
        unit_num = unit_boundaries[i][1]
        
        # 确定单元结束位置
        if i < len(unit_boundaries) - 1:
            end_pos = unit_boundaries[i+1][0]
        else:
            end_pos = len(content)
        
        unit_content = content[start_pos:end_pos].strip()
        
        # 解析单元内容
        unit = {
            "content": unit_content,
            "unit_number": unit_num,
            "estimated_time_minutes": 5  # 默认估计时间
        }
        
        # 尝试提取学习目标
        objective_match = re.search(r'(学习目标|Learning Objective|Objective)[:：](.*?)(?=\n\n|\n[A-Z]|$)', unit_content, re.IGNORECASE | re.DOTALL)
        if objective_match:
            unit["learning_objective"] = objective_match.group(2).strip()
        
        # 尝试提取关键点
        key_points = []
        key_points_match = re.search(r'(关键点|Key Points|Main Points)[:：](.*?)(?=\n\n|\n[A-Z]|$)', unit_content, re.IGNORECASE | re.DOTALL)
        if key_points_match:
            key_points_text = key_points_match.group(2).strip()
            # 尝试按不同的列表格式分割
            point_matches = re.findall(r'[•\-\*]\s*(.*?)(?=\n[•\-\*]|\n\n|$)', key_points_text)
            if point_matches:
                key_points = [point.strip() for point in point_matches]
            else:
                # 尝试按数字列表分割
                point_matches = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|\n\n|$)', key_points_text)
                if point_matches:
                    key_points = [point.strip() for point in point_matches]
                else:
                    # 按行分割
                    key_points = [line.strip() for line in key_points_text.split('\n') if line.strip()]
        
        if key_points:
            unit["key_points"] = key_points
        
        # 尝试提取估计时间
        time_match = re.search(r'(估计时间|Estimated Time|Time)[:：]\s*(\d+)[^\d]*分钟', unit_content, re.IGNORECASE)
        if time_match:
            unit["estimated_time_minutes"] = int(time_match.group(2))
        
        # 尝试提取理解检查问题
        questions = []
        questions_match = re.search(r'(理解检查|Check Questions|Questions)[:：](.*?)(?=\n\n|\n[A-Z]|$)', unit_content, re.IGNORECASE | re.DOTALL)
        if questions_match:
            questions_text = questions_match.group(2).strip()
            # 尝试按不同的问题格式分割
            question_matches = re.findall(r'[Q\d]+[\.:]?\s*(.*?)(?=\n[Q\d]+[\.:]?|\n\n|$)', questions_text)
            if question_matches:
                questions = [q.strip() for q in question_matches]
            else:
                # 按行分割
                questions = [line.strip() for line in questions_text.split('\n') if line.strip() and '?' in line]
        
        if questions:
            unit["check_questions"] = questions
        
        # 清理单元内容，移除元数据部分
        clean_content = unit_content
        for pattern in [r'(学习目标|Learning Objective|Objective)[:：].*?(?=\n\n|\n[A-Z]|$)', 
                       r'(关键点|Key Points|Main Points)[:：].*?(?=\n\n|\n[A-Z]|$)',
                       r'(估计时间|Estimated Time|Time)[:：].*?(?=\n\n|\n[A-Z]|$)',
                       r'(理解检查|Check Questions|Questions)[:：].*?(?=\n\n|\n[A-Z]|$)']:
            clean_content = re.sub(pattern, '', clean_content, flags=re.IGNORECASE | re.DOTALL)
        
        # 如果清理后的内容不为空，更新单元内容
        clean_content = re.sub(r'\n{3,}', '\n\n', clean_content).strip()
        if clean_content:
            unit["content"] = clean_content
        
        micro_units.append(unit)
    
    return micro_units
