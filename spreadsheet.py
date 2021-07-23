from google.oauth2 import service_account
import gspread
import pandas as pd
from client import Client


class SpreadSheet(Client):
    def __init__(self, sp, sai, url):
        super().__init__(sp, sai)
        self.spreadsheet = self.client.open_by_url(url)

    def dict_to_df(self, name='Diccionario'):
        dict_worksheet = self.spreadsheet.worksheet(name)
        df = pd.DataFrame(dict_worksheet.get_all_records())
        return df

    def append_query_to_spreadsheet(self, query, query_name='Query'):
        try:
            self.spreadsheet.add_worksheet(title=query_name, rows="100", cols="20")
        except:
            pass

        self.spreadsheet.worksheet(query_name).update('A1', query_name)
        self.spreadsheet.worksheet(query_name).update('A4', query)
