from config import supabase
from account import Account
import json

def fetch_data():
    return

def transform_data():
    return

def load_data():
    return



def main():
    allAccounts = supabase.table('platform_account').select("*").execute()
    for account in allAccounts.data:
        account = Account(account["platform_account_id"], None)
        print(account)
        
        

main()  
