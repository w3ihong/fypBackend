from config import supabase
from account import Platform_Account

def updatePostsTable(self : Platform_Account) -> list:

    # get existing posts from posts table
    oldList = self.getPosts()
    print(oldList)

    # get new posts from IG
    newList = self.getIGMediaObjects()
    print(newList)
    
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
            post = self.getMediaMetadata(postID)
            try:
                response = supabase.table('posts').insert([{
                    'id': postID,
                    'platform_account': self.platformAccID,
                    'created_at' : post['timestamp'],
                    'post_type': post['media_type'],
                    'caption': post['caption'],
                    'media_url': post['media_url'],
                    'permalink':post['permalink'],
                    'video_thumbnail': post['thumbnail_url']

                }]).execute()

            except:
                print("Error inserting post: ", postID)
                continue
            
            updateSuccess += 1

        print ("user: ", self.platformAccID)
        print ("delete Success: ", deleteSuccess, "/", len(toDelete))
        print ("update Success: ", updateSuccess, "/", len(toUpdateInsert))
        
        return newList

def etlInsights(post,a1: Platform_Account, mediaType):

    print("post: ", post , " mediaType: ", mediaType)
    insights = a1.getMediaInsights(post, mediaType)
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
            'post_impressions': insights['impressions'],
            'post_reach': insights['reach'],
            'post_profile_visits': insights['profile_visits'] if mediaType != 'VIDEO' else 0,
            'post_sentiment': sentimentScore,
            'post_video_views': insights['video_views']
        }]).execute()
        # print("response: ", response)
        print("SUCCESS for : ", post)
    except Exception as e:
        print("FAILED for : ", post)
        print(e)
        return False
    return True

#not used for testing
def insertInsights(post, insights, sentimentScore):
    try:
        response = supabase.table('post_metrics').insert([{
            'post_id': post,
            'post_likes': insights['likes'],
            'post_shares': insights['shares'],
            'post_saved': insights['saved'],
            'post_comments': insights['comments'],
            'post_impressions': insights['impressions'],
            'post_reach': insights['reach'],
            'post_profile_visits': insights['profile_visits'],
            'post_sentiment': sentimentScore
        }]).execute()
        print("response: ", response)
    except Exception as e:
        print("etl failed for post: ", post)
        print(e)
        return False
    return True

def test():
    insights = {'video_views': 0, 'likes': 13, 'shares': 1, 'saved': 0, 'comments': 2, 'impressions': 53, 'reach': 42, 'profile_visits': 4, 'total_interactions': 16}
    sentimentScore = 0.5
    post = "101"
    insertInsights(post, insights, sentimentScore)


def main():

    # updates posts table for all accounts
    allAccounts = supabase.table('platform_account').select("platform_account_id,access_token").execute()
    print(allAccounts.data)
    accountUpdateSuccess = 0
    for account in allAccounts.data:
        if account["access_token"] == None:
            continue
        a1 = Platform_Account(account["platform_account_id"], account["access_token"])
        mediaList = updatePostsTable(a1)
        
        postUpdateSuccess = 0
        for post in mediaList:    
            type = a1.getMediaType(post)
            
            if etlInsights(post,a1, type):
                postUpdateSuccess += 1
        print("update Success: ", postUpdateSuccess, "/", len(mediaList))
        accountUpdateSuccess += 1
    print("account update Success: ", accountUpdateSuccess, "/", len(allAccounts.data))
    

if __name__ == "__main__":
    main()