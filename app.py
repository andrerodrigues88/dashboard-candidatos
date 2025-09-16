import os
import datetime
from flask import Flask, render_template
from dotenv import load_dotenv
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Carregar variáveis de ambiente do .env
load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIALS_FILE = 'credentials.json'

app = Flask(__name__)

def get_sheet_data():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A1:Z1000'  # Ajuste se precisar
    ).execute()
    
    return result.get('values', [])

@app.route('/')
def dashboard():
    data = get_sheet_data()
    num_candidatos = len(data) - 1 if data else 0  # Menos o cabeçalho
    return render_template('dashboard.html', data=data, num_candidatos=num_candidatos)

if __name__ == '__main__':
    app.run(debug=True)
