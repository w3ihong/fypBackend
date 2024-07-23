import json
import requests
# from .sentiment import getBlobSentiment
# from .config import supabase
from sentiment import getBlobSentiment
from config import supabase

class Platform_Account:

    def __init__(self, platformAccID, accessToken, username) -> None:
        # if accessToken == None:
        #     accessToken = self.getAccountAccesstoken()
        self.accessToken = accessToken
        self.platformAccID = platformAccID
        self.username = username

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
        endpoint = 'https://graph.facebook.com/v20.0/{platformAccID}/media?access_token={accessToken}'.format(platformAccID= self.platformAccID, accessToken=self.accessToken)
        
        response = requests.get(endpoint)
        x = response.json()
        mediaList = [int(item['id']) for item in x["data"]]
        return mediaList
    
    def getPosts(self):
        existingPosts = supabase.table('posts').select('id').eq('platform_account', self.platformAccID).execute()
        itemList = [item['id'] for item in existingPosts.data]
        return itemList
        
    def getMediaMetadata(self,mediaID):
        endpoint = f'https://graph.facebook.com/v20.0/{mediaID}'
        params = {
            'fields': 'id,media_type,media_url,thumbnail_url,permalink,caption,timestamp',
            'access_token': self.accessToken
        }

        response = requests.get(endpoint, params=params)
        return response.json(), self.getMediaType(mediaID)
    
    def getMediaType(self,mediaID):
        endpoint = f'https://graph.facebook.com/v20.0/{mediaID}'
        params = {
            'fields': 'media_type',
            'access_token': self.accessToken
        }

        response = requests.get(endpoint, params=params)
        return response.json()['media_type']
    
    def processLists(self,oldList, newList):
        oldSet = set(oldList)
        newSet = set(newList)

        toUpdateInsert = newSet
        toDelete = []


        # Find items to delete
        for itemID in oldSet:
            if itemID not in newSet:
                toDelete.append(itemID)

        return toUpdateInsert, toDelete
    

    def getMediaInsights(self,mediaID, mediaType):
        if mediaType == 'VIDEO':
            metrics = 'likes,shares,saved,comments,impressions,reach,video_views,total_interactions'
        else :
            metrics = 'likes,shares,saved,comments,impressions,reach,profile_visits,video_views,total_interactions'
        
        endpoint = f'https://graph.facebook.com/v20.0/{mediaID}/insights?metric={metrics}&access_token={self.accessToken}'
        
        response = requests.get(endpoint)
        result = {item['name']: item['values'][0]['value'] for item in (response.json())['data']}
        print(result)
        return result
    
    def getMediaSentiment(self,mediaID):
        endpoint = f'https://graph.facebook.com/v20.0/{mediaID}/comments?access_token={self.accessToken}'
        
        response = requests.get(endpoint)
        texts = [item['text'] for item in (response.json())['data']]

        sentimentScore = 0
        # Printing the result
        for text in texts:
            score = getBlobSentiment(text)
            sentimentScore += score

        return sentimentScore/len(texts)
    
    def getAccountFollowers(self):
        endpoint = f'https://graph.facebook.com/v20.0/{self.platformAccID}?fields=business_discovery.username({self.username}){{followers_count}}&access_token={self.accessToken}'
        response = requests.get(endpoint)
        return response.json()["business_discovery"]["followers_count"]
    
        
    def getFollowerDemographics(self):
        endpoint = f'https://graph.facebook.com/v20.0/{self.platformAccID}/insights?metric=follower_demographics&period=lifetime&metric_type=total_value&breakdown=age,city,country,gender&access_token={self.accessToken}'
        print (endpoint)
        response = requests.get(endpoint)
        
        print (response.json())
        return 
    
    def getEngagedDemographics(self):
        return
    
    def getReachDemographics(self):
        return

def main():

    ACCESS_TOKEN = 'EAAenAlDWmIUBOw8If8twNUWZAu1oUT6mxwQrFoMMRrHXoKuYhd6OZCfXL9ZCftV5YisEZBeGebjpneqCjx9FU2XJJ6fGPvc5UDrnXZC9jwmxX2iX4iNZAUbGtZBlpddet0bK3toCWHncyn2HrSCLe0XSIHToyQaYlWvLNSo0ucfP4DHirlVKr2f9whV69QqSRa3'
    APP_ID = '17841466917978018'
    USERNAME = 'echosphere.sg'
    
    newList = [17963029475773994, 17919006197946852, 17940105560831903, 18150262132315832, 17976896420565504, 18060744193576295, 18012362903177861, 17959705052772586]
    
    postID = 18012362903177861

    a1 = Platform_Account(APP_ID, ACCESS_TOKEN, USERNAME)
    # a1.getFollowerDemographics()



if __name__ == "__main__":
    main()