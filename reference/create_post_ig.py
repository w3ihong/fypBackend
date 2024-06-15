import requests
#still need to try out this
access_token = ''
instagram_account_id = ''
image_url = 'phototest.jpg'
caption = 'hello please work'

# Step 1: Upload the image
upload_url = f'https://graph.facebook.com/v12.0/{instagram_account_id}/media'
payload = {
    'image_url': image_url,
    'caption': caption,
    'access_token': access_token
}
response = requests.post(upload_url, data=payload)
response_data = response.json()
creation_id = response_data['id']

# Step 2: Publish the media
publish_url = f'https://graph.facebook.com/v12.0/{instagram_account_id}/media_publish'
publish_payload = {
    'creation_id': creation_id,
    'access_token': access_token
}
publish_response = requests.post(publish_url, data=publish_payload)
publish_data = publish_response.json()
print(publish_data)
