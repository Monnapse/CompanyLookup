from .serper import SerperClient

class CompanyLookup:
    def __init__(self, api_key: str = None):
        self.serper_client = SerperClient(api_key=api_key)

    def lookup(self, company_name: str):
        response = self.serper_client.search(query=f'"{company_name}" official site')

        


        #return response