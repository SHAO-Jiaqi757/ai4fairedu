from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager

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
                # 使用第一个值作为内容
                first_key = next(iter(state["learning_materials"]))
                state["learning_materials"]["current_content"] = state["learning_materials"][first_key]
        else:
            # 创建一个简单的默认内容
            state["learning_materials"]["current_content"] = "这是一个示例学习内容。请提供实际的学习材料以获得更好的支持。"
    
    # 获取原始内容
    original_content = state["learning_materials"]["current_content"]
    
    # 获取提示
    prompt = prompt_manager.get_langchain_prompt("micro_content_divider")
    # 构建链
    chain = prompt | llm
    
    try:
        print(llm.openai_api_key, llm.openai_api_base)
        # 分割内容
        result = chain.invoke({"input": original_content})
        
        # 解析结果
        micro_units = parse_micro_units(result.content)
        
        # 更新状态
        state["processed_content"]["micro_units"] = micro_units
        state["current_focus"] = "micro_content_complete"
    except Exception as e:
        print(f"微内容分割时出错: {e}")
        # 创建一个简单的默认分割
        state["processed_content"]["micro_units"] = [
            {
                "title": "单元1: 基本概念",
                "objective": "理解核心概念",
                "estimated_time": "5分钟",
                "content": original_content[:len(original_content)//3],
                "interactive_element": "思考这些概念的实际应用",
                "checkpoint": "你能用自己的话解释这个概念吗？",
                "next_step": "继续学习单元2"
            },
            {
                "title": "单元2: 关键细节",
                "objective": "掌握重要细节",
                "estimated_time": "7分钟",
                "content": original_content[len(original_content)//3:2*len(original_content)//3],
                "interactive_element": "尝试举一个例子",
                "checkpoint": "这个概念与之前学习的内容有什么联系？",
                "next_step": "继续学习单元3"
            },
            {
                "title": "单元3: 应用与实践",
                "objective": "应用所学知识",
                "estimated_time": "8分钟",
                "content": original_content[2*len(original_content)//3:],
                "interactive_element": "解决一个简单的相关问题",
                "checkpoint": "你能应用这些知识解决实际问题吗？",
                "next_step": "完成学习"
            }
        ]
        state["current_focus"] = "micro_content_complete"
    
    return state

def parse_micro_units(content: str) -> List[Dict]:
    """解析LLM生成的微内容单元"""
    # 简化实现，实际应该解析LLM返回的格式化内容
    # 这里返回一个示例结果
    return [
        {
            "title": "单元1: 链表基础概念",
            "objective": "理解链表的基本结构和特点",
            "estimated_time": "5分钟",
            "content": "链表是一种线性数据结构，由节点组成，每个节点包含数据和指向下一节点的引用...",
            "interactive_element": "想象一列火车车厢，每节车厢连接到下一节",
            "checkpoint": "链表与数组的主要区别是什么？",
            "next_step": "学习链表的类型"
        },
        {
            "title": "单元2: 链表类型",
            "objective": "区分不同类型的链表",
            "estimated_time": "7分钟",
            "content": "链表主要分为三种类型：单链表、双向链表和循环链表...",
            "interactive_element": "用手指模拟不同链表中的节点连接方式",
            "checkpoint": "双向链表比单链表有什么优势？",
            "next_step": "探索链表操作"
        },
        {
            "title": "单元3: 链表操作",
            "objective": "了解链表的基本操作及其效率",
            "estimated_time": "8分钟",
            "content": "链表操作包括：插入、删除、查找和遍历...",
            "interactive_element": "思考在链表中间插入一个新元素的步骤",
            "checkpoint": "为什么链表的插入操作比数组更高效？",
            "next_step": "学习链表的实际应用"
        }
    ]

# 渐进式复杂度调整器
def progressive_complexity_adjuster(state: Dict) -> Dict:
    """
    根据用户注意力状态动态调整内容复杂度
    
    具体功能:
    1. 创建多层次内容版本(简化、标准、详细)
    2. 监测用户注意力状态指标(互动频率、完成时间)
    3. 实现渐进式内容展现策略
    4. 在注意力下降时提供复习和简化版本
    5. 支持用户手动调整复杂度级别
    """
    # 实现细节...
    return state

# ADHD支持路由器图
def build_adhd_support_graph() -> StateGraph:
    """
    构建ADHD支持系统的工作流图
    """
    workflow = StateGraph(name="adhd_support")
    
    # 添加所有ADHD支持节点
    workflow.add_node("micro_content_divider", micro_content_divider)
    workflow.add_node("progressive_complexity_adjuster", progressive_complexity_adjuster)
    workflow.add_node("key_info_extractor", key_info_extractor)
    workflow.add_node("time_aware_prompt_system", time_aware_prompt_system)
    workflow.add_node("task_breakdown_planner", task_breakdown_planner)
    workflow.add_node("focus_mode_generator", focus_mode_generator)
    workflow.add_node("personalized_connection_generator", personalized_connection_generator)
    workflow.add_node("active_retrieval_exercise_designer", active_retrieval_exercise_designer)
    workflow.add_node("gamification_element_builder", gamification_element_builder)
    
    # 定义工作流逻辑...
    
    return workflow.compile() 