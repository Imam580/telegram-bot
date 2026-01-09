# bot.py
import os
import re
import random
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
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= ENV =================
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN environment variable is missing!")

# ================= DATA =================
KUFUR_LISTESI = [
    "amk","amına","amina","orospu","piç","ibne",
    "yarrak","yarak","sik","sikeyim","göt","gavat"
]

EVERY_LINKLER = [
    "https://shoort.im/hizlicasino","https://shoort.im/egebet",
    "https://shoort.im/kavbet","https://shoort.im/pusulabet",
    "https://shoort.im/hitbet","https://shoort.im/artemisbet"
]

DOGUM_LINKLERI = [
    "https://shoort.im/zbahis","https://shoort.im/padisahbet",
    "https://shoort.im/fixbet","https://shoort.im/betoffice"
]

SPONSORLAR = {
    "zbahis": "https://shoort.in/zbahis",
    "fixbet": "https://shoort.in/fixbet",
    "betoffice": "https://shoort.in/betoffice",
    "artemisbet": "https://shoort.in/artemisbet",
}

spam_sayac = {}
mesaj_sayac = {}
cekilis_katilim = set()
cekilis_kazanan_sayi = 1

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

# ================= COMMANDS =================
async def sponsor(update, context):
    kb = [[InlineKeyboardButton(k.upper(), url=v)] for k, v in SPONSORLAR.items()]
    await update.message.reply_text("📢 Sponsorlarımız", reply_markup=InlineKeyboardMarkup(kb))

async def ban(update, context):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Yetkin yok.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("❗ Lütfen bir mesaja yanıtlayın.")
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text("✅ Kullanıcı banlandı.")

async def unban(update, context):
    if not await is_admin(update, context):
        return
    if not context.args:
        return await update.message.reply_text("/unban USER_ID")
    await context.bot.unban_chat_member(update.effective_chat.id, int(context.args[0]))
    await update.message.reply_text("✅ Ban kaldırıldı.")

async def mute(update, context):
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return await update.message.reply_text("❗ Lütfen bir mesaja yanıtlayın.")
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text("🔇 Kullanıcı susturuldu.")

async def unmute(update, context):
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return await update.message.reply_text("❗ Lütfen bir mesaja yanıtlayın.")
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        ChatPermissions(can_send_messages=True)
    )
    await update.message.reply_text("🔊 Kullanıcı açıldı.")

async def cekilis(update, context):
    cekilis_katilim.clear()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎉 Katılım için tıklayınız", callback_data="katil")]
    ])
    await update.message.reply_text("🎁 Çekiliş başladı!", reply_markup=kb)

async def cekilis_buton(update, context):
    q = update.callback_query
    cekilis_katilim.add(q.from_user.id)
    await q.answer(f"Katılım sayısı: {len(cekilis_katilim)}")

async def sayi(update, context):
    global cekilis_kazanan_sayi
    if context.args:
        cekilis_kazanan_sayi = int(context.args[0])
        await update.message.reply_text(f"🎯 Kazanan sayısı: {cekilis_kazanan_sayi}")

async def bitir(update, context):
    if not cekilis_katilim:
        return await update.message.reply_text("❌ Katılım yok.")
    kazananlar = random.sample(
        list(cekilis_katilim),
        min(cekilis_kazanan_sayi, len(cekilis_katilim))
    )
    await update.message.reply_text(f"🏆 Kazananlar:\n" + "\n".join(map(str, kazananlar)))

async def mesaj(update, context):
    await update.message.reply_text("💬 Mesaj alındı.")

async def kontrol(update, context):
    await update.message.reply_text("✅ Bot aktif.")

async def lock(update, context):
    if await is_admin(update, context):
        await context.bot.set_chat_permissions(update.effective_chat.id, ChatPermissions())
        await update.message.reply_text("🔒 Grup kilitlendi.")

