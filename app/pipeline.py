from config import supabase
from account import Platform_Account
import json

def fetch_data():
    return

def transform_data():
    return

def load_data():
    return



def main():

    # updates posts table for all accounts
    allAccounts = supabase.table('platform_account').select("platform_account_id,access_token").execute()
    for account in allAccounts.data:
        if account["access_token"] == None:
            continue
        a1 = Platform_Account(account["platform_account_id"], account["access_token"])
        a1.updatePostsTable()
        
    # ETL for all posts

    
        

main()  
