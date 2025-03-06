from typing import Dict, List, Any, Optional, TypedDict
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END
from src.config import SystemConfig
from src.utils.llm_utils import get_llm

# 导入节点函数
from src.user_profile import analyze_user_profile as profile_analyzer
from src.adhd_support import build_adhd_support_graph, micro_content_divider
from src.dyslexia_support import build_dyslexia_support_graph, syntax_simplifier

# 简单的内存类
class SimpleMemory:
    def __init__(self):
        self.memories = []
    
    def add(self, memory: str):
        self.memories.append(memory)
    
    def get_all(self):
        return self.memories

# 定义系统状态
class SupportSystemState(TypedDict):
    user_profile: Dict  # 用户特征和学习障碍类型
    learning_materials: Dict  # 原始学习材料
    processed_content: Dict  # 经过处理的内容
    interaction_history: List  # 交互历史
    current_focus: str  # 当前工作的焦点区域
    next_steps: List  # 推荐的后续步骤
    metadata: Dict  # 额外信息
    iteration_count: int  # 迭代计数器，用于防止无限循环

# 用户特征分析器
def user_profile_analyzer(state: Dict) -> Dict:
    """分析用户特征"""
    print("执行: 用户特征分析")
    
    # 使用导入的profile_analyzer函数
    result_state = profile_analyzer(state)
    
    # 记录处理历史
    memory = SimpleMemory()
    memory.add("完成用户特征分析")
    result_state["interaction_history"].append({
        "step": "user_profile_analyzer",
        "memory": memory.get_all()
    })
    
    return result_state

# ADHD支持处理器
def adhd_support_processor(state: Dict) -> Dict:
    """提供ADHD支持"""
    print("执行: ADHD支持处理")
    
    # 使用微内容分割器
    result_state = micro_content_divider(state)
    
    # 记录处理历史
    memory = SimpleMemory()
    memory.add("完成ADHD支持处理")
    result_state["interaction_history"].append({
        "step": "adhd_support_processor",
        "tool": "micro_content_divider",
        "memory": memory.get_all()
    })
    
    return result_state

# 阅读障碍支持处理器
def dyslexia_support_processor(state: Dict) -> Dict:
    """提供阅读障碍支持"""
    print("执行: 阅读障碍支持处理")
    
    # 使用句法简化器
    result_state = syntax_simplifier(state)
    
    # 记录处理历史
    memory = SimpleMemory()
    memory.add("完成阅读障碍支持处理")
    result_state["interaction_history"].append({
        "step": "dyslexia_support_processor",
        "tool": "syntax_simplifier",
        "memory": memory.get_all()
    })
    
    return result_state

# 通用学习工具处理器
def general_tools_processor(state: Dict) -> Dict:
    """应用通用学习支持工具"""
    print("执行: 通用学习工具处理")
    
    # 示例实现
    state["processed_content"]["general_tools_applied"] = True
    state["current_focus"] = "all_complete"
    
    # 记录处理历史
    memory = SimpleMemory()
    memory.add("完成通用学习工具处理")
    state["interaction_history"].append({
        "step": "general_tools_processor",
        "memory": memory.get_all()
    })
    
    return state

# 构建主控制图
def build_support_system() -> StateGraph:
    """构建支持系统的工作流图"""
    print("构建支持系统工作流图")
    
    # 创建状态图
    workflow = StateGraph(SupportSystemState)
    
    # 定义路由函数
    def router(state: Dict) -> str:
        # 增加迭代计数
        state["iteration_count"] = state.get("iteration_count", 0) + 1
        print(f"当前迭代次数: {state['iteration_count']}")
        
        # 如果迭代次数过多，强制结束
        if state["iteration_count"] >= 5:
            print("达到最大迭代次数，强制结束")
            return "end"
        
        # 检查处理状态
        if "analysis" not in state.get("user_profile", {}):
            # 如果还没有分析用户特征，先进行分析
            print("路由到: profile_analyzer")
            return "profile_analyzer"
        
        # 检查是否已经完成所有处理
        if state.get("current_focus") == "all_complete":
            print("处理完成，结束流程")
            return "end"
        
        # 检查是否已经进行了微内容分割
        if "micro_units" not in state.get("processed_content", {}):
            # 如果还没有进行微内容分割，进行ADHD支持
            print("路由到: adhd_support")
            return "adhd_support"
        
        # 检查是否已经进行了句法简化
        if "simplified_text" not in state.get("processed_content", {}):
            # 如果还没有进行句法简化，进行阅读障碍支持
            print("路由到: dyslexia_support")
            return "dyslexia_support"
        
        # 如果已经完成了微内容分割和句法简化，使用通用工具
        print("路由到: general_tools")
        return "general_tools"
    
    # 注册节点
    workflow.add_node("router", lambda state: state)  # 路由节点只返回状态，不做修改
    workflow.add_node("profile_analyzer", user_profile_analyzer)
    workflow.add_node("adhd_support", adhd_support_processor)
    workflow.add_node("dyslexia_support", dyslexia_support_processor)
    workflow.add_node("general_tools", general_tools_processor)
    
    # 添加条件路由
    workflow.add_conditional_edges(
        "router",
        router,
        {
            "profile_analyzer": "profile_analyzer",
            "adhd_support": "adhd_support",
            "dyslexia_support": "dyslexia_support",
            "general_tools": "general_tools",
            "end": END
        }
    )
    
    # 从各处理节点返回到路由决策
    workflow.add_edge("profile_analyzer", "router")
    workflow.add_edge("adhd_support", "router")
    workflow.add_edge("dyslexia_support", "router")
    workflow.add_edge("general_tools", "router")
    
    # 设置入口点
    workflow.set_entry_point("router")
    
    return workflow.compile()