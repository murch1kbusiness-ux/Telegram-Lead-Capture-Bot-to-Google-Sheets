import logging

import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_CREDENTIALS_FILE, SHEET_NAME, SPREADSHEET_ID

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

HEADER = [
    "Timestamp",
    "Name",
    "Email",
    "Contact",
    "Message",
    "Telegram ID",
    "Telegram Username",
    "Storage Status",
]

COLUMN_WIDTHS = [170, 140, 220, 160, 380, 130, 180, 140]

def format_worksheet(worksheet) -> None:
    """Apply screenshot-friendly formatting without blocking row saves."""
    try:
        worksheet.resize(
            rows=max(worksheet.row_count, 1000),
            cols=max(worksheet.col_count, len(HEADER)),
        )
        worksheet.update(values=[HEADER], range_name="A1:H1", raw=True)

        requests = [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": worksheet.id,
                        "gridProperties": {"frozenRowCount": 1},
                    },
                    "fields": "gridProperties.frozenRowCount",
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(HEADER),
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.9,
                                "green": 0.9,
                                "blue": 0.9,
                            },
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP",
                            "textFormat": {"bold": True},
                        }
                    },
                    "fields": (
                        "userEnteredFormat(backgroundColor,horizontalAlignment,"
                        "verticalAlignment,wrapStrategy,textFormat.bold)"
                    ),
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(HEADER),
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "verticalAlignment": "TOP",
                            "wrapStrategy": "WRAP",
                        }
                    },
                    "fields": "userEnteredFormat(verticalAlignment,wrapStrategy)",
                }
            },
        ]

        for index, pixel_size in enumerate(COLUMN_WIDTHS):
            requests.append(
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": worksheet.id,
                            "dimension": "COLUMNS",
                            "startIndex": index,
                            "endIndex": index + 1,
                        },
                        "properties": {"pixelSize": pixel_size},
                        "fields": "pixelSize",
                    }
                }
            )

        worksheet.spreadsheet.batch_update({"requests": requests})
    except Exception as exc:
        logger.warning("Google Sheets formatting issue: %s", exc)

def _get_worksheet():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    try:
        worksheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=SHEET_NAME,
            rows=1000,
            cols=len(HEADER),
        )

    if not worksheet.row_values(1):
        worksheet.append_row(HEADER, value_input_option="RAW")

    format_worksheet(worksheet)
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
        lead.get("storage_status", "saved"),
    ]
    worksheet.append_row(row, value_input_option="USER_ENTERED")
