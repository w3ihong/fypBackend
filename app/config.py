import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv("./.env.local")


# supabase client init
url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

NOW = int(time.time())

UNIX_WEEK = 604800
UNIX_MONTH = 2629743
FB_MONTH = 2592000
 
