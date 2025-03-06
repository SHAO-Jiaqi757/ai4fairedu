from src.prompts.prompt_manager import PromptTemplate

def profile_analyzer_en_prompt() -> PromptTemplate:
    """User learning disability profile analysis prompt in English"""
    
    system_message = """As a learning disability assessment expert, your task is to analyze user questionnaire responses, identify possible learning disability types and specific characteristics. Please follow these scientific principles:

1. Diagnostic criteria: Use the diagnostic criteria for ADHD and reading disorders (dyslexia) from DSM-5 (Diagnostic and Statistical Manual of Mental Disorders, 5th Edition) as the basis for assessment.
2. Multi-dimensional assessment: Consider multiple dimensions such as cognitive processing speed, executive function, working memory, phonological awareness, etc.
3. Severity differentiation: Grade according to the degree of impact on daily learning (mild, moderate, severe).
4. Comorbidity consideration: Pay attention to the possibility of comorbidity between ADHD and reading disorders, identifying unique symptoms of each.
5. Strength identification: Identify the user's cognitive and learning strengths for developing compensatory strategies.

Your output should be in JSON format, including the following fields:
- difficulty_type: Learning disability type (ADHD, Dyslexia, Combined, None)
- severity_level: Severity level (1-5)
- specific_features: Specific behavioral characteristics
- strengths: Cognitive and learning strengths
- recommended_strategies: Recommended support strategies

Please ensure that your analysis is both scientifically based and practical, able to directly guide subsequent personalized adjustments of the support system."""

    # Few-shot examples
    examples = [
        {
            "human": """Here are the user's assessment questionnaire responses:
{input}""",
            
            "assistant": """
{
  "difficulty_type": "ADHD",
  "severity_level": 4,
  "specific_features": {
    "attention": {
      "sustained_attention": "Severely insufficient, can maintain focus for about 20 minutes",
      "selective_attention": "Significantly decreased attention to uninteresting content",
      "divided_attention": "Difficulty switching tasks, easily interrupted"
    },
    "executive_function": {
      "organization": "Severe difficulty, struggles to independently plan complex tasks",
      "working_memory": "Notably insufficient, frequently forgets daily tasks",
      "impulse_control": "Moderate difficulty, struggles to sit still, needs physical activity"
    }
  },
  "strengths": {
    "hyper_focus": "May exhibit exceptional focus on topics of interest",
    "divergent_thinking": "May have potential for divergent thinking and creative thought"
  },
  "recommended_strategies": {
    "primary": [
      "Task breakdown: Break complex tasks into small units completable in 15-20 minutes",
      "Time management: Use the Pomodoro technique and visual timers to enhance time perception",
      "External reminder system: Establish a multi-level reminder system to prevent forgetting"
    ],
    "secondary": [
      "Environment optimization: Reduce environmental distractions",
      "Physical activity integration: Schedule brief physical activities during learning"
    ]
  }
}
"""
        }
    ]
    
    return PromptTemplate(
        name="profile_analyzer_en",
        description="Analyze user questionnaire responses, identify learning disability types and characteristics",
        system_message=system_message,
        few_shot_examples=examples
    ) 