import requests

#short term user access token
def getUserToken():
    
    return

#long term user access token
def getUserToken() -> str:
    return

# page token
def getFBPageToken() -> str:
    
    PAGE_ACCESS_TOKEN = ''
    PAGE_ID = ''  

    endpoint = f'https://graph.facebook.com/v12.0/{PAGE_ID}'


    params = {
        'access_token': PAGE_ACCESS_TOKEN,
        'fields': 'fan_count'
    }

    response = requests.get(endpoint, params=params)


    if response.status_code == 200:
        data = response.json()
        if 'fan_count' in data:
            likes_count = data['fan_count']
            print(f"The page has {likes_count} likes.")
        else:
            print("Could not retrieve likes count.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return 
