# DOCs #
Google Trends : https://pypi.org/project/pytrends/ 
Pytrends Repo : https://github.com/GeneralMills/pytrends/blob/master/examples/example.py

Facebook:
- Graph tool : https://developers.facebook.com/tools/explorer/2153953224988805/?method=GET&path=me%2Faccounts%3Faccess_token%3D%7Baccess_token%7D&version=v20.0
- Access Tokebns : https://developers.facebook.com/docs/facebook-login/guides/access-tokens#clienttokens

Local HTTPS : https://akshitb.medium.com/how-to-run-https-on-localhost-a-step-by-step-guide-c61fde893771


## modules ##
- nlp for comments (done)
    
    - flow 
        1. get comments
        2. get sentiment
        3. get average sentiment
        4. store in db


- data extraction and loading
    - daily? realtime (computationally intensive)?
    - requirements
        - scheduling function
        - 
    - flow
        1. get all accounts item  in db
        2. for each acc, extract all posts and check agaisnt db
        3. for each post get metrics and add to db
        4. check 

- trends
    - for platform hashtags and google trends
    - no way to query popular hastags straight from meta api
    - flow 
        - fetch trends from google trends
        - match trends with users interest 
        - find suitable hashtags
            - 

- Posting recommendations 
    - model selection ()
    - train on 

- network analysis
    - cant get follower's details or own's follwers
    - can get details of any business/creator account
