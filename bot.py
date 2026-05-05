import logging
import warnings
from datetime import datetime

from telegram import Update
from telegram.warnings import PTBUserWarning

# per_message=False is correct here: entry is a CallbackQueryHandler but all
# conversation states use MessageHandler, so per-message tracking isn't needed.
warnings.filterwarnings(
    "ignore",
    message="If 'per_message=False'",
    category=PTBUserWarning,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import sheets
from config import (
    BOT_TOKEN,
    ADMIN_CHAT_ID,
    GITHUB_URL,
    is_admin_configured,
    is_sheets_configured,
)
from keyboards import back_to_menu, main_menu

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

ASK_NAME, ASK_EMAIL, ASK_PHONE, ASK_MESSAGE = range(4)

INTRO_TEXT = (
    "Hi! This demo shows a Telegram bot that collects leads and sends them to Google Sheets.\n\n"
    "You can test the lead flow or view what happens after a user submits a request."
)


def _is_valid_email(email: str) -> bool:
    parts = email.split("@")
    if len(parts) != 2:
        return False

    local, domain = parts
    return bool(
        local
        and domain
        and "." in domain
        and not domain.startswith(".")
        and not domain.endswith(".")
    )


def _format_saved_row(lead: dict) -> str:
    return (
        f"{lead['timestamp']} | {lead['name']} | {lead['email']} | "
        f"{lead['phone']} | {lead['message']} | "
        f"{lead['telegram_id']} | {lead['telegram_username']}"
    )


def _format_preview_row(lead: dict) -> str:
    return (
        "Preview row:\n"
        f"Timestamp: {lead['timestamp']}\n"
        f"Name: {lead['name']}\n"
        f"Email: {lead['email']}\n"
        f"Contact: {lead['phone']}\n"
        f"Message: {lead['message']}\n"
        f"Telegram ID: {lead['telegram_id']}\n"
        f"Telegram username: {lead['telegram_username']}"
    )


def _format_admin_lead(lead: dict) -> str:
    return (
        "New lead received:\n\n"
        f"Name: {lead['name']}\n"
        f"Email: {lead['email']}\n"
        f"Contact: {lead['phone']}\n"
        f"Message: {lead['message']}\n"
        f"Telegram ID: {lead['telegram_id']}\n"
        f"Telegram username: {lead['telegram_username']}\n"
        f"Timestamp: {lead['timestamp']}"
    )


def _github_line() -> str:
    if (
        GITHUB_URL
        and "YOUR_USERNAME" not in GITHUB_URL
        and "your_" not in GITHUB_URL.lower()
    ):
        return f"GitHub: {GITHUB_URL}"
    return "GitHub link will be added after publishing."


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    await update.message.reply_text(INTRO_TEXT, reply_markup=main_menu())


async def cb_menu_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(INTRO_TEXT, reply_markup=main_menu())


async def cb_after_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    text = (
        "When a user submits the form:\n"
        "1. The bot validates the answers.\n"
        "2. The lead is saved to Google Sheets.\n"
        "3. The admin receives a Telegram notification.\n"
        "4. The user gets a confirmation message.\n\n"
        "Saved fields:\n"
        "- timestamp\n"
        "- name\n"
        "- email\n"
        "- phone or Telegram username\n"
        "- message\n"
        "- Telegram ID\n"
        "- Telegram username\n\n"
        "Sample row:\n"
        "2026-05-05 14:32:00 | John Smith | john@example.com | @johnsmith | "
        "I want to automate lead collection for my business. | 123456789 | @johnsmith"
    )
    await query.edit_message_text(text, reply_markup=back_to_menu())


async def cb_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    status = (
        "Admin notifications: Connected"
        if is_admin_configured()
        else "Admin notifications: Demo mode"
    )
    text = (
        "This is what the admin receives after a new lead:\n\n"
        "New lead received:\n\n"
        "Name: John Smith\n"
        "Email: john@example.com\n"
        "Contact: @johnsmith\n"
        "Message: I want to automate lead collection for my business.\n"
        "Telegram ID: 123456789\n"
        "Telegram username: @johnsmith\n"
        "Timestamp: 2026-05-05 14:32:00\n\n"
        "Storage: Saved to Google Sheets\n\n"
        f"{status}"
    )
    await query.edit_message_text(text, reply_markup=back_to_menu())


async def cb_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    sheets_status = "Connected" if is_sheets_configured() else "Demo mode"
    admin_status = "Connected" if is_admin_configured() else "Demo mode"
    text = (
        f"Google Sheets: {sheets_status}\n"
        f"Admin notifications: {admin_status}\n\n"
        "This demo can run without Google Sheets. "
        "In demo mode, it shows the row that would be saved."
    )
    await query.edit_message_text(text, reply_markup=back_to_menu())


async def cb_use_cases(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    text = (
        "This bot can be adapted for:\n"
        "- lead capture\n"
        "- booking requests\n"
        "- support requests\n"
        "- consultation requests\n"
        "- event registration\n"
        "- small CRM intake\n\n"
        "Each submission can be saved to Google Sheets, Airtable, Notion, or a CRM."
    )
    await query.edit_message_text(text, reply_markup=back_to_menu())


async def cb_project_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "Project: Telegram Lead Capture Bot to Google Sheets\n\n"
        "This demo shows:\n"
        "- guided Telegram form\n"
        "- email/message validation\n"
        "- Google Sheets storage\n"
        "- admin notification\n"
        "- demo mode without secrets\n\n"
        "Repo:\n"
        f"{_github_line()}"
    )
    await query.edit_message_text(
        text,
        reply_markup=back_to_menu(),
        disable_web_page_preview=True,
    )


async def flow_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text("You can send /cancel anytime to stop.\n\nWhat's your name?")
    return ASK_NAME


async def got_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text("What's your name?")
        return ASK_NAME

    context.user_data["name"] = name
    await update.message.reply_text("What email should we use to contact you?")
    return ASK_EMAIL


async def got_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text.strip()
    if not _is_valid_email(email):
        await update.message.reply_text(
            "That doesn't look like an email. Please send a valid email."
        )
        return ASK_EMAIL

    context.user_data["email"] = email
    await update.message.reply_text("Send your phone number or Telegram username.")
    return ASK_PHONE


async def got_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = update.message.text.strip()
    if not phone:
        await update.message.reply_text("Send your phone number or Telegram username.")
        return ASK_PHONE

    context.user_data["phone"] = phone
    await update.message.reply_text("What do you need help with?")
    return ASK_MESSAGE


async def got_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message.text.strip()
    if len(msg) < 5:
        await update.message.reply_text("Please add a bit more detail.")
        return ASK_MESSAGE

    context.user_data["message"] = msg
    user = update.effective_user
    lead = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": context.user_data["name"],
        "email": context.user_data["email"],
        "phone": context.user_data["phone"],
        "message": context.user_data["message"],
        "telegram_id": str(user.id),
        "telegram_username": f"@{user.username}" if user.username else "not set",
    }

    row = _format_saved_row(lead)
    sheets_connected = is_sheets_configured()
    storage_state = "demo"

    if sheets_connected:
        try:
            sheets.append_lead(lead)
            storage_state = "saved"
            logger.info("Lead saved to Google Sheets: %s", row)
        except Exception as exc:
            storage_state = "write_issue"
            logger.error("Google Sheets write failed: %s", exc)

    if storage_state != "saved":
        logger.info("Preview lead row: %s", row)

    admin_sent = False
    if is_admin_configured():
        admin_storage = {
            "saved": "Saved to Google Sheets",
            "demo": "Demo preview only",
            "write_issue": "Preview shown after Sheets write issue",
        }[storage_state]
        storage_note = admin_storage
        admin_text = f"{_format_admin_lead(lead)}\n\nStorage: {storage_note}"
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)
            admin_sent = True
        except Exception as exc:
            logger.error("Admin notification failed: %s", exc)

    if storage_state == "saved":
        final_text = "Thanks! Your request was submitted."
        if admin_sent:
            final_text += "\nThe admin has been notified."
        final_text += "\n\nStorage: Saved to Google Sheets"
    else:
        if storage_state == "write_issue":
            final_text = (
                "Thanks! Demo lead completed.\n\n"
                "Storage: Preview shown because Google Sheets could not save this row\n\n"
                f"{_format_preview_row(lead)}"
            )
        else:
            final_text = (
                "Thanks! Demo lead completed.\n\n"
                "Demo mode: Google Sheets is not connected, "
                "so this lead was previewed instead of saved.\n\n"
                "Storage: Demo preview only\n\n"
                f"{_format_preview_row(lead)}"
            )

    await update.message.reply_text(final_text, reply_markup=back_to_menu())
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Flow cancelled.", reply_markup=back_to_menu())
    return ConversationHandler.END


def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in .env")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(flow_start, pattern="^flow_start$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_name)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_email)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_phone)],
            ASK_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv_handler)

    app.add_handler(CallbackQueryHandler(cb_menu_back, pattern="^menu_back$"))
    app.add_handler(CallbackQueryHandler(cb_after_submit, pattern="^menu_after_submit$"))
    app.add_handler(CallbackQueryHandler(cb_admin, pattern="^menu_admin$"))
    app.add_handler(CallbackQueryHandler(cb_status, pattern="^menu_status$"))
    app.add_handler(CallbackQueryHandler(cb_use_cases, pattern="^menu_use_cases$"))
    app.add_handler(CallbackQueryHandler(cb_project_info, pattern="^menu_project_info$"))

    logger.info(
        "Bot started. Sheets: %s | Admin: %s",
        "connected" if is_sheets_configured() else "demo mode",
        "connected" if is_admin_configured() else "not connected",
    )
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
