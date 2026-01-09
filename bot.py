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
    "mekanbahis": "https://urllink.me/mekanbahis",
    "betnosa": "https://urllink.me/betnosa",
    "babilbet": "https://urllink.me/babilbet",
    "casibom": "https://urllink.me/casibom",
    "lordpalace": "https://urllink.me/lordpalace",
    "betwinner": "https://urllink.me/betwinner",
    "winwin": "https://urllink.me/winwin",
    "melbet": "https://urllink.me/melbet",
    "grbets": "https://urllink.me/grbets",
    "betine": "https://urllink.me/betine",
    "redfoxbet": "https://urllink.me/redfoxbet",
    "bayspin": "https://urllink.me/bayspin",
    "solobet": "https://urllink.me/solobet",
    "betorspin": "https://urllink.me/betorspin",
    "antikbet": "https://urllink.me/antikbet",
    "supertotobet": "https://urllink.me/supertotobet",
    "888starz": "https://urllink.me/888starz",
    "1king": "https://urllink.me/1king",
    "mariobet": "https://urllink.me/mariobet",

    "betkom": "https://shoort.im/betkom",
    "dodobet": "https://shoort.im/dodo",
    "xbahis": "https://shoort.im/xbahis",
    "mariobonus": "https://shoort.im/mariobonus",
    "tarafbet": "https://shoort.im/tarafbet",
    "egebet": "https://shoort.im/egebet",
    "goldenbahis": "https://shoort.im/goldenbahis",
    "betigma": "https://shoort.im/betigma",
    "nerobet": "https://shoort.im/nerobet",
    "1kingbonus": "https://shoort.im/1king",
    "ngsbahis": "https://shoort.im/ngsbahis",
    "gettobet": "https://shoort.im/gettobet",
    "betrupi": "https://shoort.im/betrupi",
    "kingroyal": "https://shoort.im/kingroyal",
    "madridbet": "https://shoort.im/madridbet",
    "meritking": "https://shoort.im/meritking",
    "hızlıcasino": "https://shoort.im/hizlicasino",
    "winbir": "https://shoort.im/winbir",
    "heybet": "https://shoort.im/heybet",
    "betturkey": "https://shoort.im/betturkey",
    "golegol": "https://shoort.im/golegol",
    "venombet": "https://shoort.im/venombet",
    "palazzo": "https://shoort.im/palazzo",
    "fixbet": "https://shoort.im/fixbet",
    "matador": "https://shoort.im/matador",
    "zbahis": "https://shoort.im/zbahis",
    "mersobahis": "https://shoort.im/merso",
    "amgbahis": "https://shoort.im/amg",
    "saltbahis": "https://shoort.im/saltbahis",
    "betorbet": "https://shoort.im/betorbet",
    "virabet": "https://shoort.im/virabet",
    "betlike": "https://shoort.im/betlike",
    "betticket": "https://shoort.im/betticket",
    "bahislion": "https://shoort.im/bahislion",
    "lordpalace2": "https://shoort.im/lordpalace",
    "betpir": "https://shoort.im/betpir",
    "gamabet": "https://shoort.im/gamabet",
    "otobet": "https://shoort.im/otobet",
    "bycasino": "https://shoort.im/bycasino",
    "bayspinn": "https://shoort.im/bayspinn",
    "bahisbudur": "https://shoort.im/bahisbudur",
    "ikasbet": "https://shoort.im/ikasbet",
    "pusulabet": "https://shoort.im/pusulabet",
    "starzbet": "https://shoort.im/starzbet",
    "ramadabet": "https://shoort.im/ramadabet",
    "padisahbet": "https://shoort.im/padisahbet",
    "casinra": "https://shoort.im/casinra",
    "betroz": "https://shoort.im/betroz",
    "makrobet": "https://shoort.im/makrobet",
    "betra": "https://shoort.im/betra",
    "netbahis": "https://shoort.im/netbahis",
    "maksibet": "https://shoort.im/maksibet",
    "mercure": "https://shoort.im/mercure",
    "rbet": "https://shoort.im/rbet",
    "favorislot": "https://shoort.im/favorislot",
    "pasacasino": "https://shoort.im/pasacasino",
    "romabet": "https://shoort.im/romabet",
    "roketbet": "https://shoort.im/roketbet",
    "betgar": "https://shoort.im/betgar",
    "pradabet": "https://shoort.im/pradabet",
    "festwin": "https://shoort.im/festwin",
    "casinopark": "https://shoort.im/casinopark",
    "yedibahis": "https://shoort.im/yedibahis",
    "bekabet": "https://shoort.im/bekabet",
    "titobet": "https://shoort.im/titobet",
    "betci": "https://shoort.im/betci",
    "betbox": "https://shoort.im/betbox",
    "alfabahis": "https://shoort.im/alfabahis",
    "hiltonbet": "https://shoort.im/hiltonbet",
    "baywinn": "https://shoort.im/baywinn",
    "betorspinn": "https://shoort.im/betorspinn",
    "betinee": "https://shoort.im/betinee",
    "betist": "https://shoort.im/betist",
    "masterbetting": "https://shoort.im/masterbetting",
    "betpipo": "https://shoort.im/betpipo",
    "sahabet": "https://shoort.im/sahabet",
    "stake": "https://shoort.im/stake",
    "onwin": "https://shoort.im/onwin",
    "tipobet": "https://shoort.im/tipobet",
    "solo": "https://shoort.im/solo",
    "supertotobet2": "https://shoort.im/supertotobet",
    "ligobet": "https://shoort.im/ligobet",
    "hilarionbet": "https://shoort.im/hilarionbet",
    "dengebet": "https://shoort.im/dengebet",
    "bahiscom": "https://shoort.im/bahisbonus",
    "hitbet": "https://shoort.im/hitbet",
    "betoffice": "https://shoort.im/betoffice",
    "galabet": "https://shoort.im/galabet",
    "zenginsin": "https://shoort.im/zenginsin",
    "casinowon": "https://shoort.im/casinowon",
    "tlcasino": "https://shoort.im/tlcasino",
    "wbahis": "https://shoort.im/wbahis",
    "bahiscasino": "https://shoort.im/bahiscasino",
    "bethand": "https://shoort.im/bethandd",
    "gorabet": "https://shoort.im/gorabet",
    "norabahis": "https://shoort.im/norabahis",
    "xslot": "https://shoort.im/xslot",
    "grandpasha": "https://shoort.im/grandpasha",
    "spinco": "https://shoort.im/spinco",
    "superbet": "https://shoort.im/superbet",
    "betsin": "https://shoort.im/betsin",
    "dedebet": "https://shoort.im/dedebet",
    "maxwin": "https://shoort.im/maxwin",
    "damabet": "https://shoort.im/damabet",
    "palacebet": "https://shoort.im/palacebet",
    "betwoon": "https://shoort.im/betwoon",
    "cratosbet": "https://shoort.im/cratosbet",
    "betwild": "https://shoort.im/betwild",
    "pashagaming": "https://shoort.im/pashagaming",
    "hızlıbahis": "https://shoort.im/hızlıbahis",
    "royalbet": "https://shoort.im/royalbet",
    "radissonbet": "https://shoort.im/radissonbet",
    "betsalvador": "https://shoort.im/betsalvador",
    "gobonus": "https://shoort.im/gobonus",
}

