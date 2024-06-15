
import requests
import csv

ACCESS_TOKEN = ''


# Check if the access token is set
if not ACCESS_TOKEN:
    raise ValueError("Access token not found. Please set the FACEBOOK_ACCESS_TOKEN environment variable.")

# Define the endpoint URL
endpoint = 'https://graph.facebook.com/v12.0/me/likes'

params = {
    'access_token': ACCESS_TOKEN,
    'limit': 100,  # Number of likes to retrieve (adjust as needed)
    'fields': 'name,created_time'  # Request specific fields
}


response = requests.get(endpoint, params=params)


if response.status_code == 200:
    data = response.json()
    if data['data']:
        # Create a list of dictionaries to hold the likes data
        likes_data = []
        for like in data['data']:
            like_data = {
                'name': like.get('name'),
                'created_time': like.get('created_time')
            }
            likes_data.append(like_data)
        
        # Define the CSV file name
        csv_file = 'facebook_likes.csv'
        
        # Write data to CSV
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'created_time'])
            writer.writeheader()
            writer.writerows(likes_data)
        
        print(f"Data successfully written to {csv_file}")
    else:
        print("No likes found.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
