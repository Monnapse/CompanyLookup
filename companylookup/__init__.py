from .serper import SerperClient
from .models.enums import LookupMethod
from .models import CompanyAnalysisComplete, Company, CompanyAnalysis, OrganicResult
from companylookup.analyze import analyze_company_list, analyze_company_snippet
from typing import Tuple

class CompanyLookup:
    def __init__(self, api_key: str = None):
        self.serper_client = SerperClient(api_key=api_key)

        self.target_keywords = ["contact", "support", "@gmail.com", "phone", "call", "email"]

    def simple_lookup(self, company_name: str) -> Tuple[CompanyAnalysis, OrganicResult]:
        """
            Perform a simple company lookup.
        """
        # SIMPLE QUERY WORK IN PROGRESS
        # Faster, uses less resources, but less accurate.
        # QUERY 1: "Virtual Technologies Group LLC" official site contact "contact" OR "support" OR "@gmail.com" OR "phone" OR "call" OR "email"
        # Find official site
        # Use result

        query = f'"{company_name}" official site contact "contact" OR "support" OR "@gmail.com" OR "phone" OR "call" OR "call us" OR "email"'
        #print(f"Simple lookup query: {query}")
        results = self.serper_client.search(query=query)
        #print(f"Simple lookup results for '{company_name}': {len(results.organic)} organic results found.")

        highest_analysis, highest_result = analyze_company_list(company_name, self.target_keywords, results.organic)

        return highest_analysis, highest_result

    def enhanced_lookup(self, company_name: str) -> Tuple[CompanyAnalysis, OrganicResult]:
        """
            Perform an enhanced company lookup.
        """
        # ENHANCED QUERY WORK IN PROGRESS
        # Slower, uses more resources, but more accurate.
        # QUERY 1: "Virtual Technologies Group LLC" official site
        # Find official site
        # QUERY 2: site:popp.com "contact" OR "support" OR "@gmail.com" OR "phone" OR "call" OR "email" OR "@popp.com"
        # Use results

        query = f'"{company_name}" official site'
        #print(f"Enhanced lookup query: {query}")
        results = self.serper_client.search(query=query)
        #print(f"Enhanced lookup results for '{company_name}': {len(results.organic)} organic results found.")
        highest_analysis, highest_result = analyze_company_list(company_name, self.target_keywords, results.organic)
        
        query2 = f'site:{highest_result.baseLink if highest_result.baseLink else highest_result.link} "contact" OR "support" OR "@gmail.com" OR "phone" OR "call" OR "call us" OR "email" OR "@{highest_result.baseLink}"'
        #print(f"Enhanced lookup second query: {query2}")
        results2 = self.serper_client.search(query=query2)
        #print(f"Enhanced lookup second results for '{company_name}': {len(results2.organic)} organic results found.")
        highest_analysis2, highest_result2 = analyze_company_list(company_name, self.target_keywords, results2.organic)

        return highest_analysis2, highest_result2

    def lookup(
            self, 
            company_name: str, 
            lookup_method: LookupMethod = LookupMethod.SIMPLE,
            description: str | None = None,
        ) -> CompanyAnalysisComplete:
        """
            Perform a company lookup based on the specified lookup type.

            Args:
                company_name (str): The name of the company to look up.
                lookup_type (LookupType): The type of lookup to perform (SIMPLE or ENHANCED).
        """

        # Checks
        if not company_name:
            raise ValueError("Company name must be provided for lookup.")
        if not lookup_method:
            raise ValueError("Lookup method must be specified.")

        # Perform lookup based on type
        highest_analysis: CompanyAnalysis = None
        highest_result: OrganicResult = None
        if lookup_method == LookupMethod.SIMPLE:
            # SIMPLE LOOKUP LOGIC
            highest_analysis, highest_result = self.simple_lookup(company_name)
        elif lookup_method == LookupMethod.ENHANCED:
            # ENHANCED LOOKUP LOGIC
            highest_analysis, highest_result = self.enhanced_lookup(company_name)

        # Construct company details if we have a valid result
        if not highest_result: 
            raise ValueError("No valid company result found during lookup.")
            return None
        
        company_details = analyze_company_snippet(
            company_name=highest_result.title,
            description=description,
            website=highest_result.baseLink,
            snippet=highest_result.snippet
        )

        #return response
        return CompanyAnalysisComplete(
            analysis=highest_analysis,
            company=company_details,
            result=highest_result
        )