async def unlock(update, context):
    if await is_admin(update, context):
        await context.bot.set_chat_permissions(
            update.effective_chat.id,
            ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text("🔓 Grup açıldı.")

async def add_filter(update, context):
    if not await is_admin(update, context):
        return
    if len(context.args) < 2:
        return await update.message.reply_text("/filter site link")
    SPONSORLAR[context.args[0].lower()] = context.args[1]
    await update.message.reply_text("✅ Site eklendi.")

async def remove_filter(update, context):
    if not await is_admin(update, context):
        return
    if context.args:
        SPONSORLAR.pop(context.args[0].lower(), None)
        await update.message.reply_text("🗑️ Site silindi.")

# ================= CALLBACK =================
async def unmute_button(update, context):
    q = update.callback_query
    uid = int(q.data.split(":")[1])
    await context.bot.restrict_chat_member(
        q.message.chat.id,
        uid,
        ChatPermissions(can_send_messages=True)
    )
    await q.edit_message_text("🔓 Mute kaldırıldı")

# ================= MESSAGE MODERATION =================
async def forward_engel(update, context):
    if not await is_admin(update, context):
        await update.message.delete()

async def site_kontrol(update, context):
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

async def every_kontrol(update, context):
    if update.message.text.lower() == "every":
        kb = [[InlineKeyboardButton("🔥 GİRİŞ", url=l)] for l in EVERY_LINKLER]
        await update.message.reply_text("🔥 Every Siteler", reply_markup=InlineKeyboardMarkup(kb))

async def dogum_kontrol(update, context):
    if update.message.text.lower() == "doğum":
        kb = [[InlineKeyboardButton("🎉 GİRİŞ", url=l)] for l in DOGUM_LINKLERI]
        await update.message.reply_text("🎉 Doğum Günü Bonusları", reply_markup=InlineKeyboardMarkup(kb))

async def kanal_etiket_engel(update, context):
    if re.search(r"@\w+", update.message.text):
        await update.message.delete()
        uid = update.message.from_user.id
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Mute Kaldır", callback_data=f"unmute:{uid}")]
        ])
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            uid,
            ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=1)
        )
        await update.message.reply_text("⛔ Kanal etiketi yasak.", reply_markup=kb)

async def spam_kontrol(update, context):
    uid = update.message.from_user.id
    spam_sayac[uid] = spam_sayac.get(uid, 0) + 1
    if spam_sayac[uid] >= 3:
        spam_sayac[uid] = 0
        await update.message.delete()

async def kufur_kontrol(update, context):
    if any(k in update.message.text.lower() for k in KUFUR_LISTESI):
        await update.message.delete()
        await update.message.reply_text("⚠️ Lütfen küfür etmeyin.")

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

async def mesaj_say(update, context):
    uid = update.message.from_user.id
    mesaj_sayac[uid] = mesaj_sayac.get(uid, 0) + 1

# ================= APP =================
app = ApplicationBuilder().token(TOKEN).build()

# COMMANDS
app.add_handler(CommandHandler("sponsor", sponsor))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("cekilis", cekilis))
app.add_handler(CommandHandler("sayi", sayi))
app.add_handler(CommandHandler("mesaj", mesaj))
app.add_handler(CommandHandler("bitir", bitir))
app.add_handler(CommandHandler("kontrol", kontrol))
app.add_handler(CommandHandler("lock", lock))
app.add_handler(CommandHandler("unlock", unlock))
app.add_handler(CommandHandler("filter", add_filter))
app.add_handler(CommandHandler("remove", remove_filter))

# CALLBACK
app.add_handler(CallbackQueryHandler(cekilis_buton, pattern="^katil$"))
app.add_handler(CallbackQueryHandler(unmute_button, pattern="^unmute:"))

# MESSAGE
app.add_handler(MessageHandler(filters.FORWARDED, forward_engel), group=0)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, site_kontrol), group=1)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, every_kontrol), group=2)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dogum_kontrol), group=3)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kanal_etiket_engel), group=4)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_kontrol), group=5)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kufur_kontrol), group=6)
app.add_handler(MessageHandler(filters.Regex(r"^!sil \d+$"), sil), group=7)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_say), group=8)

print("🔥 BONUSSEMTİ BOT AKTİF")
app.run_polling()
