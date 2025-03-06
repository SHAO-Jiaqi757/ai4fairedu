from typing import Dict, Any, List
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.config import SystemConfig
from src.prompts.prompt_manager import PromptManager

# Initialize configuration and prompt manager
config = SystemConfig()
prompt_manager = PromptManager()

def get_llm(config: SystemConfig, language: str = "en"):
    """Get LLM instance based on configuration and language"""
    # Set model parameters based on language
    model = config.get("llm.model")
    temperature = config.get("llm.temperature")
    
    # Adjust temperature for Chinese to ensure more creative output
    if language == "zh":
        temperature = min(temperature + 0.1, 1.0)  # Slightly increase temperature for Chinese
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=config.get("llm.api_key"),
        base_url=config.get("llm.base_url")
    )

def create_dashboard_analyzer_prompt(language: str = "en") -> ChatPromptTemplate:
    """Create a prompt for the dashboard analyzer based on language"""
    if language == "zh":
        system_message = """你是一位专业的学习障碍评估专家，拥有认知神经科学和特殊教育学的深厚背景。你的任务是分析学习问卷并提供基于证据的个性化学习支持策略。

请根据DSM-5诊断标准和最新的教育神经科学研究，对用户的问卷回答进行全面分析，并提供以下信息：

1. 学习障碍类型分析：
   - 评估用户是否表现出ADHD、阅读障碍(读写障碍)或两者兼有的特征
   - 根据DSM-5诊断标准识别关键指标
   - 考虑症状在不同环境下的一致性和持续性

2. 严重程度评估：
   - 根据症状对日常学习和学业表现的影响程度评估严重程度(1-5级)
   - 考虑用户已采用的补偿策略和其有效性
   - 评估功能受损的范围和程度

3. 具体特征分析：
   - 注意力维度：持续注意力、选择性注意力、分配注意力
   - 执行功能：组织能力、工作记忆、冲动控制
   - 阅读能力：阅读速度、解码能力、理解能力
   - 考虑这些特征如何相互作用和影响学习过程

4. 学习优势识别：
   - 识别认知和学习优势，作为补偿策略的基础
   - 评估特定领域的能力和兴趣
   - 确定可以利用的学习偏好和模式

5. 推荐支持策略：
   - 提供基于证据的主要和次要支持策略
   - 确保策略与用户的具体特征和优势相匹配
   - 考虑策略的实用性和可实施性
   - 包括短期干预和长期发展策略

你的分析应基于科学依据，避免过度解释或标签化，同时保持敏感性和尊重。请以JSON格式输出，包含以下字段：

重要提示：请确保你的回答完全使用中文，包括所有分析和建议。

```
{{
  "analysis": {{
    "difficulty_type": "ADHD/Dyslexia/Combined/None",
    "severity_level": 1-5,
    "specific_features": {{
      "attention": {{
        "sustained_attention": "详细描述",
        "selective_attention": "详细描述",
        "divided_attention": "详细描述"
      }},
      "executive_function": {{
        "organization": "详细描述",
        "working_memory": "详细描述",
        "impulse_control": "详细描述"
      }},
      "reading_ability": {{
        "reading_speed": "详细描述",
        "decoding": "详细描述",
        "comprehension": "详细描述"
      }}
    }},
    "strengths": {{
      "cognitive_strengths": "详细描述",
      "learning_preferences": "详细描述",
      "interest_areas": "详细描述"
    }}
  }},
  "strategies": {{
    "primary": ["详细策略1", "详细策略2", "详细策略3"],
    "secondary": ["详细策略1", "详细策略2"]
  }}
}}
```"""
    else:  # English
        system_message = """You are a professional learning disability assessment specialist with extensive background in cognitive neuroscience and special education. Your task is to analyze learning questionnaires and provide evidence-based, personalized learning support strategies.

Please conduct a comprehensive analysis of the user's questionnaire responses based on DSM-5 diagnostic criteria and current educational neuroscience research, providing the following information:

1. Learning Disability Type Analysis:
   - Evaluate whether the user exhibits characteristics of ADHD, reading disorder (dyslexia), or both
   - Identify key indicators according to DSM-5 diagnostic criteria
   - Consider consistency and persistence of symptoms across different environments

2. Severity Assessment:
   - Evaluate severity (level 1-5) based on the impact of symptoms on daily learning and academic performance
   - Consider compensatory strategies already employed by the user and their effectiveness
   - Assess the range and degree of functional impairment

3. Specific Feature Analysis:
   - Attention dimensions: sustained attention, selective attention, divided attention
   - Executive functions: organizational ability, working memory, impulse control
   - Reading abilities: reading speed, decoding skills, comprehension abilities
   - Consider how these features interact with and influence the learning process

4. Learning Strengths Identification:
   - Identify cognitive and learning strengths as a foundation for compensatory strategies
   - Assess capabilities and interests in specific domains
   - Determine learning preferences and patterns that can be leveraged

5. Recommended Support Strategies:
   - Provide evidence-based primary and secondary support strategies
   - Ensure strategies align with the user's specific features and strengths
   - Consider practicality and implementability of strategies
   - Include both short-term interventions and long-term development strategies

Your analysis should be scientifically grounded, avoid over-interpretation or labeling, while maintaining sensitivity and respect. Please output in JSON format, including the following fields:

```
{{
  "analysis": {{
    "difficulty_type": "ADHD/Dyslexia/Combined/None",
    "severity_level": 1-5,
    "specific_features": {{
      "attention": {{
        "sustained_attention": "detailed description",
        "selective_attention": "detailed description",
        "divided_attention": "detailed description"
      }},
      "executive_function": {{
        "organization": "detailed description",
        "working_memory": "detailed description",
        "impulse_control": "detailed description"
      }},
      "reading_ability": {{
        "reading_speed": "detailed description",
        "decoding": "detailed description",
        "comprehension": "detailed description"
      }}
    }},
    "strengths": {{
      "cognitive_strengths": "detailed description",
      "learning_preferences": "detailed description",
      "interest_areas": "detailed description"
    }}
  }},
  "strategies": {{
    "primary": ["detailed strategy 1", "detailed strategy 2", "detailed strategy 3"],
    "secondary": ["detailed strategy 1", "detailed strategy 2"]
  }}
}}
```"""

    # Create the prompt template
    messages = [
        ("system", system_message),
        ("human", "Here are the user's questionnaire responses:\n{questionnaire_data}")
    ]
    
    return ChatPromptTemplate.from_messages(messages)

