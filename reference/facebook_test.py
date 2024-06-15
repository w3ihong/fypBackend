
import os
import requests
import csv


ACCESS_TOKEN = ''

# Check if the access token is set
if not ACCESS_TOKEN:
    raise ValueError("Access token not found. Please set the FACEBOOK_ACCESS_TOKEN environment variable.")

# Define the endpoint URL
endpoint = 'https://graph.facebook.com/v12.0/me/posts'  # Use 'me/posts' endpoint for user's posts


params = {
    'access_token': ACCESS_TOKEN,
    'limit': 10,  # Number of posts to retrieve
    'fields': 'message,created_time,attachments{media_type,media_url}'  # Request specific fields including media
}

# Make a GET request to the Facebook Graph API
response = requests.get(endpoint, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data['data']:
        # Create a list of dictionaries to hold the post data
        posts_data = []
        for post in data['data']:
            post_data = {
                'message': post.get('message'),
                'created_time': post.get('created_time')
            }

            # Check if there are attachments and add media data
            if 'attachments' in post:
                attachments = post['attachments']['data'][0]
                post_data['media_type'] = attachments.get('media_type')
                post_data['media_url'] = attachments.get('media_url')
            else:
                post_data['media_type'] = None
                post_data['media_url'] = None

            posts_data.append(post_data)

        # Define the CSV file name
        csv_file = 'facebook_posts_with_media.csv'

        # Write data to CSV
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['message', 'created_time', 'media_type', 'media_url'])
            writer.writeheader()
            writer.writerows(posts_data)

        print(f"Data successfully written to {csv_file}")
    else:
        print("No posts found.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)