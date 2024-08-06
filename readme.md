## Introduction ##
This repo serves as the backend for my fyp project @https://github.com/w3ihong/FYP

## Docs ##
api end point : https://fyp-ml-ejbkojtuia-ts.a.run.app

- /run-pipeline
    - triggers the pipeline that performs ETL from Meta's API into our database

- /onboard_account/{id}
    - extracts data of a new signup, including posts and metrics. Should be triggered only once, upon connecting a new instagram account.
    - fields 
        - {id} : platform account id 

- /demographics/{id}?type={type}&timeframe={timeframe}
    - retrieves demographics data from Meta's API
    - fields 
        - {id}        : platform account id 
        - {type}      : type of users to extract, can be either "reached" or "engaged"
        - {timeframe} : duration, can be either "this_month" or "this_week"

- /trends_by_country/{country}
    - retrieves topics that trending in a specific country
    - fields
        - {country}   : full country name in lowercase and under scores (e.g united_states, singapore)

- /related_topics/{keyword}
    - retrives trending topics related to a given keyword
    - fields
        - {keyword}   : keyword in string, no specific format
        - {timeframe} : can be now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m, today 12-m or todau 5-y. defaults to now 7-d
        - {geo}       : string of the country abbreviation e.g. "US", "IN". defaults to (worldwide)

- /related_queries/{keyword}
    - rtrieves trendgin queries realted to a given keyword
    - same fields as topics


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

useful links 
Google Trends : https://pypi.org/project/pytrends/ 
Pytrends Repo : https://github.com/GeneralMills/pytrends/blob/master/examples/example.py

ConceptNet: https://github.com/commonsense/conceptnet5/wiki/API

security = https://developers.facebook.com/docs/facebook-login/security/#https
