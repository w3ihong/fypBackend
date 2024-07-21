import sys
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .pipeline import singleAccountOnboard 
from .pipeline import main as pipelineMain
from .config import supabase

#Fast API init
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost","http://localhost:8000","http://localhost:3000", "https://fyp-flame.vercel.app"],  # Frontend URL
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
