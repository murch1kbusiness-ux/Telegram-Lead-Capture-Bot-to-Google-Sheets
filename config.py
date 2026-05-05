import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID: str = os.getenv("ADMIN_CHAT_ID", "")
GOOGLE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")
SHEET_NAME: str = os.getenv("SHEET_NAME", "Leads")
GITHUB_URL: str = os.getenv("GITHUB_URL", "")


def is_sheets_configured() -> bool:
    return bool(
        SPREADSHEET_ID
        and GOOGLE_CREDENTIALS_FILE
        and os.path.isfile(GOOGLE_CREDENTIALS_FILE)
    )


def is_admin_configured() -> bool:
    return bool(ADMIN_CHAT_ID)
