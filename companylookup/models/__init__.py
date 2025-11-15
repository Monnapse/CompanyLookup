from pydantic import BaseModel
from ..serper.models import OrganicResult

class Company(BaseModel):
    name: str | None
    website: str | None
    overview: str | None
    snippet: str | None
    phones: set[str] | None
    emails: set[str] | None

class CompanyAnalysis(BaseModel):
    score: float
    url: str
    company: str

#class AnalyzeQuery(BaseModel):
#    lambda_function: lambda: float

class CompanyAnalysisComplete(BaseModel):
    analysis: CompanyAnalysis | None
    company: Company | None
    result: OrganicResult | None