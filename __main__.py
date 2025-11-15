"""
    Testing module
"""

from companylookup.analyze import analyze_company_snippet
#from companylookup.serper.types import OrganicResult

from companylookup import CompanyLookup, LookupType
from dotenv import load_dotenv
import os
load_dotenv()

company_lookup = CompanyLookup(api_key=os.getenv("SERPER_API_KEY"))

if __name__ == "__main__":
  print("This is a test module.")

  #company = analyze_company_snippet(
  #    company_name="MetrolineDirect",
  #    snippet="MetrolineDirect's phone number is (801) 555-8776 801-555-5735 801 555 3467 801.555.1212 test@example.com john.doe@sub.domain.net sales@company.co.uk info@mail.server.example.org user+tag@domain.com What is the MetrolineDirect's official website? MetrolineDirect's official website is metrolinedirect.com email: help@metrolinedirect.com ...",
  #    description="MetrolineDirect specializes in telecom products and services.",
  #    website="https://www.metrolinedirect.com"
  #)
#
  #print(company)

  #"""
    
  #  organic_raw = [
  #  {
  #    "title": "Mitel Integrated DECT Headset for 6900 Series (51305332)",
  #    "link": "https://www.metrolinedirect.com/mitel-integrated-dect-headset-for-6900-series.html?srsltid=AfmBOoqMvZT-iTlik4xUeltW0iFU1hbEb2H5GfwfGlBHQgaXD3ubRe6b",
  #    "snippet": "It features secure DECT wireless technology, up to 8 hours talk time, excellent range, and integrated call controls on the headset.",
  #    "currency": "$",
  #    "price": 118.95,
  #    "position": 1
  #  },
  #  {
  #    "title": "MetrolineDirect - Phone Number & Corp Office",
  #    "link": "https://seamless.ai/b/metrolinedirect-15204180",
  #    "snippet": "MetrolineDirect's phone number is 248.655.1463. What is the MetrolineDirect's official website? MetrolineDirect's official website is metrolinedirect.com ...",
  #    "position": 2
  #  },
  #  {
  #    "title": "Metroline - Overview, News & Similar companies",
  #    "link": "https://www.zoominfo.com/c/metroline-inc/343390622",
  #    "snippet": "Metroline's official website is www.metrolinedirect.com What is Metroline's Revenue? ... Metroline contact info: Phone number: (800) 929-8061 Website: www.",
  #    "position": 3
  #  },
  #  {
  #    "title": "70% OFF MetrolineDirect Coupon Codes - November 2025 ...",
  #    "link": "https://metrolinedirect.tenereteam.com/coupons",
  #    "snippet": "MetrolineDirect specializes in telecom products and services. It offers a wide range of IP phones, wireless headsets, and conference units.",
  #    "date": "Nov 4, 2025",
  #    "position": 4
  #  },
  #  {
  #    "title": "MetrolineDirect – Cybersecurity Risk Score & Incident History",
  #    "link": "https://www.rankiteo.com/company/metrolinedirect",
  #    "snippet": "Official Website of MetrolineDirect. The official website of MetrolineDirect is https://www.metrolinedirect.com. MetrolineDirect's AI-Generated Cybersecurity ...",
  #    "position": 5
  #  },
  #  {
  #    "title": "25% Off MetrolineDirect Promo Code, Coupons Nov 2025",
  #    "link": "https://metrolinedirect1.knoji.com/promo-codes/",
  #    "snippet": "MetrolineDirect promo codes, coupons & deals, November 2025. Save BIG w/ (15) MetrolineDirect verified coupon codes & storewide coupon codes.",
  #    "position": 6
  #  },
  #  {
  #    "title": "Metroline vs. Distribution",
  #    "link": "https://www.tek-tips.com/threads/metroline-vs-distribution.1764900/",
  #    "snippet": "We currently buy all of our Avaya products from distribution, Westcon, Synnex,..., how can Metrolinedirect blow the doors off the pricing we can ...",
  #    "date": "Apr 26, 2016",
  #    "position": 7
  #  },
  #  {
  #    "title": "How to set admin password on poly phone - start up screen ...",
  #    "link": "https://www.tiktok.com/@metrolinedirect/video/7163785053028240683",
  #    "snippet": "Press the down arrow button enter your new password and then press the down arrow button again enter your new password again to confirm.",
  #    "date": "3 years ago",
  #    "position": 8
  #  },
  #  {
  #    "title": "WMR Presents \"The Majors at Grattan\" Official Qualifying ...",
  #    "link": "https://cdn.connectsites.net/user_files/scca/downloads/000/017/008/Grp3QualSat.pdf?1471109293",
  #    "snippet": "metrolinedirect.com. GY/R-line DJRace/West MI Imports. KoteQuip LLC. Hoosier/Red Line Oil/Six Shooter Coffee/Sti. Wounded Turtle Racing. Laps. 11. 10. 10. 12.",
  #    "position": 9
  #  }
  #]

    #organic = [OrganicResult(**item) for item in organic_raw]

    #analysis = analyze_company_list("MetrolineDirect", organic)
    #print(analysis)
    #print(f"Best match: {analysis.company} with score {analysis.score * 100:.2f}% at {analysis.url}")

  company_result = company_lookup.lookup(
    company_name="Momentum Telecom",
    lookup_type=LookupType.ENHANCED,
    description="MetrolineDirect specializes in telecom products and services."
  )
  # "POPP Communications" official site contact "contact" OR "support" OR "@gmail.com" OR "phone" OR "call" OR "call us" OR "email"
  # "POPP Communications" official site contact "contact" OR "support" OR "@gmail.com" OR "phone" OR "call" OR "call us" OR "email"

  print("Company Lookup Result:")
  print(f"Company Name: {company_result.analysis.company}")
  print(f"Company URL: {company_result.analysis.url}")
  print(f"Analysis Score: {company_result.analysis.score * 100:.2f}%")
  print(f"Company Details: {company_result.company}")
  print(f"Original Search Result: {company_result.result}")
  #print("End of Test Module.")

  
  #"""