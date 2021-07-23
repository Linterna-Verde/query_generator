from google.oauth2 import service_account
import gspread

class Client:
    def __init__(self, sp, sai):
        self.scopes = sp
        self.service_account_info = sai

        #initialize the creds and client
        creds = service_account.Credentials.from_service_account_info(self.service_account_info,scopes=self.scopes)
        self.client = gspread.authorize(creds)
