from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🧪 Test lead flow", callback_data="flow_start")],
            [InlineKeyboardButton("📊 What happens after submit", callback_data="menu_after_submit")],
            [InlineKeyboardButton("👨‍💼 Admin notification example", callback_data="menu_admin")],
            [InlineKeyboardButton("🔌 Integration status", callback_data="menu_status")],
            [InlineKeyboardButton("💼 Business use cases", callback_data="menu_use_cases")],
            [InlineKeyboardButton("🔗 Project info", callback_data="menu_project_info")],
        ]
    )


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back to menu", callback_data="menu_back")]]
    )
