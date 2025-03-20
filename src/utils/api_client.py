import os
import yaml
import requests
import json
from typing import Optional, List, Dict
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '../../.env')  # 动态计算路径
load_dotenv(env_path, override=True)

class DeepSeekClient:
    """DeepSeek API 客户端封装类"""
    
    def __init__(self):
        """
        初始化API客户端
        从环境变量加载API密钥并验证配置文件
        """
        # 加载环境变量
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.endpoints = None

        # 验证API密钥格式
        if not self.api_key:
            raise ValueError("❌ 错误：请先设置 DEEPSEEK_API_KEY 环境变量")
        if not self.api_key.startswith("sk-"):
            raise ValueError("❌ 错误：API密钥格式无效，应以 sk- 开头")

        # 加载API端点配置
        try:
            config_path = os.path.join(os.path.dirname(__file__), '../../config/paths.yaml')
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.endpoints = config['api_endpoints']
        except FileNotFoundError:
            raise RuntimeError("⚠️ 配置文件 config/paths.yaml 未找到")
        except KeyError:
            raise RuntimeError("⚠️ 配置文件中缺少 api_endpoints 字段")
        except Exception as e:
            raise RuntimeError(f"⚠️ 配置文件加载失败: {str(e)}")

        # 调试输出
        print(f"✅ API客户端初始化成功 | 端点: {self.endpoints['chat']}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.3
    ) -> Optional[str]:
        """
        调用DeepSeek聊天补全API
        
        :param messages: 消息列表，格式示例：
            [{"role": "user", "content": "你好"}]
        :param model: 使用的模型名称
        :param temperature: 生成文本的随机性控制（0-1）
        :return: 模型生成的文本内容，失败时返回None
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        try:
            # 调试请求信息
            print(f"🚀 发送请求到: {self.endpoints['chat']}")
            print(f"📦 请求参数: {json.dumps(payload, indent=2, ensure_ascii=False)}")

            response = requests.post(
                self.endpoints['chat'],
                headers=headers,
                json=payload,
                timeout=15  # 增加超时时间
            )
            response.raise_for_status()  # 自动处理4xx/5xx错误

            # 解析响应
            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.HTTPError as e:
            print(f"🔴 HTTP错误 ({e.response.status_code}): {e.response.text}")
        except requests.exceptions.Timeout:
            print("⏱️ 请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            print("📡 网络连接错误，请检查网络设置")
        except KeyError:
            print("🔍 响应格式异常，无法解析结果")
        except Exception as e:
            print(f"⚠️ 未处理的异常: {str(e)}")
        
        return None

# 简易测试方法（可直接运行测试）
if __name__ == "__main__":
    print("=== API客户端测试 ===")
    try:
        client = DeepSeekClient()
        test_response = client.chat_completion(
            messages=[{"role": "user", "content": "你好，请说'测试成功'"}]
        )
        print(f"测试结果: {test_response}")
    except Exception as e:
        print(f"测试失败: {str(e)}")