 

from pytrends.request import TrendReq
import pandas as pd

pytrends  = TrendReq(hl='en-US', tz=360, timeout=(10,60), retries=2, backoff_factor=0.1)


def buildPayload(keyword_list= [],cat=0, timeframe = 'now 7-d', geo = None, gprop = None):
    # required for related topics and queries, interest over time, and interest by region
    # keyword_list: 
    # timeframe, options: now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m, today 12-m or todau 5-y. defaults to now 7-d
    # geo is a string of the country abbreviation e.g. "US". defaults to (worldwide)
    # gprop is the google property to filter results options: "images", "news", "youtube". defaults to (web searches)
    pytrends.build_payload(keyword_list, cat=cat, timeframe= timeframe, geo=geo, gprop=gprop)

def getRelatedTopics(keyword_list= [],cat=0, timeframe = 'now 7-d', geo = None, gprop = ''):
    
    # requries a payload to be built first
    buildPayload(keyword_list, cat, timeframe, geo, gprop)
    try:
        topics = pytrends.related_topics()
    except Exception as e:
        print(e)
        return {"error": "Query failed"}
    print(topics)
    risingTopics = topics[keyword_list[0]]['rising']
    topTopics = topics[keyword_list[0]]['top']
    # remove unnecessary columns
    try:
        risingTopicsCleaned = risingTopics.drop(columns=['link', 'topic_mid','topic_type','value'])
        topTopicsCleaned  = topTopics.drop(columns=['link', 'topic_mid','topic_type','value','hasData'])
    except KeyError as e:
        return {"error": "Insufficient data"}
    # convert both into dictionaries and combine them
    result = {}
    result['rising'] = risingTopicsCleaned.to_dict(orient='index')
    result['top'] = topTopicsCleaned.to_dict(orient='index')

    # result = {}
    # result['keywords'] = keyword_list
    # result['timeframe'] = timeframe
    # result['geo'] = geo
    return result

def getRelatedQueries(keyword_list= [''],cat=0, timeframe = 'now 7-d', geo = None, gprop = ''):
    # requries a payload to be built first
    buildPayload(keyword_list, cat, timeframe, geo, gprop)
    try:
        queries = pytrends.related_queries()
    except Exception as e:
        print(e)
        return {"error": "Query failed"}
    risingQueries = queries[keyword_list[0]]['rising']
    topQueries = queries[keyword_list[0]]['top']
    # rearrange the columns
    try:
        risingQueriesRA = risingQueries[['value','query']]
        topQueriesRA = topQueries[['value','query']]
    except KeyError as e:
        return {"error": "Insufficient data"}
    # convert to dictionary and combine 
    result = {}
    result['rising'] = risingQueriesRA.to_dict(orient='index')
    result['top'] = topQueriesRA.to_dict(orient='index')
    return result

def getKeywordSuggestions(keyword):
    return pytrends.suggestions(keyword)

# # doesnt work after google trends update
# def getRealTimeTrends(country = 'US'):
#     # Trending now - real time search trends on google trends
#     # country parameter takes in abbreviated country name  in CAPS e.g. "US"
#     # no topic parameter like in the website
#     try:
#         result = pytrends.realtime_trending_searches(pn = country)
#     except KeyError as e:
#         return "No matching country found"
#     except Exception as e:
#         return e
#     resultDict = result.drop(columns='entityNames').to_dict(orient='index')
#     cleaned_data = {outer_key: inner_dict[0] for outer_key, inner_dict in resultDict.items()}
#     return cleaned_data

def getTrendingTopics(country = "united_states"):
    # country parameter takes in full country name in snake_case e.g. united_states
    # default to united_states if no country is specified
    # no worldwide option
    # trending now - daily search trends on google trends
    try:
        result = pytrends.trending_searches(pn = country)
    except KeyError as e:
        return "No matching country found"
    except Exception as e:
        return e
    resultDict = result.to_dict(orient='index')
    cleaned_data = {outer_key: inner_dict[0] for outer_key, inner_dict in resultDict.items()}
    return  cleaned_data

def main():
    keyword = ["hsbaskf"]
    
    
    # AccKw = getAccountKW(ACC_ID)
    # print(AccKw)
    
    trends = getRelatedTopics(keyword,timeframe='today 1-m',)
    
    # queries = getRelatedQueries(keyword)
    # print("queries")
    # print(queries)
    # trends = getTrendingTopics("united_states")
    # trends = getRealTimeTrends("US")
    print(trends)

if __name__ == "__main__":

    main()
   