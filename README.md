# Telegram Lead Capture Bot to Google Sheets

This project is a portfolio demo Telegram bot for collecting leads in chat.

It asks a user for their name, email, contact, and message. A completed lead can be saved to Google Sheets and sent to an admin as a Telegram notification.

Telegram bot messages are kept client-facing. Technical setup instructions are intentionally kept in this README, not inside the bot.

## What this project does

- Collects lead details through a guided Telegram form
- Validates email addresses and short messages
- Saves lead rows to Google Sheets when credentials are connected
- Sends a Telegram notification to the admin when `ADMIN_CHAT_ID` is set
- Runs in demo mode without Google credentials or admin notifications

## Demo features

The `/start` menu includes:

| Button | Purpose |
|---|---|
| 🧪 Test lead flow | Runs the client-facing lead capture flow |
| 📊 What happens after submit | Explains the business workflow and saved fields |
| 👨‍💼 Admin notification example | Shows the admin message format |
| 🔌 Integration status | Shows whether Sheets and admin notifications are connected |
| 💼 Business use cases | Lists ways the bot can be adapted |
| 🔗 Project info | Shows the stack, demo mode, and repo link |

Lead flow:

1. Ask for name
2. Ask for email
3. Ask for phone number or Telegram username
4. Ask what the user needs help with
5. Save or show the row, then confirm submission

## Demo mode

The bot works even when Google Sheets is not connected.

If `SPREADSHEET_ID` is empty or the credentials file is missing:

- the lead flow still completes
- the collected row is shown to the Telegram user at the end
- the row is written to the terminal log
- no Google setup errors are shown to the Telegram user

If `ADMIN_CHAT_ID` is empty:

- admin notifications are skipped
- the demo still works

In demo mode, submitted test lead data may appear in terminal logs. Do not use real customer data when testing locally.

Minimum demo setup requires only `BOT_TOKEN`.

## Full setup

1. Create a Telegram bot with BotFather.
2. Install the Python dependencies.
3. Add your environment variables.
4. Optional: connect Google Sheets.
5. Optional: set `ADMIN_CHAT_ID` for admin alerts.
6. Run the bot locally.

## Telegram BotFather setup

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot`.
3. Follow the prompts.
4. Copy the API token.
5. Put it in `.env` as `BOT_TOKEN`.

To receive admin notifications, get your own Telegram chat ID:

1. Message [@userinfobot](https://t.me/userinfobot).
2. Copy the numeric ID it returns.
3. Put it in `.env` as `ADMIN_CHAT_ID`.

## Google Sheets setup

Google Sheets is optional. Skip this section for demo mode.

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project.
3. Enable Google Sheets API.
4. Enable Google Drive API.
5. Go to IAM & Admin > Service Accounts.
6. Create a service account.
7. Create a JSON key and download it.
8. Save the file in the project root, for example as `credentials.json`.
9. Create a Google Sheet.
10. Share the sheet with the service account email as Editor.
11. Copy the spreadsheet ID from the sheet URL:

```text
https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit
```

The bot creates the worksheet tab if it does not exist.

Saved columns:

| Timestamp | Name | Email | Phone / Username | Message | Telegram ID | Telegram Username |
|---|---|---|---|---|---|---|
| 2026-05-05 14:32:00 | John Smith | john@example.com | @johnsmith | I want to automate lead collection for my business. | 123456789 | @johnsmith |

## Environment variables

Copy the example file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Variables:

| Variable | Required | Description |
|---|---:|---|
| `BOT_TOKEN` | Yes | Telegram bot token from BotFather |
| `ADMIN_CHAT_ID` | No | Telegram chat ID for admin notifications |
| `GOOGLE_CREDENTIALS_FILE` | No | Path to the Google service account JSON file |
| `SPREADSHEET_ID` | No | Google Sheet ID from the sheet URL |
| `SHEET_NAME` | No | Worksheet tab name. Defaults to `Leads` |
| `GITHUB_URL` | No | Repo URL shown in Project info after publishing |

Demo mode:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=
GOOGLE_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=
SHEET_NAME=Leads
GITHUB_URL=
```

Full setup:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=123456789
GOOGLE_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=your_google_spreadsheet_id_here
SHEET_NAME=Leads
GITHUB_URL=
```

## Run locally

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the bot:

```bash
python bot.py
```

The terminal shows which integrations are active:

```text
Bot started. Sheets: connected | Admin: connected
Bot started. Sheets: demo mode | Admin: not connected
```

## Screenshots checklist

Use `screenshots/SCREENSHOTS.md` as the capture checklist.

Required portfolio screenshots:

- `01_start_menu.png`
- `02_lead_flow_name_step.png`
- `03_invalid_email_rejection.png`
- `05_short_message_rejection.png`
- `06_final_lead_confirmation.png`
- `07_admin_notification_demo.png`
- `09_project_info.png`
- `10_integration_status.png`
- `11_what_happens_after.png`

## Security notes

- Do not commit `.env`.
- Do not commit `credentials.json`.
- Keep `BOT_TOKEN` private.
- Keep the Google service account key private.
- Share the Google Sheet only with the service account email and trusted users.
- Use a separate Google Cloud project for client demos when possible.

## Testing

```bash
python -m py_compile bot.py sheets.py config.py keyboards.py
```

## Business use cases

This bot can be adapted for:

- lead capture
- booking requests
- support requests
- consultation requests
- event registration
- small CRM intake

Each submission can be saved to Google Sheets, Airtable, Notion, or a CRM.

## Project structure

```text
.
├── bot.py
├── sheets.py
├── config.py
├── keyboards.py
├── .env.example
├── .gitignore
├── requirements.txt
├── screenshots/
│   └── SCREENSHOTS.md
└── README.md
```

## Tech stack

- Python 3.10+
- python-telegram-bot
- Google Sheets API
- gspread
- google-auth
- python-dotenv

## License

MIT
