import requests
from .utils.api_client import DeepSeekClient

class ResearchAgent:
    def __init__(self):
        self.client = DeepSeekClient()
    
    def generate_research(self, topic):
        response = self.client.chat_completion(
            messages=[...],
            model="deepseek-chat"
        )