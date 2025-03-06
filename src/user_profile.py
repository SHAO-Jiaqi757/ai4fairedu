from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.prompts.prompt_manager import PromptManager
import json

# 初始化配置和提示管理器
config = SystemConfig()
prompt_manager = PromptManager()

class LearningDifficultyProfile(BaseModel):
    """用户学习困难特征模型"""
    
    # 基本信息
    difficulty_type: str = Field(..., description="学习困难类型: ADHD, Dyslexia, 或两者兼有")
    severity_level: int = Field(..., description="严重程度: 1-5, 5最严重")
    
    # ADHD相关特征
    attention_span_minutes: Optional[int] = Field(None, description="平均注意力持续时间(分钟)")
    distraction_triggers: Optional[List[str]] = Field(None, description="常见分心触发因素")
    hyperfocus_topics: Optional[List[str]] = Field(None, description="容易引起深度专注的主题")
    task_switching_difficulty: Optional[int] = Field(None, description="任务切换难度: 1-5")
    
    # 阅读障碍相关特征
    reading_speed_wpm: Optional[int] = Field(None, description="阅读速度(词/分钟)")
    difficult_letter_patterns: Optional[List[str]] = Field(None, description="容易混淆的字母组合")
    phonological_processing: Optional[int] = Field(None, description="音素处理能力: 1-5")
    preferred_text_format: Optional[Dict] = Field(None, description="首选文本格式(字体、大小、间距等)")
    
    # 学习偏好
    learning_modality_preference: Dict[str, float] = Field(..., description="学习模态偏好(视觉、听觉、动觉的权重)")
    optimal_learning_time: List[str] = Field(..., description="最佳学习时间段")
    interest_areas: List[str] = Field(..., description="兴趣领域，用于关联学习")
    previous_strategies: Dict[str, int] = Field(..., description="之前使用的策略及其有效性(1-5)")

def analyze_user_profile(state: Dict) -> Dict:
    """
    分析用户的学习困难特征，生成个性化支持策略
    
    具体功能:
    1. 从用户输入和行为模式识别学习困难特征
    2. 估计各项学习能力的强度和挑战
    3. 创建个性化的支持策略组合
    4. 随用户交互持续优化配置文件
    """
    
    # 获取LLM
    llm = get_llm(config)
    
    # 获取提示
    prompt = prompt_manager.get_langchain_prompt("profile_analyzer")
    
    # 构建链
    chain = prompt | llm
    
    # 检查是否有问卷答案
    if "questionnaire_answers" not in state.get("user_profile", {}):
        # 如果没有问卷答案，使用默认分析
        state["user_profile"]["analysis"] = {
            "difficulty_type": "ADHD",  # 默认假设为ADHD
            "severity_level": 3,  # 中等严重程度
            "specific_features": {
                "attention": {
                    "sustained_attention": "中度不足，能持续关注约30分钟",
                    "selective_attention": "对不感兴趣内容注意力下降",
                    "divided_attention": "任务切换有一定困难"
                },
                "executive_function": {
                    "organization": "中度困难，需要帮助规划复杂任务",
                    "working_memory": "轻度不足，偶尔遗忘任务",
                    "impulse_control": "轻度困难，能保持静坐但需要活动"
                }
            },
            "strengths": {
                "hyper_focus": "对感兴趣主题可能出现良好专注",
                "divergent_thinking": "具有一定思维发散能力"
            }
        }
        
        # 生成支持策略
        state["user_profile"]["support_strategies"] = {
            "primary": [
                "任务分解：将复杂任务分解为20-30分钟可完成的小单元",
                "时间管理：使用视觉计时器增强时间感知",
                "提醒系统：建立基本提醒系统防止遗忘"
            ],
            "secondary": [
                "环境优化：减少主要分心因素",
                "定期休息：每30分钟安排短暂休息"
            ]
        }
        
        state["current_focus"] = "profile_analyzed"
        return state
    
    # 分析用户特征
    try:
        # 将问卷答案转换为字符串格式
        questionnaire_str = json.dumps(state["user_profile"]["questionnaire_answers"], 
                                      ensure_ascii=False, indent=2)
        
        # 调用LLM分析
        result = chain.invoke({"input": questionnaire_str})
        
        # 解析LLM输出为结构化数据
        analysis = parse_json_response(result.content)
        
        # 更新状态
        state["user_profile"]["analysis"] = analysis
        state["user_profile"]["support_strategies"] = generate_support_strategies(analysis)
        state["current_focus"] = "profile_analyzed"
    except Exception as e:
        # 出错时使用默认分析
        print(f"分析用户特征时出错: {e}")
        state["user_profile"]["analysis"] = {
            "difficulty_type": "ADHD",
            "severity_level": 3,
            "specific_features": {
                "attention": {"sustained_attention": "中度不足"},
                "executive_function": {"organization": "中度困难"}
            },
            "strengths": {"adaptability": "较强"}
        }
        state["user_profile"]["support_strategies"] = {
            "primary": ["任务分解", "时间管理"],
            "secondary": ["环境优化"]
        }
        state["current_focus"] = "profile_analyzed"
    
    return state

def parse_json_response(content: str) -> Dict:
    """解析LLM返回的JSON响应"""
    # 简化实现，实际应该使用json.loads并处理可能的解析错误
    # 这里返回一个示例结果
    return {
        "difficulty_type": "ADHD",
        "severity_level": 4,
        "specific_features": {
            "attention": {
                "sustained_attention": "严重不足，能持续关注约20分钟",
                "selective_attention": "对不感兴趣内容注意力显著下降",
                "divided_attention": "任务切换困难，容易被打断"
            },
            "executive_function": {
                "organization": "严重困难，难以自主规划复杂任务",
                "working_memory": "明显不足，经常遗忘日常任务",
                "impulse_control": "中度困难，难以静坐，需要身体活动"
            }
        },
        "strengths": {
            "hyper_focus": "对感兴趣主题可能出现超常专注",
            "divergent_thinking": "可能具有思维发散和创造性思考的潜力"
        }
    }

def generate_support_strategies(analysis: Dict) -> Dict:
    """根据分析生成支持策略"""
    # 简化实现，实际应该根据分析结果生成个性化策略
    # 这里返回一个示例结果
    return {
        "primary": [
            "任务分解：将复杂任务分解为15-20分钟可完成的小单元",
            "时间管理：使用番茄工作法和视觉计时器增强时间感知",
            "外部提醒系统：建立多层次提醒系统防止遗忘"
        ],
        "secondary": [
            "环境优化：减少环境分心因素",
            "身体活动整合：在学习过程中安排短暂的身体活动"
        ]
    }