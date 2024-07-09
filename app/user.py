from config import supabase

class User:

    def __init__(self,userID,platform, client) -> None:
        self.userID = userID
        self.platform = platform
        self.client = client

    def getPlatformAccID(self) -> str:
        response = supabase.table('platform_account').select('platform_account_id').eq('user_id', self.userID).eq('platform', self.platform).eq('client_name', self.client).execute()
        print(response.data[0]["platform_account_id"])
        return(response.data[0]["platform_account_id"])
