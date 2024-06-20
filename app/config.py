import os
from supabase import create_client, Client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Fast API init
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://fyp-flame.vercel.app"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# supabase client init
os.environ["SUPABASE_URL"] = str("https://fpfkrvlfzcslqjfkcfzl.supabase.co")
os.environ["SUPABASE_KEY"] = str("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwZmtydmxmemNzbHFqZmtjZnpsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMxOTE0NTYsImV4cCI6MjAyODc2NzQ1Nn0.2dVff91qo0QuckDUWRfAh3KlLFF_5T6MCf90A0KEqg8")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
 
APP_ID = '2153953224988805'
APP_SECRET = '5e5874258a0f788689edadaadfb3b6a4'