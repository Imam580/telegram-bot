# bot.py
import os
import re
from datetime import timedelta
from dotenv import load_dotenv

from telegram import (
    Update,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.constants import ChatMemberStatus, MessageEntityType
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= ENV =================
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN missing")

# ================= KÜFÜR (NET KELİME) =================
KUFUR_KELIMELERI = ["amk", "orospu", "piç", "ibne", "yarrak", "sik", "göt"]
KUFUR_REGEX = re.compile(rf"\b({'|'.join(KUFUR_KELIMELERI)})\b", re.I)

# ================= LİNK LİSTELERİ =================
# 🔧 BURAYA AYNI FORMATTA EKLEYEREK ÇOĞALT

SPONSORLAR = {
    "zbahis": "https://shoort.im/zbahis",
    "fixbet": "https://shoort.im/fixbet",
}

EVERY_SITELER = {
    "HızlıCasino": "https://shoort.im/hizlicasino",
    "Egebet": "https://shoort.im/egebet",
}

DOGUM_SITELER = {
    "Zbahis": "https://shoort.im/zbahis",
    "Padisahbet": "https://shoort.im/padisahbet",
}

# ================= STATE =================
spam_counter = {}

# ================= ADMIN =================
async def is_admin(update, context):
    try:
        m = await context.bot.get_chat_member(
            update.effective_chat.id,
            update.effective_user.id
        )
        return m.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except:
        return False

# ================= UNMUTE BUTONU =================
def unmute_keyboard(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔓 Mute Kaldır", callback_data=f"unmute:{user_id}")]
    ])

async def unmute_button(update, context):
    q = update.callback_query
    user_id = int(q.data.split(":")[1])
    await context.bot.restrict_chat_member(
        q.message.chat.id,
        user_id,
        ChatPermissions(can_send_messages=True)
    )
    await q.edit_message_text("🔊 Mute kaldırıldı")

# ================= GUARD: KÜFÜR =================
async def kufur_guard(update, context):
    if not update.message or not update.message.text:
        return
    if update.message.sender_chat or await is_admin(update, context):
        return

    if KUFUR_REGEX.search(update.message.text):
        await update.message.delete()
        await update.effective_chat.send_message("⚠️ Lütfen küfür etmeyin.")

# ================= GUARD: SPAM =================
async def spam_guard(update, context):
    if not update.message or update.message.sender_chat:
        return
    if await is_admin(update, context):
        return

    uid = update.message.from_user.id
    spam_counter[uid] = spam_counter.get(uid, 0) + 1

    if spam_counter[uid] == 2:
        await update.message.reply_text("⚠️ Spam yapmayın.")
    elif spam_counter[uid] >= 3:
        spam_counter[uid] = 0
        await update.message.delete()
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            uid,
            ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=1)
        )
        await update.effective_chat.send_message(
            "🔇 Spam nedeniyle 1 saat mute",
            reply_markup=unmute_keyboard(uid)
        )

# ================= GUARD: LİNK =================
async def link_guard(update, context):
    if not update.message or update.message.sender_chat:
        return
    if await is_admin(update, context):
        return

    text = update.message.text.lower()
    if "http://" in text or "https://" in text or "t.me/" in text:
        uid = update.message.from_user.id
        await update.message.delete()
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            uid,
            ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=1)
        )
        await update.effective_chat.send_message(
            "🔇 Link paylaştığınız için 1 saat mute",
            reply_markup=unmute_keyboard(uid)
        )

# ================= GUARD: KANAL ETİKET =================
async def kanal_etiket_guard(update, context):
    if not update.message or update.message.sender_chat:
        return
    if await is_admin(update, context):
        return

    if not update.message.entities:
        return

    for ent in update.message.entities:
        if ent.type == MessageEntityType.MENTION:
            text = update.message.text[ent.offset: ent.offset + ent.length]
            if text.lower().startswith("@"):
                uid = update.message.from_user.id
                await update.message.delete()
                await context.bot.restrict_chat_member(
                    update.effective_chat.id,
                    uid,
                    ChatPermissions(can_send_messages=False),
                    until_date=timedelta(hours=1)
                )
                await update.effective_chat.send_message(
                    "🔇 Kanal etiketi yasaktır",
                    reply_markup=unmute_keyboard(uid)
                )
                return

# ================= SİTE ADI ALGILAMA =================
async def site_kontrol(update, context):
    if update.message.sender_chat:
        return

    key = update.message.text.lower().strip()
    if key in SPONSORLAR:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{key.upper()} GİRİŞ", url=SPONSORLAR[key])]
        ])
        await update.message.reply_text(
            f"{key.upper()} sitesine gitmek için tıklayın",
            reply_markup=kb,
            reply_to_message_id=update.message.message_id
        )

# ================= EVERY / DOĞUM =================
async def every_kontrol(update, context):
    if update.message.text.lower() == "every":
        buttons = [[InlineKeyboardButton(n, url=u)] for n, u in EVERY_SITELER.items()]
        await update.message.reply_text(
            "🔥 Every Siteler",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

async def dogum_kontrol(update, context):
    if update.message.text.lower() == "doğum":
        buttons = [[InlineKeyboardButton(n, url=u)] for n, u in DOGUM_SITELER.items()]
        await update.message.reply_text(
            "🎉 Doğum Günü Bonusları",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ================= KOMUTLAR =================
async def ban(update, context):
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return await update.message.reply_text("Ban için mesaja yanıtlayın.")
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text("🚫 Kullanıcı banlandı.")

async def unban(update, context):
    if not await is_admin(update, context):
        return
    if not context.args:
        return
    await context.bot.unban_chat_member(
        update.effective_chat.id,
        int(context.args[0])
    )
    await update.message.reply_text("✅ Ban kaldırıldı.")

async def mute(update, context):
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
    await update.message.reply_text(
        "🔇 Kullanıcı mute edildi",
        reply_markup=unmute_keyboard(user.id)
    )

async def unmute(update, context):
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
    await update.message.reply_text("🔊 Kullanıcı açıldı.")

async def sil(update, context):
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

# ================= APP =================
app = ApplicationBuilder().token(TOKEN).build()

# COMMANDS
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(MessageHandler(filters.Regex(r"^!sil \d+$"), sil))

# CALLBACK
app.add_handler(CallbackQueryHandler(unmute_button, pattern="^unmute:"))

# MESSAGE (SIRA ÖNEMLİ)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, site_kontrol), group=0)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, every_kontrol), group=1)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dogum_kontrol), group=2)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kanal_etiket_guard), group=3)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_guard), group=4)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_guard), group=5)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kufur_guard), group=6)

print("🔥 BOT AKTİF")
app.run_polling(drop_pending_updates=True)
