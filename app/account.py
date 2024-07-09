import sentiment
import json
import requests
from config import supabase
from config import APP_ID

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
    
    def updatePostsTable(self):

        # get existing posts from posts table
        oldList = self.getPosts()

        # get new posts from IG
        newList = self.getIGMediaObjects()
        
        # compare with mediaList
        toUpdateInsert, toDelete = self.processLists(oldList, newList)

        if len(toUpdateInsert) == 0 and len(toDelete) == 0:
            print("No new posts to update or delete")
            return 
        
        else:
            # delete old posts
            updateSuccess = 0
            deleteSuccess = 0

            for postID in toDelete:
                try:
                    response = supabase.table('posts').delete().eq('id', postID).execute()
                     
                except:
                    print("Error deleting post: ", postID)
                    continue
                deleteSuccess += 1
                
            # insert new posts
            for postID in toUpdateInsert:
                post = self.getMediaMetadata(postID)
                try:
                    response = supabase.table('posts').insert([{
                        'id': postID,
                        'platform_account': self.platformAccID,
                        'created_at' : post['timestamp'],
                        'post_type': post['media_type'],
                        'caption': post['caption'],
                        'media_url': post['media_url'],
                        'permalink':post['permalink']

                    }]).execute()

                except:
                    print("Error inserting post: ", postID)
                    continue
                
                updateSuccess += 1

            print ("user: ", self.platformAccID)
            print ("delete Success: ", deleteSuccess, "/", len(toDelete))
            print ("update Success: ", updateSuccess, "/", len(toUpdateInsert))

            return 

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
    
    def getMediaInsights(self,mediaID):
            endpoint = f'https://graph.facebook.com/v20.0/{mediaID}/insights'
            params = {
                'fields': 'engagement,impressions,reach,saved',
                'access_token': self.accessToken
            }

            response = requests.get(endpoint, params=params)

            return
    
    
def main():

    ACCESS_TOKEN = 'EAAenAlDWmIUBO3k0yBJbAWTW615hbJnqAWjkz6idP6ZBfVPSa3EMylPbbfcsEbqwk2s21uIHpHoEKPO1ZAyMyrnaiu6Js0ZCvDxjE4PZCvAtS7zqqcw9z7A6XRJDNgIda3cutLO6VAIZAnSxrlxHhQ301n4z2mgAT4d5VVaMxtomWQV93B75tjjAWzGY46k7H'
    APP_ID = '17841466917978018'
    
    a1 = Platform_Account(APP_ID, ACCESS_TOKEN)
    # oldList = a1.getPosts()
    # print ("old list")
    # print(oldList)
    # newList = a1.getIGMediaObjects()
    # print("new list")
    # print(newList)
    # l1, l2 = a1.processLists(oldList, newList)
    a1.updatePostsTable()



if __name__ == "__main__":
    main()