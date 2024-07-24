# Introduction #
This repo serves as the backend for my fyp project @https://github.com/w3ihong/FYP

# DOCs #
api end point : https://fyp-ml-ejbkojtuia-ts.a.run.app

- /run-pipeline
    - triggers the pipelien that performs ETL from Meta's API into our database

- /onboard_account/{id}
    - extracts data of a new signup, including posts and metrics. Should be triggered only once, upon connecting a new instagram account.
    - fields 
        - {id} : platform account id 

- /demographics/{id}/{type}/{timeframe}
    - retrieves demographics data from Meta's API
    - fields 
        - {id}        : platform account id 
        - {type}      : type of users to extract, can be either "reached" or "engaged"
        - {timeframe} : duration, can be either "this_month" or "this_week"

- /trends
    - 
## hosting ##
- containerized with docker and hosted on google cloud run 
- data pipeline is triggered by gloud scheduer every day at 12 midnight SGT

## modules ##

- data pipeline 
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
            

## TODO ##
- better nlp model for sentiment (emojis)
- hosting and automating pipeline

# useful links #
Google Trends : https://pypi.org/project/pytrends/ 
Pytrends Repo : https://github.com/GeneralMills/pytrends/blob/master/examples/example.py

ConceptNet: https://github.com/commonsense/conceptnet5/wiki/API

security = https://developers.facebook.com/docs/facebook-login/security/#https
