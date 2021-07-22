from google.oauth2 import service_account
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'keys.json'

class Client:
    def __init__(self, sp, sap):
        self.scopes = sp
        self.service_account_file = sap

        #initialize the creds and client
        creds = service_account.Credentials.from_service_account_file(self.service_account_file,scopes=self.scopes)
        self.client = gspread.authorize(creds)
