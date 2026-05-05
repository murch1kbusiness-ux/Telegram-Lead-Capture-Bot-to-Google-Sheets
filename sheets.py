import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_CREDENTIALS_FILE, SHEET_NAME, SPREADSHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

HEADER = [
    "Timestamp",
    "Name",
    "Email",
    "Phone / Username",
    "Message",
    "Telegram ID",
    "Telegram Username",
]


def _get_worksheet():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    try:
        worksheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=10)

    if not worksheet.row_values(1):
        worksheet.append_row(HEADER, value_input_option="RAW")

    return worksheet


def append_lead(lead: dict) -> None:
    """Append a single lead row to the Google Sheet."""
    worksheet = _get_worksheet()
    row = [
        lead["timestamp"],
        lead["name"],
        lead["email"],
        lead["phone"],
        lead["message"],
        lead["telegram_id"],
        lead["telegram_username"],
    ]
    worksheet.append_row(row, value_input_option="USER_ENTERED")
