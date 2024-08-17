from .config import supabase
from .account import Platform_Account
# from config import supabase
# from account import Platform_Account


def updatePostsTable(self : Platform_Account) -> list:

    # get existing posts from posts table
    oldList = self.getPosts()

    # get new posts from IG
    newList = self.getIGMediaObjects()
    NEWwithMedia = {}
    # compare with mediaList
    toUpdateInsert, toDelete = self.processLists(oldList, newList)

    if len(toUpdateInsert) == 0 and len(toDelete) == 0:
        print("No new posts to update or delete")
        return newList
    
    else:
        # delete old posts
        updateSuccess = 0
        deleteSuccess = 0

        for postID in toDelete:
            try:
                response = supabase.table('posts').delete().eq('id', postID).execute()
            except Exception as e:
                print("Error deleting post: ", postID)
                print(e)
                continue
            deleteSuccess += 1
            
        # insert new posts
        for postID in toUpdateInsert:
            post,mediaType = self.getMediaMetadata(postID)
            try:
                response = supabase.table('posts').upsert([{
                    'id': postID,
                    'platform_account': self.platformAccID,
                    'created_at' : post['timestamp'],
                    'post_type': post['media_type'],
                    'caption': post['caption'],
                    'media_url': post['media_url'],
                    'permalink':post['permalink'],
                    'video_thumbnail': post['thumbnail_url'] if post['media_type'] == 'VIDEO' else None

                }]).execute()
                NEWwithMedia[postID] = mediaType
            except Exception as e:
                print("Error inserting post: ", postID)
                print(e)
                continue
            
            updateSuccess += 1

        print ("USER: ", self.platformAccID)
        print ("MediaList: ", NEWwithMedia)
        print ("Update Success: ", updateSuccess, "/", len(toUpdateInsert))
        print ("Delete Success: ", deleteSuccess, "/", len(toDelete))
        print (" ")
        
        return NEWwithMedia

def updatePostMetrics(post,a1: Platform_Account, mediaType, followers):

    insights = a1.getMediaInsights(post, mediaType)
    if insights == None:
        print("Failed to get insights for: ", post)
        return False , {}
    if insights['comments'] != 0:
        sentimentScore = a1.getMediaSentiment(post)
    else:
        sentimentScore = 0
    try:    
        response = supabase.table('post_metrics').insert([{
            'post_id': post,
            'post_likes': insights['likes'],
            'post_shares': insights['shares'],
            'post_saved': insights['saved'],
            'post_comments': insights['comments'],
            'post_impressions': insights['impressions'] if mediaType != 'VIDEO' else insights['video_views'],
            'post_reach': insights['reach'],
            'post_profile_visits': insights['profile_visits'] if mediaType != 'VIDEO' else 0,
            'post_sentiment': sentimentScore,
            'post_video_views': insights['video_views'],
            'post_amplification_rate' : insights['shares']/followers
        }]).execute()
        print("SUCCESS for : ", post)
    except Exception as e:
        print("Failed store data  for : ", post)
        print(e)
        return False, {}
    
    fullMetrics = {"id": post , "likes":insights["likes"], "shares": insights['shares'], "saved": insights["saved"], "comments": insights["comments"], "impressions": insights["impressions"], "reach" : insights["reach"], "profile_visits" : insights['profile_visits'] if mediaType != 'VIDEO' else 0, "sentiment" : sentimentScore, "video_views" : insights['video_views'], "amplification_rate":insights['shares']/followers }
    
    return True, fullMetrics

def updateAccountMetrics(metrics, postCount, a1: Platform_Account):
    metrics["sentiment"] = metrics["sentiment"]/postCount
    print("Account metrics: ", metrics)
    try:
        response = supabase.table('platform_metrics').insert([{
            'platform_account' : a1.platformAccID,
            'platform_profile_visits' : metrics["profile_visits"],
            'platform_followers' : metrics["followers"],
            'platform_likes' : metrics["likes"],
            'platform_comments' : metrics['comments'],
            'platform_saves' : metrics['saved'],
            'platform_shares' : metrics['shares'],
            'platform_impressions' : metrics['impressions'],
            'platform_sentiment' : metrics['sentiment']
            # reach cannot be derieved 

        }]).execute()
        print("Account metrics Success for :", a1.platformAccID)
    except Exception as e:
        print( "Account metrics Failed for :", a1.platformAccID)
        print (e)
        return False
    
    return True

