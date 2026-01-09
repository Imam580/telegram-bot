# bot.py
import os
from datetime import timedelta
from dotenv import load_dotenv

from telegram import (
    Update,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= ENV =================
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN environment variable is missing!")

# ================= KÜFÜR =================
KUFUR_LISTESI = [
    "amk","aq","amq","anan","ananı","amına","amina",
    "orospu","piç","ibne","yarrak","yarak","sik",
    "göt","gavat","salak","aptal","gerizekalı","mal"
]

# ================= FİLTRELER =================
FILTERS = {
    "zbahis": "https://shoort.im/zbahis",
    "fixbet": "https://shoort.im/fixbet",
    "betoffice": "https://shoort.im/betoffice",
}

# ================= SPAM =================
spam_counter = {}

# ================= ADMIN =================
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(
            update.effective_chat.id,
            update.effective_user.id
        )
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
