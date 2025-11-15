from .serper.types import OrganicResult
from .types import CompanyAnalysis
import re

HIGH_PRIORITY = 1.0
MEDIUM_PRIORITY = 0.35
LOW_PRIORITY = 0.1
#PARTIAL_PRIORITY = 0.35

def analyze_in_order(x: any, ops: list[callable], log: bool = False) -> float:
    score = 0.0
    total_checks = 0

    for func in ops:
        result = func(x)
        if result is not None:
            if log:
                print(f"{func.__name__}  - Check result: {result}")
            score += result
            total_checks += 1

    return score / total_checks if total_checks > 0 else 0.0

def analyze_title_match(company_name: str, title: str) -> float:
    if not title: return 0.0
    return analyze_in_order(title, [
        lambda x: HIGH_PRIORITY if company_name.lower() in x.lower() else 0.0, # Exact match (HIGH PRIORITY)
        lambda x: MEDIUM_PRIORITY if ''.join([word[0] for word in company_name.split() if word]).lower() in x.lower() else 0.0, # Initials match
        lambda x: LOW_PRIORITY if len(set(company_name.lower().split()).intersection(set(x.lower().split()))) >= len(company_name.split()) / 2 else 0.0, # Partial match
    ])

def analyze_snippet_keywords(company_name: str, snippet: str) -> float:
    if not snippet: return 0.0
    # Add space to camel case words
    camel_case_words = re.findall(r'[A-Z][a-z]*', company_name)
    if camel_case_words:
        company_name = ' '.join(camel_case_words)
    #print(f"Analyzing snippet for company name: {company_name}")
    keywords = company_name.lower().split()
    
    return analyze_in_order(snippet, [
        lambda x: HIGH_PRIORITY if all(keyword in x.lower() for keyword in keywords) else 0.0, # All keywords present
        lambda x: MEDIUM_PRIORITY if any(keyword in x.lower() for keyword in keywords) else 0.0, # Any keyword present
        lambda x: min(1.0, sum(1 for keyword in keywords if keyword in x.lower()) / len(keywords)) # Proportion of keywords present
    ])

def analyze_url_official(company_name: str, url: str) -> float:
    if not url: return 0.0
    return analyze_in_order(url, [
        lambda x: HIGH_PRIORITY if company_name.replace(" ", "").lower() in x.lower() else 0.0, # Company name in URL
        lambda x: MEDIUM_PRIORITY if any(x.lower().endswith(ext) for ext in [".com", ".org", ".net", ".gov", ".edu"]) else 0.0, # Common official extensions
        lambda x: LOW_PRIORITY if len(x) < 50 else 0.0 # URL length check
    ], log=False)

def analyze_sitelinks(company_name: str, sitelinks: list[str]) -> float:
    if not sitelinks: return 0.0
    return analyze_in_order(sitelinks, [
        lambda x: LOW_PRIORITY if company_name.replace(" ", "").lower() in x.lower() else 0.0, # Company name in sitelink list
        lambda x: LOW_PRIORITY if any(x.lower().endswith(ext) for ext in [".com", ".org", ".net", ".gov", ".edu"]) else 0.0, # Common official extensions
    ])

def analyze_price_currency(price: float, currency: str) -> float:
    if not price or not currency: return 0.0
    return analyze_in_order((price, currency), [
        lambda x: LOW_PRIORITY if x[1] in ["USD", "EUR", "GBP"] else 0.0, # Common currencies
        lambda x: LOW_PRIORITY if x[0] > 0 else 0.0 # Positive price check
    ])

def analyze_position(position: int) -> float:
    return max(0.0, 1.0 - (position - 1) * MEDIUM_PRIORITY)  # Decrease score by PARTIAL_PRIORITY for each position down

def analyze_company(company_name: str, result: OrganicResult) -> CompanyAnalysis:
    # Checks
    # 1: Check how close the company name is to the title
    # 2: Check the snippet for company related keywords
    # 3: Check if the URL looks like an official site (e.g., contains the company name, length, extension, etc.)
    # 4: Check for sitelinks that indicate an official site
    # 5: Check the position in search results

    # baseLink
    #print(f"Analyzing result: {result.title} - {result.link} - baseLink: {result.baseLink}")

    #print(f"Analysis for {result.link}:")
    score = analyze_in_order(result, [
        lambda x: analyze_title_match(company_name, x.title),
        lambda x: analyze_snippet_keywords(company_name, x.snippet),
        lambda x: analyze_url_official(company_name, x.baseLink if x.baseLink else x.link),
        lambda x: analyze_sitelinks(company_name, x.sitelinks),
        lambda x: analyze_position(x.position) if x.position else 0.0,
        lambda x: analyze_price_currency(x.price, x.currency) if x.price and x.currency else 0.0
    ])

    analysis = CompanyAnalysis(
        score=score,
        url=result.link,
        company=result.title
    )

    #print(analysis)

    return analysis

def analyze_company_list(company_name: str, organic_results: list[OrganicResult]) -> dict:
    highest: CompanyAnalysis = None
    for result in organic_results:  
        analysis = analyze_company(company_name, result)
        print(f"Result Analysis: {analysis}")
        if analysis and (highest is None or analysis.score > highest.score):
            highest = analysis

    return highest
