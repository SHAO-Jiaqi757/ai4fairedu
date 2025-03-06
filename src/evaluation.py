from typing import Dict, List, Any
import pandas as pd
from pydantic import BaseModel
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager

# 初始化配置和提示管理器
config = SystemConfig()
prompt_manager = PromptManager()

class InterventionResult(BaseModel):
    """记录单次支持干预的结果"""
    intervention_type: str  # 干预类型
    intervention_id: str  # 唯一标识符
    user_id: str  # 用户标识符
    difficulty_type: str  # 目标学习困难
    start_time: str  # 开始时间
    completion_time: str  # 完成时间
    engagement_metrics: Dict  # 参与度指标
    comprehension_score: float  # 理解度分数
    user_feedback: Dict  # 用户反馈
    system_adjustments: List  # 系统作出的调整

def evaluate_intervention_effectiveness(interventions: List[InterventionResult]) -> Dict:
    """
    评估支持干预的有效性，并提出优化建议
    
    功能:
    1. 分析不同干预类型的参与度和理解度效果
    2. 识别用户特定的反应模式
    3. 生成针对性的优化建议
    4. 预测未来干预效果
    """
    
    # 获取LLM
    llm = get_llm(config)
    
    # 获取提示
    prompt = prompt_manager.get_langchain_prompt("intervention_effectiveness")
    
    # 将干预结果转换为结构化数据
    df = pd.DataFrame([i.dict() for i in interventions])
    
    # 计算汇总统计数据
    summary_stats = {
        "intervention_types": df.groupby("intervention_type").agg({
            "comprehension_score": ["mean", "std"],
            "engagement_metrics.time_spent": ["mean", "std"],
            "user_feedback.satisfaction": ["mean", "std"]
        }).to_dict(),
        "user_patterns": identify_user_patterns(df),
        "temporal_trends": analyze_temporal_trends(df)
    }
    
    # 使用LLM分析数据并提出优化建议
    optimization_suggestions = generate_optimization_suggestions(llm, summary_stats)
    
    return {
        "summary_statistics": summary_stats,
        "effectiveness_analysis": analyze_effectiveness(summary_stats),
        "optimization_suggestions": optimization_suggestions,
        "prediction_models": build_prediction_models(df)
    } 