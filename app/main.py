import sys
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .pipeline import singleAccountOnboard 
from .pipeline import main as pipelineMain
from .config import supabase
from .account import Platform_Account
from .trends import getTrendingTopics
from .trends import getRelatedTopics
from .trends import getRelatedQueries

#Fast API init
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/onboard_account/{id}")
async def onboarding(id:int):
    account = supabase.table('platform_account').select("access_token,account_username").eq('platform_account_id', id).execute()
    access_token = account.data[0]["access_token"]
    username = account.data[0]["account_username"]
    return singleAccountOnboard(id,access_token, username)
    
@ app.get("/run_pipeline")
def pipeline():
    print(" ")
    print("Date time: ", datetime.datetime.now())
    print(" ")
    return pipelineMain()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/demographics/{id}")
def retrieve_demographics_data(
    id: str,
    type: str,
    timeframe: str
):
    account = supabase.table('platform_account').select("access_token,account_username").eq('platform_account_id', id).execute()
    access_token = account.data[0]["access_token"]
    username = account.data[0]["account_username"]
    a1 = Platform_Account(id,access_token,username)
    return a1.getDemographics(type,timeframe)
    
@app.get("/trends_by_country/{country}")
def retrieveCountryTrends(country):
    return getTrendingTopics(country)

@app.get("/related_topics/{keyword}")
def retrieve_related_topics(
    keyword: str,
    timeframe: Optional[str] = 'now 7-d',
    geo: Optional[str] = None
):  
    print("Keyword: ", keyword)
    print("Timeframe: ", timeframe)
    print("Geo: ", geo)
    return getRelatedTopics(keyword_list=[keyword], timeframe=timeframe, geo=geo)

@app.get("/related_queries/{keyword}")
def retrieve_related_queries(
    keyword: str,
    timeframe: Optional[str] = 'now 7-d',
    geo: Optional[str] = None
):  
    print("Keyword: ", keyword)
    print("Timeframe: ", timeframe)
    print("Geo: ", geo)
    return getRelatedQueries(keyword_list=[keyword],timeframe=timeframe,geo=geo)


    