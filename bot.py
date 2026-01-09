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
            ChatMemberStatus.OWNER
        )
    except:
        return False

# ================= KÜFÜR =================
async def kufur_kontrol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if update.message.sender_chat:
        return
    if await is_admin(update, context):
        return

    text = update.message.text.lower()
    for k in KUFUR_LISTESI:
        if k in text:
            try:
                await update.message.delete()
            except:
                pass
            return

# ================= LINK =================
async def link_engel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if update.message.sender_chat:
        return
    if await is_admin(update, context):
        return

    text = update.message.text.lower()
    if "http://" in text or "https://" in text or "t.me/" in text:
        try:
            await update.message.delete()
        except:
            pass

# ================= SPAM =================
async def spam_kontrol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if update.message.sender_chat:
        return
    if await is_admin(update, context):
        return

    uid = update.message.from_user.id
    spam_counter[uid] = spam_counter.get(uid, 0) + 1

    if spam_counter[uid] >= 7:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            uid,
            ChatPermissions(can_send_messages=False),
            until_date=timedelta(minutes=30)
        )
        spam_counter[uid] = 0

# ================= SITE =================
async def site_kontrol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    for key, link in FILTERS.items():
        if key in text:
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"🔗 {key.upper()} GİRİŞ", url=link)]
            ])
            await update.message.reply_text(
                f"✅ <b>{key.upper()}</b>",
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

# ================= KOMUTLAR =================
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    if len(context.args) < 2:
        await update.message.reply_text("/filter site link")
        return
    FILTERS[context.args[0].lower()] = context.args[1]
    await update.message.reply_text("✅ Filtre eklendi")

async def remove_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    if not context.args:
        return
    FILTERS.pop(context.args[0].lower(), None)
    await update.message.reply_text("🗑️ Filtre kaldırıldı")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    if not context.args:
        return
    await context.bot.unban_chat_member(
        update.effective_chat.id,
        int(context.args[0])
    )

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        ChatPermissions(can_send_messages=False)
    )

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        ChatPermissions(can_send_messages=True)
    )

async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    await context.bot.set_chat_permissions(
        update.effective_chat.id,
        ChatPermissions()
    )

async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    await context.bot.set_chat_permissions(
        update.effective_chat.id,
        ChatPermissions(can_send_messages=True)
    )

async def sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
    try:
        n = int(update.message.text.split()[1])
    except:
        return

    for i in range(n):
        try:
            await context.bot.delete_message(
                update.effective_chat.id,
                update.message.message_id - i
            )
        except:
            pass

# ================= BOT =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, site_kontrol), group=0)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kufur_kontrol), group=1)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_engel), group=2)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_kontrol), group=3)
app.add_handler(MessageHandler(filters.Regex(r"^!sil \d+$"), sil), group=4)

app.add_handler(CommandHandler("filter", add_filter))
app.add_handler(CommandHandler("remove", remove_filter))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("lock", lock))
app.add_handler(CommandHandler("unlock", unlock))

print("🔥 BOT AKTİF")
app.run_polling()
