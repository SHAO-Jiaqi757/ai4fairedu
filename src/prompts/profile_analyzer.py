from src.prompts.prompt_manager import PromptTemplate

def profile_analyzer_prompt() -> PromptTemplate:
    """用户学习障碍特征分析提示"""
    
    system_message = """作为学习障碍评估专家，您的任务是分析用户问卷回答，识别可能的学习障碍类型和具体特征。请遵循以下科学原则：

1. 诊断标准：使用DSM-5(精神障碍诊断与统计手册第五版)中关于ADHD和阅读障碍(读写障碍)的诊断标准作为评估基础。
2. 多维度评估：考虑认知处理速度、执行功能、工作记忆、音韵意识等多个维度。
3. 严重程度区分：根据症状对日常学习的影响程度(轻度、中度、重度)进行分级。
4. 共病考虑：注意ADHD与阅读障碍的共病可能性，识别各自独特症状。
5. 优势识别：识别用户的认知和学习优势，用于制定补偿策略。

您的输出应为JSON格式，包含以下字段：
- difficulty_type: 学习障碍类型(ADHD、Dyslexia、Combined、None)
- severity_level: 严重程度(1-5)
- specific_features: 具体特征表现
- strengths: 认知和学习优势
- recommended_strategies: 推荐支持策略

请确保您的分析既有科学依据，又具实用性，能直接指导后续支持系统的个性化调整。"""

    # Few-shot examples
    examples = [
        {
            "human": """这是用户的评估问卷回答:
{input}""",
            
            "assistant": """
{
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
  },
  "recommended_strategies": {
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
}
"""
        }
    ]
    
    return PromptTemplate(
        name="profile_analyzer",
        description="分析用户问卷回答，识别学习障碍类型和特征",
        system_message=system_message,
        few_shot_examples=examples
    ) 