def singleAccountOnboard(id, access_token, username):
    # account = supabase.table('platform_account').select("access_token,account_username").eq('platform_account_id', id).execute()
    # access_token = account.data[0]["access_token"]
    # username = account.data[0]["account_username"]
    print ("Onboarding Account: ", id)
    a1 = Platform_Account(id, access_token, username)
    mediaList = updatePostsTable(a1)
    followers = a1.getAccountFollowers()
    postUpdateSuccess = 0
    accountMetrics = {"video_views" : 0, "likes": 0 , "shares": 0 , "saved": 0, "comments": 0 , "impressions": 0, "profile_visits" : 0, "sentiment" : 0 , "sentiment" : 0, "followers" : followers}
    
    for post in mediaList:
        type = mediaList[post]
        insightsETLSuccess, fullPostMetrics = updatePostMetrics(post,a1,type,followers)
        if insightsETLSuccess:
            accountMetrics['likes'] += fullPostMetrics['likes']
            accountMetrics['shares'] += fullPostMetrics['shares']
            accountMetrics['saved'] += fullPostMetrics['saved']
            accountMetrics['comments'] += fullPostMetrics['comments']
            accountMetrics['impressions'] += fullPostMetrics['impressions']
            accountMetrics['profile_visits'] += fullPostMetrics['profile_visits']
            accountMetrics['sentiment'] += fullPostMetrics['sentiment']
            accountMetrics['video_views'] += fullPostMetrics['video_views']

            postUpdateSuccess += 1
    

    print("update Success: ", postUpdateSuccess, "/", len(mediaList))
    
    accountMetricsUpdate = updateAccountMetrics(accountMetrics, len(mediaList), a1)
    print("Full Account Metrics ", accountMetrics)
    if accountMetricsUpdate:
        return True
    return False

def updateDemographics(a1 :Platform_Account):
    followerDemo = a1.getFollowerDemographics()
    if followerDemo == False:
        followerDemo = {'age': "More than 100 followers required for demographics data", 'city': '', 'country': '', 'gender': ''}
    try:
        response = supabase.table('follower_demographics').insert([{    
            'platform_account' : a1.platformAccID,
            'age' : followerDemo['age'],
            'city' : followerDemo['city'],
            'country' : followerDemo['country'],
            'gender' : followerDemo['gender']
        }]).execute()
    except Exception as e:
        print("Demographics update failed for: ", a1.platformAccID)
        print(e)
        return False

    return True

def main():
    # updates posts table for all accounts
    allAccounts = supabase.table('platform_account').select("platform_account_id,access_token,account_username").execute()
    accountUpdateSuccess = 0
    for account in allAccounts.data:
        if account["access_token"] == None:
            continue
        a1 = Platform_Account(account["platform_account_id"], account["access_token"], account["account_username"])
        mediaList = updatePostsTable(a1)
        followers = a1.getAccountFollowers()
        postUpdateSuccess = 0
        accountMetrics = {"video_views" : 0, "likes": 0 , "shares": 0 , "saved": 0, "comments": 0 , "impressions": 0, "profile_visits" : 0, "sentiment" : 0 , "sentiment" : 0, "followers" : followers}
        
        for post in mediaList:
            type = mediaList[post]
            insightsETLSuccess, fullPostMetrics = updatePostMetrics(post,a1,type,followers)
            if insightsETLSuccess:
                accountMetrics['likes'] += fullPostMetrics['likes']
                accountMetrics['shares'] += fullPostMetrics['shares']
                accountMetrics['saved'] += fullPostMetrics['saved']
                accountMetrics['comments'] += fullPostMetrics['comments']
                accountMetrics['impressions'] += fullPostMetrics['impressions'] if type != 'VIDEO' else fullPostMetrics['video_views']
                accountMetrics['profile_visits'] += fullPostMetrics['profile_visits']
                accountMetrics['sentiment'] += fullPostMetrics['sentiment']
                accountMetrics['video_views'] += fullPostMetrics['video_views']

                postUpdateSuccess += 1

        print("Post update Success: ", postUpdateSuccess, "/", len(mediaList))

        # demographics update here
        result = updateDemographics(a1)
        if result:
            print("Demographics update Success")
        else:
            print("Demographics update Failed")

        accountMetricsUpdate = updateAccountMetrics(accountMetrics, len(mediaList), a1)
        
        if accountMetricsUpdate:
            print ("Account metrics Success")
            accountUpdateSuccess += 1
        else:
            print ("Account metrics Failed")

    print("Account update Success: ", accountUpdateSuccess, "/", len(allAccounts.data))
    

if __name__ == "__main__":
    ACCESS_TOKEN = 'EAAenAlDWmIUBOw8If8twNUWZAu1oUT6mxwQrFoMMRrHXoKuYhd6OZCfXL9ZCftV5YisEZBeGebjpneqCjx9FU2XJJ6fGPvc5UDrnXZC9jwmxX2iX4iNZAUbGtZBlpddet0bK3toCWHncyn2HrSCLe0XSIHToyQaYlWvLNSo0ucfP4DHirlVKr2f9whV69QqSRa3'
    APP_ID = '17841466917978018'
    USERNAME = 'echosphere.sg'

    a1 = Platform_Account(APP_ID,ACCESS_TOKEN,USERNAME)
    updatePostMetrics('18024137249095516',a1,'CAROUSEL_ALBUM', 108)