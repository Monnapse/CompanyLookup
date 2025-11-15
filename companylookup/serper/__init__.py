import requests
import json

from .types import (
    SearchResponse,
    SearchParameters,
    KnowledgeGraph,
    OrganicResult,
    PeopleAlsoAskItem,
    RelatedSearch,
    SiteLink,
)

class SerperClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"

    def search(
            self, 
            query: str,
            country: str | None = None,
            location: str | None = None,
            language: str | None = None,
            date_range: str | None = None,
            page: int | None = None,
        ) -> SearchResponse:
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "gl": country,
            "location": location,
            "hl": language,
            "tbs": date_range,
            "page": page
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return SearchResponse(**response.json())