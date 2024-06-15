import sentiment
import json
import uuid
from env import supabase

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

    def __init__(self,appID) -> None:
        self.appID = appID
        

    def getPlatformAccMetrics(self) -> str:
        return

def main():

    ACCESS_TOKEN = 'EAAenAlDWmIUBO2FZAO9WxyLqg5VWb22uLzAki5CZAbEtM76aVs3IPyvN60gBzx7IjWZCWKUZAr3uozYaKwxWGpL1ZAHlowiX0DsWgsGgsQ2l5lYzSJAe1nXZC6Ia0huL5CJGS0tnZB88VGzCMJGFtOeNZA8jV4lEl4mo1iPwZCXJsl5ZCGipgZBDzO3dtUAWpJGTGNZCvQZDZD'
    testUser = uuid.UUID('8b811229-6c65-436b-9c20-5b6abbc0b02d')
    platform = 'Facebook'
    client = 'john james'
    u1 = User(testUser ,platform , client)
    platformAccID = u1.getPlatformAccID()
    a1 = Account(platformAccID)
    

if __name__ == "__main__":
    main()