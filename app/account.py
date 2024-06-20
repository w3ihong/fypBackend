import sentiment
import json
import uuid
import requests
from config import supabase
from config import APP_ID

class User:

    def __init__(self,userID,platform, client) -> None:
        self.userID = userID
        self.platform = platform
        self.client = client

    def getPlatformAccID(self) -> str:
        response = supabase.table('platform_account').select('platform_account_id').eq('user_id', self.userID).eq('platform', self.platform).eq('client_name', self.client).execute()
        print(response.data[0]["platform_account_id"])
        return(response.data[0]["platform_account_id"])

class Account:

    def __init__(self, accessToken, platformAccID) -> None:
        if accessToken == None:
            accessToken = self.getAccountAccesstoken()
        self.accessToken = accessToken
        self.platformAccID = platformAccID

    def getAccountAccesstoken(self) -> str:
        response = supabase.table('platform_account').select('access_token').eq('platform_account_id', self.appID).execute()
        return(response.data[0]["access_token"])

    def getAccountPages(self) -> str:
        
        endpoint = 'https://graph.facebook.com/v20.0/122114362640325987/accounts'
        params = {
            'access_token': self.accessToken
        }
        response = requests.get(endpoint, params=params)
        print("Acc page : \n")
        print(response.json())
        x = json.loads(response.text)
        return x["data"][0]["id"]

    def getPageIGBusinessAccount(self, pageID):
        endpoint =  "https://graph.facebook.com/v20.0/{}?fields=instagram_business_account&access_token={}".format(pageID, self.accessToken)
        response = requests.get(endpoint)
        print("Page busienss Acc : " + response.json())
        x = json.loads(response.text)
        return x["instagram_business_account"]["id"]
    
    def getIGMediaObjects(self):
        endpoint = 'https://graph.facebook.com/v20.0/{}/media?accesstoken={}'.format(self.getPageIGBusinessAccount(), self.accessToken)
        response = requests.get(endpoint)
        print(response.json())
        x = json.loads(response.text)
        return x["data"]
    
def main():

    ACCESS_TOKEN = 'EAAenAlDWmIUBOwgUdzuOd6tPKHoV2B1qV9a5OVxwmFBQCE3AEJIZBQE80uEGu11NqmlboMkZBPXmfJKEGe9XM4R80cL9WVxDQLm235WWLKZAW5ffauHe9tjz7o5z91zzDqIMBOTGHraZCZAXxtKdqZCsHyPgYaHaeCX1erArNoI4ZBtMSKxTZCtZClBGPBaIA0FVXVKfWTk8ubPtgE3XLBZCZAJRr6qBAZDZD'
    PAGE_ID = '335138266348897'

    testUser = uuid.UUID('8b811229-6c65-436b-9c20-5b6abbc0b02d')
    platform = 'Facebook page'
    client = 'self'
    u1 = User(testUser ,platform , client)  
    platformAccID = u1.getPlatformAccID()
    a1 = Account(platformAccID, ACCESS_TOKEN)
    pageID = a1.getAccountPages()
    ig1  = a1.getPageIGBusinessAccount(pageID)

if __name__ == "__main__":
    main()