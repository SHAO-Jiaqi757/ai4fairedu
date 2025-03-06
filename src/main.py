from typing import Dict, Any
import argparse
import logging
from src.architecture import build_support_system
from src.config import SystemConfig
from src.user_profile import analyze_user_profile
from src.adhd_support import build_adhd_support_graph
from src.dyslexia_support import build_dyslexia_support_graph
import json
import os
from datetime import datetime

def setup_logging(config: SystemConfig) -> None:
    """配置日志系统"""
    logging.basicConfig(
        level=getattr(logging, config.get("logging.level")),
        filename=config.get("logging.file"),
        format=config.get("logging.format")
    )

def load_user_profile(profile_path: str = None) -> Dict:
    """加载用户配置文件"""
    if not profile_path:
        return {}
    
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"加载用户配置文件失败: {e}")
        return {}

def load_learning_materials(material_path: str = None) -> Dict:
    """加载学习材料"""
    if not material_path:
        return {}
    
    try:
        with open(material_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取文件名作为标题
        title = os.path.basename(material_path)
        if '.' in title:
            title = title.rsplit('.', 1)[0]
        
        # 估计阅读时间（简单估计：平均阅读速度200词/分钟）
        word_count = len(content.split())
        estimated_reading_time = max(1, round(word_count / 200))
        
        return {
            "current_content": content,
            "title": title,
            "type": "text",
            "word_count": word_count,
            "estimated_reading_time_minutes": estimated_reading_time,
            "source_path": material_path
        }
    except Exception as e:
        logging.error(f"加载学习材料失败: {e}")
        return {}

def save_results(state: Dict, results_path: str) -> None:
    """保存处理结果"""
    if not results_path:
        logging.warning("未指定结果保存路径，结果将不会被保存")
        return
    
    try:
        # 确保目录存在
        os.makedirs(results_path, exist_ok=True)
        
        # 生成结果文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(results_path, f"result_{timestamp}.json")
        
        # 保存结果
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            
        # 同时保存一个latest_result.json
        latest_file = os.path.join(results_path, "latest_result.json")
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            
        logging.info(f"结果已保存至 {result_file}")
    except Exception as e:
        logging.error(f"保存结果失败: {e}")

def main():
    """系统主入口点"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="学习障碍支持系统")
    parser.add_argument("--config", type=str, help="配置文件路径")
    parser.add_argument("--difficulty-type", type=str, help="学习困难类型 (adhd, dyslexia, combined)")
    parser.add_argument("--material", type=str, help="学习材料路径")
    parser.add_argument("--user-profile", type=str, help="用户配置文件路径")
    args = parser.parse_args()
    
    # 加载配置
    config = SystemConfig()
    if args.config:
        config.load_file(args.config)
    
    # 设置日志
    setup_logging(config)
    logging.info("系统启动")
    
    # 构建主支持系统
    support_system = build_support_system()
    
    # 初始化状态
    initial_state = {
        "user_profile": load_user_profile(args.user_profile) if args.user_profile else {},
        "learning_materials": load_learning_materials(args.material) if args.material else {},
        "processed_content": {},
        "interaction_history": [],
        "current_focus": "start",
        "next_steps": [],
        "metadata": {"config": config.config},
        "iteration_count": 0  # 添加迭代计数器
    }
    
    # 运行系统
    final_state = support_system.invoke(initial_state, config={"recursion_limit": 20})
    
    # 保存结果
    save_results(final_state, config.get("storage.results_path"))
    
    logging.info("处理完成")

if __name__ == "__main__":
    main() 