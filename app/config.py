import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv



# supabase client init
supabase: Client = create_client("https://fpfkrvlfzcslqjfkcfzl.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwZmtydmxmemNzbHFqZmtjZnpsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMxOTE0NTYsImV4cCI6MjAyODc2NzQ1Nn0.2dVff91qo0QuckDUWRfAh3KlLFF_5T6MCf90A0KEqg8")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

NOW = int(time.time())

UNIX_WEEK = 604800
UNIX_MONTH = 2629743
FB_MONTH = 2592000
 
