import os
import requests

# Replace with your User Access Token
ACCESS_TOKEN = ''


endpoint = 'https://graph.facebook.com/v12.0/me/feed'

# Define the message you want to post
message = 'Hello test'


params = {
    'access_token': ACCESS_TOKEN,
    'message': message
}


response = requests.post(endpoint, data=params)

if response.status_code == 200:
    data = response.json()
    if 'id' in data:
        print(f"Post created successfully: {data['id']}")
    else:
        print("Error: Post ID not returned.")
        print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
