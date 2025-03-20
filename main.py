# main.py 顶部添加
import sys
import os

# 确保项目根目录加入系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 在导入任何自定义模块前加载环境变量
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
from dotenv import load_dotenv
load_dotenv() 
from src.utils.api_client import DeepSeekClient
import argparse
import json
from src.research_agent import ResearchAgent
from src.mindmap_engine import MindmapGenerator
from src.ppt_builder import PPTBuilder
from src.utils.file_loader import EditableFileManager
from src.utils.config_manager import PipelineController

def main():
    parser = argparse.ArgumentParser(description='智能研究报告生成器')
    parser.add_argument('--input', required=True, help='研究主题')
    parser.add_argument('--stop-at', choices=['text', 'mindmap', 'ppt'], 
                       help='停止阶段')
    parser.add_argument('--force', action='store_true', 
                       help='强制重新生成所有内容')
    args = parser.parse_args()

    controller = PipelineController()
    
    # 执行文本生成
    if args.force or controller.need_generate('text'):
        agent = ResearchAgent()
        research_data = agent.generate_research(args.input)
        with open('intermediate/research_output.json', 'w') as f:
            json.dump(research_data, f, ensure_ascii=False, indent=2)
    
    # 执行思维导图生成
    if not args.stop_at or args.stop_at == 'mindmap':
        if EditableFileManager().check_modified('intermediate/research_output.json'):
            generator = MindmapGenerator()
            generator.generate_from_json(research_data, 'intermediate/mindmap.mmd')
    
    # 执行PPT生成
    if not args.stop_at or args.stop_at == 'ppt':
        builder = PPTBuilder()
        builder.build_from_mindmap(research_data)

if __name__ == "__main__":
    main()