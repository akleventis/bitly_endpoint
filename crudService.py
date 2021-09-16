import requests

class CrudService:

    def __init__(self, headers):
        self.headers = headers

    def getGroup(self, group_guid):
        try:
            response = requests.get(f'https://api-ssl.bitly.com/v4/groups/{group_guid}', headers=self.headers).json()
        except requests.exceptions.RequestException as e:
            raise(SystemExit(e))
        return response

    def getUser(self):
        try:
            response = requests.get(f'https://api-ssl.bitly.com/v4/user', headers=self.headers).json()
        except requests.exceptions.RequestException as e:
            raise(SystemExit(e))
        return response
    

    def getLinks(self, group_guid):
        try:
            response = requests.get(f'https://api-ssl.bitly.com/v4/groups/{group_guid}/bitlinks', headers=self.headers).json()
        except requests.exceptions.RequestException as e:
            raise(SystemExit(e))
        return response


    def getClicksByCountry(self, bitlink, unit, units):
        try:
            response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries?day={unit}&units={units}', headers=self.headers).json()
        except requests.exceptions.RequestException as e:
            raise(SystemExit(e))
        return response
