from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

pp = pprint.PrettyPrinter(indent=4)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Подключение к Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/tarasmalinovskij/Downloads/Практикум дата_Саент/key-coral-marker-395509-068b05361acc.json', scope)
client = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1vJZIuIWpWcyOF5oi0W1YzXy_YcXoUOeDUsQ9RKSFHaY/edit?usp=drive_link'
sheet = client.open_by_url(spreadsheet_url).sheet1
def update_test_results(self, expected_result, actual_result):
    """
    Обновляет таблицу Google Sheets с результатами тестов.
    """
    test_name = f"{self.__class__.__name__}.{self._testMethodName}"
    data = [test_name, expected_result, actual_result]
    sheet.insert_row(data, index=2)  # Вставляем данные начиная со второй строки