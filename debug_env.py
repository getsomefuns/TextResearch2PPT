import os
from dotenv import load_dotenv

def debug_env():
    # 打印系统级环境变量
    print("\n=== 系统环境变量 ===")
    print(f"PATH: {os.getenv('PATH', '未设置')[:100]}...")
    
    # 强制加载项目.env
    env_path = '/Users/a1234/Documents/TextResearch2PPT/.env'
    load_dotenv(env_path)
    
    # 打印项目环境变量
    print("\n=== 项目环境变量 ===")
    print(f"当前工作目录: {os.getcwd()}")
    print(f".env文件存在: {os.path.exists(env_path)}")
    print(f"DEEPSEEK_API_KEY: {os.getenv('DEEPSEEK_API_KEY', '未设置')}")

if __name__ == "__main__":
    debug_env()