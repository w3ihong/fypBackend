# DOCs #
Google Trends : https://pypi.org/project/pytrends/ 
Pytrends Repo : https://github.com/GeneralMills/pytrends/blob/master/examples/example.py

ConceptNet: https://github.com/commonsense/conceptnet5/wiki/API

Facebook:
- Graph tool : https://developers.facebook.com/tools/explorer/2153953224988805/?method=GET&path=me%2Faccounts%3Faccess_token%3D%7Baccess_token%7D&version=v20.0
- Access Tokebns : https://developers.facebook.com/docs/facebook-login/guides/access-tokens#clienttokens

security = https://developers.facebook.com/docs/facebook-login/security/#https



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
    - can be done in js
    - for platform hashtags and google trends
    - no way to query popular hastags straight from meta api
    - flow 
        - fetch trends from google trends
        - match trends with users interest 
        - find suitable hashtags
            - 
