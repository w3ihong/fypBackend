 
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

def getRelatedTopics(keyword_list= [''],cat=0, timeframe = 'now 7-d', geo = None, gprop = ''):
    
    # requries a payload to be built first
    buildPayload(keyword_list, cat, timeframe, geo, gprop)
    try:
        topics = pytrends.related_topics()  
    except Exception as e:
        print(e)
        return {"error": "Query failed"}
    
    return process_trends_data(topics, keyword_list)

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
    result = {}
    if risingQueries.empty and topQueries.empty:
        return {"error": "Insufficient data"}

    try:
        
        # Ensure risingQueries and topQueries contain data
        if risingQueries.empty:
            risingQueriesRA = pd.DataFrame({
                'value': [0],
                'query': ['Insufficient data']
            })
        else:
            risingQueriesRA = risingQueries[['value', 'query']]

        if topQueries.empty:
            topQueriesRA = pd.DataFrame({
                'value': [0],
                'query': ['Insufficient data']
            })
        else:
            topQueriesRA = topQueries[['value', 'query']]


    except KeyError as e:
        return {"error": "Insufficient data"}
    except TypeError as e:
        return {"error": "Insufficient data"}
    # convert to dictionary and combine
    result['rising'] = risingQueriesRA.to_dict(orient='index')
    result['top'] = topQueriesRA.to_dict(orient='index')
    return result


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

def process_trends_data(data, keyword_list):
    # Extracting the DataFrames
    rising_df = data[keyword_list[0]]['rising']
    
    top_df = data[keyword_list[0]]['top']

    result = {}
    
    # Check if the rising DataFrame is empty
    if rising_df.empty:
        result['rising'] = {
            0: {
                'formattedValue': 'N/A',
                'topic_title': 'Insufficient data'
            }
        }
    else:
        # Clean the rising DataFrame and convert it to a dictionary
        rising_cleaned = rising_df.drop(columns=['link', 'topic_mid', 'topic_type', 'value'])
        result['rising'] = rising_cleaned.to_dict(orient='index')

    # Check if the top DataFrame is empty
    if top_df.empty:
        result['top'] = {
            0: {
                'formattedValue': 'N/A',
                'topic_title': 'Insufficient data'
            }
        }
    else:
        # Clean the top DataFrame and convert it to a dictionary
        top_cleaned = top_df.drop(columns=['link', 'topic_mid', 'topic_type', 'value', 'hasData'])
        result['top'] = top_cleaned.to_dict(orient='index')
    
    return result


def main():
    keyword = ["apple"]
    
    
    # AccKw = getAccountKW(ACC_ID)
    # print(AccKw)
    
    trends = getRelatedQueries(keyword,timeframe='today 3-m')
    
    # queries = getRelatedQueries(keyword)
    # print("queries")
    # print(queries)
    # trends = getTrendingTopics("united_states")
    # trends = getRealTimeTrends("US")
    print(trends)

if __name__ == "__main__":

    main()
   