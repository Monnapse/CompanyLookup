# CompanyLookup
Lookup companies

### [Example Code Link](https://github.com/Monnapse/CompanyLookup/blob/main/__main__.py)
```python
from companylookup import CompanyLookup, LookupMethod

company_lookup = CompanyLookup(api_key="SERPER_API_KEY")

company_result = company_lookup.lookup(
   company_name="Momentum Telecom",
   lookup_method=LookupMethod.ENHANCED,
   description="Momentum Telecom is a global provider of cloud voice, managed network, and unified communications solutions for business."
)

print("Company Lookup Result:")
print(f"Company Name: {company_result.analysis.company}")
print(f"Company URL: {company_result.analysis.url}")
print(f"Analysis Score: {company_result.analysis.score * 100:.2f}%")
print(f"Company Details: {company_result.company}")
print(f"Original Search Result: {company_result.result}")
```