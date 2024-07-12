import sentiment
import json
import requests
import time
from config import supabase
from config import APP_ID
from config import NOW

class Platform_Account:

    def __init__(self, platformAccID, accessToken) -> None:
        # if accessToken == None:
        #     accessToken = self.getAccountAccesstoken()
        self.accessToken = accessToken
        self.platformAccID = platformAccID


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
        return response.json()
    
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

        toUpdateInsert = []
        toDelete = []

        # Find items to update or insert
        for itemID in newSet:
            if itemID not in oldSet:
                toUpdateInsert.append(itemID)

        # Find items to delete
        for itemID in oldSet:
            if itemID not in newSet:
                toDelete.append(itemID)

        print("toUpdateInsert: ", toUpdateInsert)
        print("toDelete: ", toDelete)
        return toUpdateInsert, toDelete
    

    def getMediaInsights(self,mediaID, mediaType):
        if mediaType == 'VIDEO':
            metrics = 'likes,shares,saved,comments,impressions,reach,video_views,total_interactions'
        else :
            metrics = 'likes,shares,saved,comments,impressions,reach,profile_visits,video_views,total_interactions'
        
        endpoint = f'https://graph.facebook.com/v20.0/{mediaID}/insights?metric={metrics}&access_token={self.accessToken}'
        

        response = requests.get(endpoint)
        print (response.json())
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
            score = sentiment.getBlobSentiment(text)
            sentimentScore += score

        return sentimentScore/len(texts)
        
    
    def getAccountInsights(self, since, until = NOW, period : str = 'day'):

        # followerEndpoint = f'https://graph.facebook.com/v20.0/{self.platformAccID}/insights?metric=follower_count&period={period}&since={since}&until={until}&access_token={self.accessToken}'

        metric = "impressions,reach,profile_views,total_interactions,accounts_engaged,likes,comments,saves,shares"
        if since == None:
            endpoint = f'https://graph.facebook.com/v20.0/{self.platformAccID}/insights?metric={metric}&period={period}&metric_type=total_value&access_token={self.accessToken}'
        else:
            endpoint = f'https://graph.facebook.com/v20.0/{self.platformAccID}/insights?metric={metric}&period={period}&metric_type=total_value&since={since}&until={until}&access_token={self.accessToken}'

        response = requests.get(endpoint)
        # response = requests.get(endpoint)
        
        return response.json()
    
        
    def getFollowerDemographics(self):
        return 
    
    def getEngagedDemographics(self):
        return
    
    def getReachDemographics(self):
        return



def main():

    ACCESS_TOKEN = 'EAAenAlDWmIUBO3k0yBJbAWTW615hbJnqAWjkz6idP6ZBfVPSa3EMylPbbfcsEbqwk2s21uIHpHoEKPO1ZAyMyrnaiu6Js0ZCvDxjE4PZCvAtS7zqqcw9z7A6XRJDNgIda3cutLO6VAIZAnSxrlxHhQ301n4z2mgAT4d5VVaMxtomWQV93B75tjjAWzGY46k7H'
    APP_ID = '17841466917978018'

    newList = [17963029475773994, 17919006197946852, 17940105560831903, 18150262132315832, 17976896420565504, 18060744193576295, 18012362903177861, 17959705052772586]
    
    postID = 18012362903177861

    a1 = Platform_Account(APP_ID, ACCESS_TOKEN)
    # oldList = a1.getPosts()
    # print ("old list")
    # print(oldList)
    # newList = a1.getIGMediaObjects()
    # print(newList)

    # score = a1.getMediaSentiment(postID)

    i1 = a1.getAccountInsights(None, None, 'day')
    print(i1)

    # for i in newList:
    #     a1.getMediaInsights(i)



if __name__ == "__main__":
    main()