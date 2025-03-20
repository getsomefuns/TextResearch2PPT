from src.utils.api_client import DeepSeekClient

def market_analysis():
    client = DeepSeekClient()
    query = (
        "我需要了解可穿戴式智能设备的市场情况,包括:\n"
        "1. 当前市场需求\n"
        "2. 头部企业名单\n"
        "3. 未来可能爆发式增长的产品类型\n"
        "4. 相关技术瓶颈分析"
    )
    response = client.chat_completion(
        messages=[{"role": "user", "content": query}]
    )
    print("=== 分析结果 ===")
    print(response)

if __name__ == "__main__":
    market_analysis()