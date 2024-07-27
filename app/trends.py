 
from config import supabase
import json
from pytrends.request import TrendReq
import pandas as pd
from nltk.corpus import wordnet

pytrends  = TrendReq(hl='en-US', tz=360, timeout=(10,60), retries=3, backoff_factor=0.1)

def getAccountKW(accountID):
    response = supabase.table('platform_account').select('category').eq('platform_account_id', accountID).execute()
    return response.data[0]['category']

def buildPayload(keyword_list, timeframe = 'today 5-y', geo = '', gprop = ''):
    pytrends.build_payload(keyword_list, cat=0, timeframe= timeframe, geo=geo, gprop=gprop)

def getTrendingTopics(country = "united_states"):
    # country parameter takes in full country name in snake_case e.g. united_states
    # default to world if no country is specified
    return pytrends.trending_searches(pn = country) 

def getKWtrend(keyword_list, tf = 'today 5-y' ):
    #gets the trends of a list of keywords
    pytrends.build_payload(keyword_list, cat=0, timeframe= tf, geo='', gprop='') 
    return pytrends.interest_over_time()

def getRelatedTopics():
    return pytrends.related_topics()

def getRealTimeTrends(country = 'US'):
    return pytrends.realtime_trending_searches(pn = country)


def getKeywordSuggestions(keyword):
    return pytrends.suggestions(keyword)

def getRelatedTrends():
    #match user's keywords with trends
    return 

def getTrends(accountID):

    AccKeyWords = getAccountKW(accountID)
    relatedTrends = getRelatedTrends(AccKeyWords)

    return 

def main():
    keyword_list = ['gaming']
    # result = getKWtrend(kw_list)
    # print(result.to_string())
    # AccKw = getAccountKW(28736509815)
    # trends = getRelatedTrends(AccKw)
    pytrends.build_payload(keyword_list, cat=0, timeframe= 'today 5-y', geo='', gprop='') 

    trends = getTrendingTopics("singapore")
    print(trends.to_string())
    relatedTrends = getRelatedTopics()
    print(relatedTrends)


if __name__ == "__main__":

    main()
    # # Get synsets for a word
    # synsets = wordnet.synsets('dog')

    # # Get definitions and examples
    # for synset in synsets:
    #     print(synset.definition())
    #     print(synset.examples())