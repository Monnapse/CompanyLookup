from pydantic import BaseModel

class Company(BaseModel):
    name: str
    website: str
    description: str
    phones: list[str]
    emails: list[str]

class CompanyAnalysis(BaseModel):
    score: float
    url: str
    company: str

class AnalyzeQuery(BaseModel):
    lambda_function: lambda: float