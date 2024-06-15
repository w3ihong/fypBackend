
import requests 
import csv

# Read the access token
ACCESS_TOKEN = ''


if not ACCESS_TOKEN:
    raise ValueError("Access token not found. Please set the FACEBOOK_ACCESS_TOKEN environment variable.")

endpoint = 'https://graph.facebook.com/v12.0/me/friends'

params = {
    'access_token': ACCESS_TOKEN,
    'limit': 50  # Number of friends to retrieve (adjust as needed)
}

response = requests.get(endpoint, params=params)


if response.status_code == 200:
    data = response.json()
    if data['data']:
       
        friends_data = []
        for friend in data['data']:
            friend_data = {
                'name': friend.get('name'),
                'id': friend.get('id')
            }
            friends_data.append(friend_data)
        
        
        csv_file = 'facebook_friends.csv'
        
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'id'])
            writer.writeheader()
            writer.writerows(friends_data)
        
        print(f"Data successfully written to {csv_file}")
    else:
        print("No friends found.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