EVERY_SITELER = {
    "HızlıCasino": "https://shoort.im/hizlicasino",
    "Egebet": "https://shoort.im/egebet",
    "Kavbet": "https://shoort.im/kavbet",
    "Pusulabet": "https://shoort.im/pusulabet",
    "Hitbet": "https://shoort.im/hitbet",
    "Artemisbet": "https://shoort.im/artemisbet",

    "SosyalDavet": "https://linkturbo.co/sosyaldavet",
    "MatGuncel": "http://dub.is/matguncel",
    "JojoyaGit": "http://dub.pro/jojoyagit",
    "HoliGuncel": "https://dub.pro/holiguncel",
    "BetsmoveGuncel": "http://dub.is/betsmoveguncel",
    "LunaSosyal": "http://lunalink.org/lunasosyal/",
    "MegaGuncel": "https://dub.is/megaguncel",
    "ZirveGuncel": "https://dub.is/zirveguncel",
    "OdeonGuncel": "http://dub.is/odeonguncel",
    "MaviGuncel": "http://dub.is/maviguncel",
    "SosyalDavet2": "https://linkelit.co/sosyaldavet",

    "Coinbar": "https://shoort.in/coinbar",
    "NakitBahis": "https://shoort.in/nakitbahis",
}


DOGUM_SITELER = {
    "Zbahis": "https://shoort.im/zbahis",
    "Padisahbet": "https://shoort.im/padisahbet",
    "Fixbet": "https://shoort.im/fixbet",
    "Betmatik": "https://shoort.im/betmatik",
    "Bayspinn": "https://shoort.im/bayspinn",
    "Betoffice": "https://shoort.im/betoffice",
    "Betinee": "https://shoort.im/betinee",
    "Xslot": "https://shoort.im/xslot",
    "Starzbet": "https://shoort.im/starzbet",
    "Betpipo": "https://shoort.im/betpipo",
    "Norabahis": "https://shoort.im/norabahis",
    "Spinco": "https://shoort.im/spinco",

    "HermesBet": "https://hermesbet.wiki/telegram",

    "Cratosbet": "https://shoort.im/cratosbet",
    "Betkom": "https://shoort.im/betkom",
    "Masterbetting": "https://shoort.im/masterbetting",
    "MarioBonus": "https://shoort.im/mariobonus",
    "Betwild": "https://shoort.im/betwild",
    "PashaGaming": "https://shoort.im/pashagaming",
    "Royalbet": "https://shoort.im/royalbet",
    "Radissonbet": "https://shoort.im/radissonbet",

    "JojoyaGit": "https://dub.pro/jojoyagit",
    "HoliGuncel": "http://t.t2m.io/holiguncel",

    "Kavbet": "https://shoort.im/kavbet",
    "Betgit": "https://shoort.im/betgit",
    "Madridbet": "https://shoort.im/madridbet",
    "Artemisbet": "https://shoort.im/artemisbet",
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


