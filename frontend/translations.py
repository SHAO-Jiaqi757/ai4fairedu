"""
Translation module for the AI4FairEdu application.
This module provides translations for the application's user interface.
"""

# Dictionary of translations
translations = {
    # Dashboard page
    "dashboard": {
        "en": {
            "title": "Your Learning Dashboard",
            "subtitle": "Personalized insights and support strategies based on your profile",
            "loading": "Analyzing your profile...",
            "refresh_analysis": "Refresh Analysis",
            "profile_summary": "Your Learning Profile",
            "difficulty_type": "Learning Difficulty Type",
            "severity_level": "Severity Level",
            "mild": "Mild",
            "moderate": "Moderate",
            "significant": "Significant",
            "specific_features": "Specific Features",
            "strengths": "Your Strengths",
            "no_features": "No specific features identified yet",
            "no_strengths": "No strengths identified yet",
            "support_strategies": "Recommended Support Strategies",
            "primary_strategies": "Primary Strategies",
            "secondary_strategies": "Secondary Strategies",
            "no_primary": "No primary strategies available yet",
            "no_secondary": "No secondary strategies available yet",
            "next_steps": "Next Steps",
            "upload_material": "Upload Learning Material",
            "upload_description": "Submit text-based learning materials to receive personalized adaptations based on your profile.",
            "upload_button": "Upload Material",
            "view_previous": "View Previous Materials",
            "view_description": "Access your previously processed learning materials and continue your studies.",
            "view_button": "View History",
            "update_profile": "Update Your Profile",
            "update_description": "Retake the questionnaire to update your learning profile as your needs change.",
            "update_button": "Update Profile",
            "learning_resources": "Learning Resources",
            "resources_description": "Explore additional resources and tips for managing your specific learning challenges.",
            "resources_button": "View Resources",
            "progress_tracking": "Your Learning Progress",
            "progress_placeholder1": "Your learning progress will be displayed here as you use the system.",
            "progress_placeholder2": "Upload and study materials to start tracking your progress.",
            "analysis_pending": "Analysis Pending"
        },
        "zh": {
            "title": "您的学习仪表板",
            "subtitle": "基于您的个人资料的个性化见解和支持策略",
            "loading": "正在分析您的个人资料...",
            "refresh_analysis": "刷新分析",
            "profile_summary": "您的学习档案",
            "difficulty_type": "学习困难类型",
            "severity_level": "严重程度",
            "mild": "轻度",
            "moderate": "中度",
            "significant": "显著",
            "specific_features": "具体特征",
            "strengths": "您的优势",
            "no_features": "尚未确定具体特征",
            "no_strengths": "尚未确定优势",
            "support_strategies": "推荐的支持策略",
            "primary_strategies": "主要策略",
            "secondary_strategies": "次要策略",
            "no_primary": "尚无可用的主要策略",
            "no_secondary": "尚无可用的次要策略",
            "next_steps": "下一步",
            "upload_material": "上传学习材料",
            "upload_description": "提交基于文本的学习材料，以根据您的个人资料获取个性化调整。",
            "upload_button": "上传材料",
            "view_previous": "查看以前的材料",
            "view_description": "访问您之前处理过的学习材料并继续您的学习。",
            "view_button": "查看历史",
            "update_profile": "更新您的个人资料",
            "update_description": "重新进行问卷调查，以随着您的需求变化更新您的学习档案。",
            "update_button": "更新档案",
            "learning_resources": "学习资源",
            "resources_description": "探索管理您特定学习挑战的其他资源和提示。",
            "resources_button": "查看资源",
            "progress_tracking": "您的学习进度",
            "progress_placeholder1": "随着您使用系统，您的学习进度将显示在这里。",
            "progress_placeholder2": "上传并学习材料以开始跟踪您的进度。",
            "analysis_pending": "分析待处理"
        }
    },
    
    # Base template
    "base": {
        "en": {
            "site_title": "AI4FairEdu",
            "home": "Home",
            "dashboard": "My",
            "materials": "Upload Materials",
            "questionnaire": "Questionnaire",
            "about": "About",
            "contact": "Contact",
            "increase_font": "Increase Font Size",
            "decrease_font": "Decrease Font Size",
            "toggle_dyslexic": "Toggle Dyslexic-friendly Font",
            "toggle_contrast": "Toggle High Contrast",
            "change_language": "Change Language"
        },
        "zh": {
            "site_title": "AI4FairEdu",
            "home": "首页",
            "dashboard": "我的",
            "materials": "上传学习材料",
            "questionnaire": "问卷调查",
            "about": "关于我们",
            "contact": "联系我们",
            "increase_font": "增大字体",
            "decrease_font": "减小字体",
            "toggle_dyslexic": "切换阅读障碍友好字体",
            "toggle_contrast": "切换高对比度",
            "change_language": "更改语言"
        }
    },
    
    # Home page
    "home": {
        "en": {
            "title": "Welcome to AI4FairEdu",
            "subtitle": "Personalized Learning Support for Students with ADHD and Dyslexia",
            "intro_heading": "Personalized Learning Experience",
            "intro_text": "AI4FairEdu is designed to provide personalized learning support for students with ADHD and dyslexia, making education more accessible and effective.",
            "feature1_title": "Personalized Analysis",
            "feature1_text": "Complete a questionnaire to receive a personalized analysis of your learning profile and recommended support strategies.",
            "feature2_title": "Adaptive Learning Materials",
            "feature2_text": "Upload your learning materials and receive adapted versions that match your learning profile and needs.",
            "feature3_title": "Accessibility Tools",
            "feature3_text": "Use our built-in accessibility tools to customize your learning experience, including font adjustments and high contrast mode.",
            "get_started": "Get Started",
            "learn_more": "Learn More",
            "start_questionnaire": "Start Questionnaire",
            
            # How It Works section
            "how_it_works_title": "How It Works",
            "step1_title": "Complete the Questionnaire",
            "step1_text": "Answer questions about your learning preferences, challenges, and strengths to help us understand your needs.",
            "step2_title": "Receive Your Analysis",
            "step2_text": "Our AI analyzes your responses to identify potential learning difficulties and recommend personalized strategies.",
            "step3_title": "Upload Learning Materials",
            "step3_text": "Submit text-based learning materials that you want to study more effectively.",
            "step4_title": "Study with Personalized Support",
            "step4_text": "Access your transformed learning materials with features tailored to your specific learning needs.",
            
            # Testimonials section
            "testimonials_title": "What Our Users Say",
            "testimonial1_text": "AI4FairEdu has transformed my learning experience. Breaking down complex topics into manageable chunks helps me stay focused and engaged.",
            "testimonial1_author": "Alex Chen",
            "testimonial1_role": "College Student with ADHD",
            "testimonial2_text": "The text simplification feature has made reading academic papers so much easier. I can now understand complex concepts without getting overwhelmed by difficult vocabulary.",
            "testimonial2_author": "Jamie Rodriguez",
            "testimonial2_role": "Graduate Student with Dyslexia",
            "testimonial3_text": "As an educator, I've seen remarkable improvements in my students' engagement and comprehension when using AI4FairEdu. It's a game-changer for inclusive education.",
            "testimonial3_author": "Dr. Sarah Johnson",
            "testimonial3_role": "Special Education Teacher",
            
            # CTA section
            "cta_title": "Ready to Transform Your Learning Experience?",
            "cta_text": "Join thousands of students who have discovered their full potential with AI4FairEdu."
        },
        "zh": {
            "title": "欢迎使用 AI4FairEdu",
            "subtitle": "为 ADHD 和阅读障碍学生提供个性化学习支持",
            "intro_heading": "个性化学习体验",
            "intro_text": "AI4FairEdu 旨在为患有 ADHD 和阅读障碍的学生提供个性化学习支持，使教育更加无障碍和有效。",
            "feature1_title": "个性化分析",
            "feature1_text": "完成问卷调查，获取个性化的学习档案分析和推荐的支持策略。",
            "feature2_title": "自适应学习材料",
            "feature2_text": "上传您的学习材料，获取与您的学习档案和需求相匹配的改编版本。",
            "feature3_title": "无障碍工具",
            "feature3_text": "使用我们内置的无障碍工具来定制您的学习体验，包括字体调整和高对比度模式。",
            "get_started": "开始使用",
            "learn_more": "了解更多",
            "start_questionnaire": "开始问卷调查",
            
            # How It Works section
            "how_it_works_title": "工作原理",
            "step1_title": "完成问卷调查",
            "step1_text": "回答有关您的学习偏好、挑战和优势的问题，帮助我们了解您的需求。",
            "step2_title": "获取您的分析",
            "step2_text": "我们的人工智能分析您的回答，识别潜在的学习困难并推荐个性化策略。",
            "step3_title": "上传学习材料",
            "step3_text": "提交您想要更有效学习的基于文本的学习材料。",
            "step4_title": "使用个性化支持进行学习",
            "step4_text": "访问根据您的特定学习需求定制的转换后的学习材料。",
            
            # Testimonials section
            "testimonials_title": "用户评价",
            "testimonial1_text": "AI4FairEdu 彻底改变了我的学习体验。将复杂的主题分解成可管理的小块帮助我保持专注和投入。",
            "testimonial1_author": "陈亚力",
            "testimonial1_role": "患有 ADHD 的大学生",
            "testimonial2_text": "文本简化功能使阅读学术论文变得容易得多。我现在可以理解复杂的概念，而不会被困难的词汇所淹没。",
            "testimonial2_author": "罗德里格斯杰米",
            "testimonial2_role": "患有阅读障碍的研究生",
            "testimonial3_text": "作为一名教育工作者，我看到使用 AI4FairEdu 时，学生的参与度和理解力有了显著提高。这对包容性教育来说是一个改变游戏规则的工具。",
            "testimonial3_author": "莎拉·约翰逊博士",
            "testimonial3_role": "特殊教育教师",
            
            # CTA section
            "cta_title": "准备好改变您的学习体验了吗？",
            "cta_text": "加入数千名已经发现自己全部潜力的学生的行列。"
        }
    },
    
    # About page
    "about": {
        "en": {
            "title": "About AI4FairEdu",
            "subtitle": "Our Mission and Vision",
            "mission_title": "Our Mission",
            "mission_text": "AI4FairEdu is dedicated to making education more accessible and effective for students with learning difficulties, particularly ADHD and dyslexia, through personalized AI-powered support.",
            "vision_title": "Our Vision",
            "vision_text": "We envision a world where every student, regardless of their learning differences, has equal access to education and can reach their full potential.",
            "how_it_works_title": "How It Works",
            "how_it_works_text": "Our system analyzes your learning profile through a questionnaire and adapts learning materials to match your specific needs and preferences.",
            "team_title": "Our Team",
            "team_text": "We are a team of AI Agents, including educators, technologists, and researchers passionate about making education more inclusive and accessible.",
            "contact_title": "Contact Us",
            "contact_text": "Have questions or feedback? We'd love to hear from you.",
            "contact_email": "Email: contact@ai4fairedu.org",
            
            # Solution Features section
            "solution_title": "Our Solution",
            "solution_text": "AI4FairEdu leverages artificial intelligence to transform standard learning materials into personalized, accessible formats that address the specific needs of students with ADHD and dyslexia.",
            "feature1_title": "Personalized User Profiling",
            "feature1_text": "Our system analyzes each user's learning profile through a comprehensive questionnaire, identifying specific challenges, strengths, and preferences.",
            "feature2_title": "ADHD Support Features",
            "feature2_text": "For students with attention challenges, we provide micro-content segmentation, progressive complexity adjustment, time awareness prompts, and visual engagement enhancements.",
            "feature3_title": "Dyslexia Support Features",
            "feature3_text": "For students with reading difficulties, we offer syntax simplification, vocabulary substitution, text-to-speech integration, and dyslexia-friendly formatting options.",
            "feature4_title": "Adaptive Learning",
            "feature4_text": "Our system continuously learns from user interactions and feedback to improve the personalization and effectiveness of its support features.",
            
            # Team Grid section
            "team_member1_title": "Profile Analyzer",
            "team_member1_role": "Learning Profile Specialist",
            "team_member1_bio": "Analyzes questionnaire responses to identify learning disability characteristics and creates personalized user profiles based on DSM-5 criteria.",
            "team_member2_title": "Focus Enhancer",
            "team_member2_role": "ADHD Support Specialist",
            "team_member2_bio": "Transforms learning materials into micro-content segments with progressive complexity adjustment to maintain attention and engagement.",
            "team_member3_title": "Text Transformer",
            "team_member3_role": "Dyslexia Support Specialist",
            "team_member3_bio": "Simplifies complex syntax and substitutes difficult vocabulary while preserving educational content for improved reading comprehension.",
            "team_member4_title": "Insight Generator",
            "team_member4_role": "Learning Analytics Expert",
            "team_member4_bio": "Analyzes learning patterns and progress to provide actionable insights and personalized recommendations for continuous improvement.",
            
            # CTA section
            "join_cta_title": "Join Us in Making Education Accessible for All",
            "join_cta_text": "Experience the power of personalized learning support designed for your unique needs."
        },
        "zh": {
            "title": "关于 AI4FairEdu",
            "subtitle": "我们的使命和愿景",
            "mission_title": "我们的使命",
            "mission_text": "AI4FairEdu 致力于通过个性化的 AI 支持，使教育对有学习困难的学生（特别是 ADHD 和阅读障碍）更加无障碍和有效。",
            "vision_title": "我们的愿景",
            "vision_text": "我们设想一个世界，每个学生，无论其学习差异如何，都能平等地获得教育并充分发挥其潜力。",
            "how_it_works_title": "工作原理",
            "how_it_works_text": "我们的系统通过问卷调查分析您的学习档案，并根据您的特定需求和偏好调整学习材料。",
            "team_title": "我们的团队",
            "team_text": "我们是一支由AI Agents组成的团队，包括教育工作者、技术专家和研究专家，热衷于使教育更具包容性和无障碍性。",
            "contact_title": "联系我们",
            "contact_text": "有问题或反馈？我们很乐意听取您的意见。",
            "contact_email": "电子邮件：contact@ai4fairedu.org",
            
            # Solution Features section
            "solution_title": "我们的解决方案",
            "solution_text": "AI4FairEdu 利用人工智能将标准学习材料转化为个性化、无障碍的格式，以满足 ADHD 和阅读障碍学生的特定需求。",
            "feature1_title": "个性化用户分析",
            "feature1_text": "我们的系统通过全面的问卷调查分析每个用户的学习档案，识别特定的挑战、优势和偏好。",
            "feature2_title": "ADHD 支持功能",
            "feature2_text": "对于注意力有挑战的学生，我们提供微内容分段、渐进复杂度调整、时间意识提示和视觉参与增强。",
            "feature3_title": "阅读障碍支持功能",
            "feature3_text": "对于有阅读困难的学生，我们提供语法简化、词汇替换、文本转语音集成和阅读障碍友好的格式选项。",
            "feature4_title": "自适应学习",
            "feature4_text": "我们的系统不断从用户互动和反馈中学习，以提高其支持功能的个性化和有效性。",
            
            # Team Grid section
            "team_member1_title": "档案分析师",
            "team_member1_role": "学习档案专家",
            "team_member1_bio": "分析问卷回答以识别学习障碍特征，并基于 DSM-5 标准创建个性化用户档案。",
            "team_member2_title": "专注力增强器",
            "team_member2_role": "ADHD 支持专家",
            "team_member2_bio": "将学习材料转化为微内容段落，通过渐进复杂度调整来保持注意力和参与度。",
            "team_member3_title": "文本转换器",
            "team_member3_role": "阅读障碍支持专家",
            "team_member3_bio": "简化复杂语法并替换困难词汇，同时保留教育内容以提高阅读理解能力。",
            "team_member4_title": "洞察生成器",
            "team_member4_role": "学习分析专家",
            "team_member4_bio": "分析学习模式和进度，提供可行的洞察和个性化建议，以持续改进。",
            
            # CTA section
            "join_cta_title": "加入我们，让教育对所有人都无障碍",
            "join_cta_text": "体验为您的独特需求设计的个性化学习支持的力量。"
        }
    },
    
    # Questionnaire page
    "questionnaire": {
        "en": {
            "title": "Learning Profile Questionnaire",
            "subtitle": "Help us understand your learning needs and preferences",
            "instructions": "Please answer the following questions to help us create your personalized learning profile. This information will be used to adapt learning materials to your specific needs.",
            "personal_info": "Personal Information",
            "age": "Age",
            "education_level": "Education Level",
            "subject_interests": "Subject Interests (comma separated)",
            "learning_difficulties": "Learning Difficulties",
            "diagnosed_conditions": "Diagnosed Conditions (select all that apply)",
            "adhd": "ADHD",
            "dyslexia": "Dyslexia",
            "none": "None",
            "self_reported": "Self-reported Challenges (select all that apply)",
            "attention_patterns": "Attention Patterns",
            "focus_duration": "Average Focus Duration (minutes)",
            "best_focus_time": "Best Focus Time of Day (select all that apply)",
            "morning": "Morning",
            "afternoon": "Afternoon",
            "evening": "Evening",
            "distraction_triggers": "Distraction Triggers (select all that apply)",
            "noise": "Noise",
            "visual_stimuli": "Visual Stimuli",
            "internal_thoughts": "Internal Thoughts",
            "hyperfocus_activities": "Activities that capture your complete attention",
            "reading_patterns": "Reading Patterns",
            "reading_speed": "Reading Speed",
            "slow": "Slow",
            "average": "Average",
            "fast": "Fast",
            "difficult_text_features": "Text Features that are Difficult (select all that apply)",
            "small_font": "Small Font",
            "dense_text": "Dense Text",
            "certain_fonts": "Certain Fonts",
            "preferred_text_format": "Preferred Text Format",
            "font": "Font",
            "size": "Size",
            "spacing": "Spacing",
            "background": "Background Color",
            "comprehension_aids": "Comprehension Aids that Help You",
            "learning_preferences": "Learning Preferences",
            "modality_preference": "Modality Preference (rate from 0 to 1)",
            "visual": "Visual",
            "auditory": "Auditory",
            "kinesthetic": "Kinesthetic",
            "feedback_preference": "Feedback Preference",
            "immediate": "Immediate",
            "delayed": "Delayed",
            "group_vs_individual": "Group vs. Individual Learning",
            "group": "Group",
            "individual": "Individual",
            "mixed": "Mixed",
            "technology_comfort": "Comfort with Technology",
            "low": "Low",
            "medium": "Medium",
            "high": "High",
            "previous_strategies": "Previous Strategies",
            "strategy_effectiveness": "Rate the effectiveness of strategies you've tried",
            "task_breakdown": "Task Breakdown",
            "pomodoro": "Pomodoro Technique",
            "text_to_speech": "Text-to-Speech",
            "concept_mapping": "Concept Mapping",
            "effectiveness": "Effectiveness",
            "not_effective": "Not effective",
            "slightly_effective": "Slightly effective",
            "moderately_effective": "Moderately effective",
            "very_effective": "Very effective",
            "extremely_effective": "Extremely effective",
            "havent_tried": "Haven't tried",
            "notes": "Notes (optional)",
            "previous": "Previous",
            "next": "Next",
            "submit": "Submit Questionnaire"
        },
        "zh": {
            "title": "学习档案问卷",
            "subtitle": "帮助我们了解您的学习需求和偏好",
            "instructions": "请回答以下问题，帮助我们创建您的个性化学习档案。这些信息将用于根据您的特定需求调整学习材料。",
            "personal_info": "个人信息",
            "age": "年龄",
            "education_level": "教育水平",
            "subject_interests": "兴趣科目（用逗号分隔）",
            "learning_difficulties": "学习困难",
            "diagnosed_conditions": "已诊断的情况（选择所有适用项）",
            "adhd": "注意力缺陷多动障碍（ADHD）",
            "dyslexia": "阅读障碍",
            "none": "无",
            "self_reported": "自我报告的挑战（选择所有适用项）",
            "attention_patterns": "注意力模式",
            "focus_duration": "平均专注时间（分钟）",
            "best_focus_time": "一天中最佳专注时间（选择所有适用项）",
            "morning": "上午",
            "afternoon": "下午",
            "evening": "晚上",
            "distraction_triggers": "分心触发因素（选择所有适用项）",
            "noise": "噪音",
            "visual_stimuli": "视觉刺激",
            "internal_thoughts": "内部思考",
            "hyperfocus_activities": "能够完全吸引您注意力的活动",
            "reading_patterns": "阅读模式",
            "reading_speed": "阅读速度",
            "slow": "慢",
            "average": "平均",
            "fast": "快",
            "difficult_text_features": "困难的文本特征（选择所有适用项）",
            "small_font": "小字体",
            "dense_text": "密集文本",
            "certain_fonts": "特定字体",
            "preferred_text_format": "首选文本格式",
            "font": "字体",
            "size": "大小",
            "spacing": "间距",
            "background": "背景颜色",
            "comprehension_aids": "对您有帮助的理解辅助工具",
            "learning_preferences": "学习偏好",
            "modality_preference": "模态偏好（从0到1评分）",
            "visual": "视觉",
            "auditory": "听觉",
            "kinesthetic": "动觉",
            "feedback_preference": "反馈偏好",
            "immediate": "即时",
            "delayed": "延迟",
            "group_vs_individual": "小组与个人学习",
            "group": "小组",
            "individual": "个人",
            "mixed": "混合",
            "technology_comfort": "对技术的适应度",
            "low": "低",
            "medium": "中",
            "high": "高",
            "previous_strategies": "以前的策略",
            "strategy_effectiveness": "评价您尝试过的策略的有效性",
            "task_breakdown": "任务分解",
            "pomodoro": "番茄工作法",
            "text_to_speech": "文本转语音",
            "concept_mapping": "概念映射",
            "effectiveness": "有效性",
            "not_effective": "无效",
            "slightly_effective": "略有效",
            "moderately_effective": "中等有效",
            "very_effective": "非常有效",
            "extremely_effective": "极其有效",
            "havent_tried": "未尝试",
            "notes": "备注（可选）",
            "previous": "上一步",
            "next": "下一步",
            "submit": "提交问卷"
        }
    },
    
    # Material upload page
    "material_upload": {
        "en": {
            "title": "Upload Learning Material",
            "subtitle": "Submit your learning material for personalized adaptations",
            "material_title": "Material Title",
            "material_text": "Material Text",
            "placeholder": "Paste or type your learning material here...",
            "submit": "Process Material",
            "back": "Back to My",
            "instructions": "Upload your learning material to receive a personalized version adapted to your learning profile. We support plain text and markdown formatting.",
            "file_upload": "Or upload a file",
            "supported_formats": "Supported formats: .txt, .md, .pdf",
            "max_size": "Maximum file size: 10MB",
            "processing_time": "Processing may take a few minutes depending on the size of your material.",
            
            # Tips Grid section
            "tips_title": "Tips for Best Results",
            "tip1_title": "Plain Text Format",
            "tip1_text": "For best results, submit plain text without complex formatting. Remove any special characters or formatting that might interfere with processing.",
            "tip2_title": "Maintain Structure",
            "tip2_text": "Keep paragraph breaks and section headings to help our system understand the structure of your content.",
            "tip3_title": "Optimal Length",
            "tip3_text": "For best performance, submit materials between 500-5000 words. Longer texts can be split into multiple submissions.",
            "tip4_title": "Language Support",
            "tip4_text": "Currently, our system works best with English-language content. Support for additional languages is coming soon."
        },
        "zh": {
            "title": "上传学习材料",
            "subtitle": "提交您的学习材料以获取个性化调整",
            "material_title": "材料标题",
            "material_text": "材料文本",
            "placeholder": "在此粘贴或输入您的学习材料...",
            "submit": "处理材料",
            "back": "返回仪表板",
            "instructions": "上传您的学习材料，以获取根据您的学习档案调整的个性化版本。我们支持纯文本和 Markdown 格式。",
            "file_upload": "或上传文件",
            "supported_formats": "支持的格式：.txt、.md、.pdf",
            "max_size": "最大文件大小：10MB",
            "processing_time": "处理时间可能需要几分钟，具体取决于您的材料大小。",
            
            # Tips Grid section
            "tips_title": "获得最佳结果的提示",
            "tip1_title": "纯文本格式",
            "tip1_text": "为获得最佳结果，请提交没有复杂格式的纯文本。删除可能干扰处理的任何特殊字符或格式。",
            "tip2_title": "保持结构",
            "tip2_text": "保留段落分隔和章节标题，以帮助我们的系统理解您内容的结构。",
            "tip3_title": "最佳长度",
            "tip3_text": "为获得最佳性能，请提交 500-5000 字之间的材料。较长的文本可以分成多次提交。",
            "tip4_title": "语言支持",
            "tip4_text": "目前，我们的系统最适合英语内容。对其他语言的支持即将推出。"
        }
    },
    
    # Learning view page
    "learning_view": {
        "en": {
            "title": "Learning View",
            "original": "Original",
            "adapted": "Adapted",
            "notes": "Notes",
            "timer": "Timer",
            "start": "Start",
            "pause": "Pause",
            "stop": "Stop",
            "reset": "Reset",
            "save_notes": "Save Notes",
            "back": "Back to My"
        },
        "zh": {
            "title": "学习视图",
            "original": "原始",
            "adapted": "已调整",
            "notes": "笔记",
            "timer": "计时器",
            "start": "开始",
            "pause": "暂停",
            "stop": "停止",
            "reset": "重置",
            "save_notes": "保存笔记",
            "back": "返回仪表板"
        }
    },
    
    # Materials history page
    "materials_history": {
        "en": {
            "title": "Your Learning Materials",
            "subtitle": "Access your previously processed learning materials",
            "no_materials": "You haven't processed any learning materials yet.",
            "upload_new": "Upload New Material",
            "back": "Back to My",
            "material_title": "Title",
            "processed_date": "Processed Date",
            "view": "View"
        },
        "zh": {
            "title": "您的学习材料",
            "subtitle": "访问您之前处理过的学习材料",
            "no_materials": "您尚未处理任何学习材料。",
            "upload_new": "上传新材料",
            "back": "返回仪表板",
            "material_title": "标题",
            "processed_date": "处理日期",
            "view": "查看"
        }
    }
}

def get_translation(section, key, language="en"):
    """
    Get a translation for a specific key in a section.
    
    Args:
        section: The section of the application (e.g., 'dashboard', 'base')
        key: The specific key to translate
        language: The language to translate to (default: 'en')
        
    Returns:
        The translated string, or the key itself if no translation is found
    """
    if language not in ["en", "zh"]:
        language = "en"
        
    if section in translations and language in translations[section] and key in translations[section][language]:
        return translations[section][language][key]
    
    # Fallback to English if the key doesn't exist in the specified language
    if section in translations and "en" in translations[section] and key in translations[section]["en"]:
        return translations[section]["en"][key]
    
    # Return the key itself if no translation is found
    return key 