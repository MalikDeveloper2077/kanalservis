import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from kanalservis.settings import GOOGLE_CREDENTIALS_FILE


def get_google_service_sacc():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_CREDENTIALS_FILE, scopes
    ).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)
