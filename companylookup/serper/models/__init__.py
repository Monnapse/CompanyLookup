from typing import List, Optional, Dict
from pydantic import BaseModel
import tldextract

class SearchParameters(BaseModel):
    q: str
    type: str
    engine: str

class KnowledgeGraph(BaseModel):
    title: Optional[str] = None
    imageUrl: Optional[str] = None
    description: Optional[str] = None
    descriptionSource: Optional[str] = None
    descriptionLink: Optional[str] = None
    attributes: Dict[str, str]

class SiteLink(BaseModel):
    title: str
    link: str

class OrganicResult(BaseModel):
    """
        Represents an organic search result from Serper.

        IF YOUR RESULTS SHOULD HAVE VALUES THAT ARENT HERE THEEN ADD NEW TYPES HERE
    """

    # Common fields
    title: str
    link: str
    snippet: Optional[str] = None
    sitelinks: Optional[List[SiteLink]] = None
    position: Optional[int] = None
    date: Optional[str] = None
    currency: Optional[str] = None
    price: Optional[float] = None

    # Computed field
    baseLink: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)

        if self.link and not self.baseLink:
            self.baseLink = tldextract.extract(self.link).registered_domain  # Extract base link without subdomain from full URL (https://metrolinedirect.tenereteam.com/coupons -> tenereteam.com)
            #print(f"Computed baseLink: {self.baseLink} from link: {self.link}")

class PeopleAlsoAskItem(BaseModel):
    question: str
    snippet: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None

class RelatedSearch(BaseModel):
    query: str

class SearchResponse(BaseModel):
    searchParameters: SearchParameters
    knowledgeGraph: Optional[KnowledgeGraph] = None
    organic: List[OrganicResult]
    peopleAlsoAsk: Optional[List[PeopleAlsoAskItem]] = None
    relatedSearches: Optional[List[RelatedSearch]] = None
    credits: int