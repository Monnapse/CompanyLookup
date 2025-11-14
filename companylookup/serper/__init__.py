import requests
import json

class SerperClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str) -> dict:
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()