def analyze_dashboard_data(questionnaire_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
    """
    Analyze questionnaire data and generate dashboard content using an expert LLM
    
    Args:
        questionnaire_data: The user's questionnaire responses
        language: The language to use for the analysis (en or zh)
        
    Returns:
        A dictionary containing the analysis and recommended strategies
    """
    # Validate language parameter
    if language not in ["en", "zh"]:
        print(f"Invalid language: {language}, defaulting to English")
        language = "en"
    
    print(f"Analyzing dashboard data in language: {language}")
    
    # Get LLM
    llm = get_llm(config, language)
    
    # Create prompt based on language
    prompt = create_dashboard_analyzer_prompt(language)
    
    # Create output parser with appropriate settings for the language
    output_parser = JsonOutputParser()
    
    # Create chain
    chain = prompt | llm | output_parser
    
    # Format questionnaire data for the prompt
    formatted_data = json.dumps(questionnaire_data, indent=2, ensure_ascii=False)
    
    # Run the chain
    try:
        result = chain.invoke({"questionnaire_data": formatted_data})
        
        # For Chinese output, ensure proper encoding
        if language == "zh":
            # Check if the output is already in Chinese
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in str(result))
            if not has_chinese:
                print("Warning: Chinese analysis did not return Chinese text")
        
        return result
    except Exception as e:
        print(f"Error analyzing dashboard data: {e}")
        # Return a default response in case of error
        error_message = "请稍后再试" if language == "zh" else "Please try again later."
        return {
            "analysis": {
                "difficulty_type": "Analysis Error",
                "severity_level": 0,
                "specific_features": {},
                "strengths": {}
            },
            "strategies": {
                "primary": [error_message],
                "secondary": []
            }
        } 