from typing import Tuple
from .serper.types import OrganicResult
from .types import CompanyAnalysis, Company
import re

HIGH_PRIORITY = 1.0
MEDIUM_PRIORITY = 0.35
LOW_PRIORITY = 0.1
#PARTIAL_PRIORITY = 0.35

def analyze_in_order(x: any, ops: list[callable], log: bool = False) -> float:
    """
        Analyze using a list of operations in order, returning the first non-None result.
    """

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

def analyze_title_match(company_name: str, title: str, target_keywords: list[str]) -> float:
    """
        Analyze the title of a search result and return a score.
    """

    if not title: return 0.0
    return analyze_in_order(title, [
        lambda x: HIGH_PRIORITY if company_name.lower() in x.lower() else 0.0, # Exact match (HIGH PRIORITY)
        lambda x: MEDIUM_PRIORITY if ''.join([word[0] for word in company_name.split() if word]).lower() in x.lower() else 0.0, # Initials match
        lambda x: LOW_PRIORITY if len(set(company_name.lower().split()).intersection(set(x.lower().split()))) >= len(company_name.split()) / 2 else 0.0, # Partial match
        lambda x: HIGH_PRIORITY if any(keyword in x.lower() for keyword in target_keywords) else 0.0, # Target keywords present
    ])

def analyze_snippet_keywords(company_name: str, snippet: str, target_keywords: list[str]) -> float:
    """
        Analyze the keywords in a snippet and return a score.
    """

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
        lambda x: min(1.0, sum(1 for keyword in keywords if keyword in x.lower()) / len(keywords)), # Proportion of keywords present
        lambda x: HIGH_PRIORITY if any(keyword in x.lower() for keyword in target_keywords) else 0.0, # Target keywords present
    ])

def analyze_url_official(company_name: str, url: str, target_keywords: list[str]) -> float:
    """
        Analyze the URL of a search result and return a score.
    """

    if not url: return 0.0
    return analyze_in_order(url, [
        lambda x: HIGH_PRIORITY if company_name.replace(" ", "").lower() in x.lower() else 0.0, # Company name in URL
        lambda x: MEDIUM_PRIORITY if any(x.lower().endswith(ext) for ext in [".com", ".org", ".net", ".gov", ".edu"]) else 0.0, # Common official extensions
        lambda x: LOW_PRIORITY if len(x) < 50 else 0.0, # URL length check
        lambda x: HIGH_PRIORITY if any(keyword in x.lower() for keyword in target_keywords) else 0.0, # Target keywords present
    ], log=False)

def analyze_sitelinks(company_name: str, sitelinks: list[str]) -> float:
    """
        Analyze the sitelinks of a search result and return a score.
    """

    if not sitelinks: return 0.0
    return analyze_in_order(sitelinks, [
        lambda x: LOW_PRIORITY if company_name.replace(" ", "").lower() in x.lower() else 0.0, # Company name in sitelink list
        lambda x: LOW_PRIORITY if any(x.lower().endswith(ext) for ext in [".com", ".org", ".net", ".gov", ".edu"]) else 0.0, # Common official extensions
    ])

def analyze_price_currency(price: float, currency: str) -> float:
    """
        Analyze the price and currency of a search result and return a score.
    """

    if not price or not currency: return 0.0
    return analyze_in_order((price, currency), [
        lambda x: LOW_PRIORITY if x[1] in ["USD", "EUR", "GBP"] else 0.0, # Common currencies
        lambda x: LOW_PRIORITY if x[0] > 0 else 0.0 # Positive price check
    ])

def analyze_position(position: int) -> float:
    """
        Analyze the position of a search result and return a score.
    """

    return max(0.0, 1.0 - (position - 1) * MEDIUM_PRIORITY)  # Decrease score by PARTIAL_PRIORITY for each position down

def analyze_company(company_name: str, target_keywords: list[str], result: OrganicResult) -> CompanyAnalysis:
    """
        Analyze a single organic search result and return a company analysis.
    """

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
        lambda x: analyze_title_match(company_name, x.title, target_keywords),
        lambda x: analyze_snippet_keywords(company_name, x.snippet, target_keywords),
        lambda x: analyze_url_official(company_name, x.baseLink if x.baseLink else x.link, target_keywords),
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

def analyze_company_list(company_name: str, target_keywords: list[str], organic_results: list[OrganicResult]) -> Tuple[CompanyAnalysis, OrganicResult]:
    """
        Analyze a list of organic search results and return the highest scoring company analysis and its corresponding result.

        Args:
            company_name (str): The name of the company to analyze against.
            target_keywords (list[str]): A list of target keywords to look for in the analysis. (Ex: "contact", "support", etc.)
            organic_results (list[OrganicResult]): A list of organic search results to analyze.
            
    """

    highest: CompanyAnalysis = None
    highest_result = None
    for result in organic_results:  
        analysis = analyze_company(company_name, target_keywords, result)
        #print(f"Result Analysis: {analysis}")
        if analysis and (highest is None or analysis.score > highest.score):
            highest = analysis
            highest_result = result

    return highest, highest_result

def analyze_company_snippet(
        company_name: str | None, 
        description: str | None,
        website: str | None,
        snippet: str
    ) -> Company:
    """
        Analyze a company snippet and return a Company object.
    """
    #name: str
    #website: str
    #description: str
    #phones: list[str]
    #emails: list[str]


    phones = re.findall(
        r'\b(?:\+?1[\s.-]?)?(?:\(?(\d{3})\)?[\s.-]?)(\d{3})[\s.-]?(\d{4})(?:\s*(?:x|ext\.?|extension)\s*(\d+))?\b',
        snippet,
        flags=re.IGNORECASE
    )
    formatted_phones = []
    for area, first3, last4, ext in phones:
        phone = f"({area}) {first3}-{last4}"
        if ext:
            phone += f" x{ext}"
        formatted_phones.append(phone)

    emails = re.findall(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*(?=\b)',
        snippet
    )

    company = Company(
        name=company_name,
        website=website,
        description=description,
        snippet=snippet,
        phones=formatted_phones,
        emails=emails
    )

    return company