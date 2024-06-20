import account 
from config import supabase
import json
from pytrends.request import TrendReq
import pandas as pd

pytrends  = TrendReq(hl='en-US', tz=360)

def getAccountKW(accountID):
    response = supabase.table('account_keywords').select('keyword').eq('account_id', accountID).execute()
    return response.data

def getTrendingTopics(country):
    # contry parameter takes in full country name in snake_case e.g. united_states
    return pytrends.trending_searches(pn= country) 

def getKWtrend(keyword_list):
    pytrends.build_payload(keyword_list, cat=0, timeframe='today 5-y', geo='', gprop='') 
    return pytrends.interest_over_time()

def getRelatedTopics():
    return pytrends.related_topics()

def main():
    kw_list = ["keyboard"]
    # result = getKWtrend(kw_list)
    # print(result.to_string())
    trends = getTrendingTopics("united_states")
    print(trends.to_string())



if __name__ == "__main__":
    main()