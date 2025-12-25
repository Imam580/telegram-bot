from telegram import Update, ChatPermissions
from telegram.constants import ChatMemberStatus
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters as tg_filters

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")




# --- Filtreler ---
filters_dict = {
    "mekanbahis": "urllink.me/mekanbahis", "betnosa": "urllink.me/betnosa", "babilbet": "urllink.me/babilbet",
    "casibom": "urllink.me/casibom", "lordpalace": "urllink.me/lordpalace", "betwinner": "urllink.me/betwinner",
    "winwin": "urllink.me/winwin", "melbet": "urllink.me/melbet", "grbets": "urllink.me/grbets",
    "betine": "urllink.me/betine", "redfoxbet": "urllink.me/redfoxbet", "bayspin": "urllink.me/bayspin",
    "solobet": "urllink.me/solobet", "betorspin": "urllink.me/betorspin", "antikbet": "urllink.me/antikbet",
    "supertotobet": "urllink.me/supertotobet", "888starz": "urllink.me/888starz", "1king": "urllink.me/1king",
    "mariobet": "urllink.me/mariobet",
    # Shoort.in linkleri (verdiğin tüm linkler)
    "betkom": "shoort.in/betkom", "dodobet": "shoort.in/dodo", "xbahis": "shoort.in/xbahis",
    "mariobonus": "shoort.in/mariobonus", "tarafbet": "shoort.in/tarafbet", "egebet": "shoort.in/egebet",
    "goldenbahis": "shoort.in/goldenbahis", "betigma": "shoort.in/betigma", "nerobet": "shoort.in/nerobet",
    "1kingbonus": "shoort.in/1king", "ngsbahis": "shoort.in/ngsbahis", "gettobet": "shoort.in/gettobet",
    "betrupi": "shoort.in/betrupi", "kingroyal": "shoort.in/kingroyal", "madridbet": "shoort.in/madridbet",
    "meritking": "shoort.in/meritking", "hızlıcasino": "shoort.in/hizlicasino", "winbir": "shoort.in/winbir",
    "heybet": "shoort.in/heybet", "betturkey": "shoort.in/betturkey", "golegol": "shoort.in/golegol",
    "venombet": "shoort.in/venombet", "palazzo": "shoort.in/palazzo", "fixbet": "shoort.in/fixbet",
    "matador": "shoort.in/matador", "zbahis": "shoort.in/zbahis", "mersobahis": "shoort.in/merso",
    "amgbahis": "shoort.in/amg", "saltbahis": "shoort.in/saltbahis", "betorbet": "shoort.in/betorbet",
    "virabet": "shoort.in/virabet", "betlike": "shoort.in/betlike", "betticket": "shoort.in/betticket",
    "bahislion": "shoort.in/bahislion", "lordpalace2": "shoort.in/lordpalace", "betpir": "shoort.in/betpir",
    "gamabet": "shoort.in/gamabet", "otobet": "shoort.in/otobet", "bycasino": "shoort.in/bycasino",
    "bayspinn": "shoort.in/bayspinn", "bahisbudur": "shoort.in/bahisbudur", "ikasbet": "shoort.in/ikasbet",
    "pusulabet": "shoort.in/pusulabet", "starzbet": "shoort.in/starzbet", "ramadabet": "shoort.in/ramadabet",
    "padisahbet": "shoort.in/padisahbet", "casinra": "shoort.in/casinra", "betroz": "shoort.in/betroz",
    "makrobet": "shoort.in/makrobet", "betra": "shoort.in/betra", "netbahis": "shoort.in/netbahis",
    "maksibet": "shoort.in/maksibet", "mercure": "shoort.in/mercure", "rbet": "shoort.in/rbet",
    "favorislot": "shoort.in/favorislot", "pasacasino": "shoort.in/pasacasino", "romabet": "shoort.in/romabet",
    "roketbet": "shoort.in/roketbet", "betgar": "shoort.in/betgar", "pradabet": "shoort.in/pradabet",
    "festwin": "shoort.in/festwin", "casinopark": "shoort.in/casinopark", "yedibahis": "shoort.in/yedibahis",
    "bekabet": "shoort.in/bekabet", "titobet": "shoort.in/titobet", "betci": "shoort.in/betci",
    "betbox": "shoort.in/betbox", "alfabahis": "shoort.in/alfabahis", "hiltonbet": "shoort.in/hiltonbet",
    "baywinn": "shoort.in/baywinn", "betorspinn": "shoort.in/betorspinn", "betinee": "shoort.in/betinee",
    "betist": "shoort.in/betist", "masterbetting": "shoort.in/masterbetting", "betpipo": "shoort.in/betpipo",
    "sahabet": "shoort.in/sahabet", "stake": "shoort.in/stake", "onwin": "shoort.in/onwin",
    "tipobet": "shoort.in/tipobet", "solo": "shoort.in/solo", "supertotobet2": "shoort.in/supertotobet",
    "ligobet": "shoort.in/ligobet", "hilarionbet": "shoort.in/hilarionbet", "dengebet": "shoort.in/dengebet",
    "bahiscom": "shoort.in/bahisbonus", "hitbet": "shoort.in/hitbet", "betoffice": "shoort.in/betoffice",
    "galabet": "shoort.in/galabet", "zenginsin": "shoort.in/zenginsin", "casinowon": "shoort.in/casinowon",
    "tlcasino": "shoort.in/tlcasino", "wbahis": "shoort.in/wbahis", "bahiscasino": "shoort.in/bahiscasino",
    "bethand": "shoort.in/bethandd", "gorabet": "shoort.in/gorabet", "norabahis": "shoort.in/norabahis",
    "xslot": "shoort.in/xslot", "grandpasha": "shoort.in/grandpasha", "spinco": "shoort.in/spinco",
    "superbet": "shoort.in/superbet", "betsin": "shoort.in/betsin", "dedebet": "shoort.in/dedebet",
    "maxwin": "shoort.in/maxwin", "damabet": "shoort.in/damabet", "palacebet": "shoort.in/palacebet",
    "betwoon": "shoort.in/betwoon", "cratosbet": "shoort.in/cratosbet", "betwild": "shoort.in/betwild",
    "pashagaming": "shoort.in/pashagaming", "hızlıbahis": "shoort.in/hızlıbahis", "royalbet": "shoort.in/royalbet",
    "radissonbet": "shoort.in/radissonbet", "betsalvador": "shoort.in/betsalvador", "gobonus": "shoort.in/gobonus",
}

# --- /filtre komutu: tüm filtreleri göster ---
async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    if not filters_dict:
        await update.message.reply_text("⚠️ Hiç filtre yok!")
        return
    mesaj = "📌 Filtreler:\n"
    for key, value in filters_dict.items():
        mesaj += f"- {key} → {value}\n"
    await update.message.reply_text(mesaj)

# --- /removefilter komutu: tek filtreyi sil ---
async def remove_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    if not context.args:
        await update.message.reply_text("❌ Kullanım: /removefilter <filtre_ismi>")
        return
    site_ismi = context.args[0].lower()
    if site_ismi in filters_dict:
        del filters_dict[site_ismi]
        await update.message.reply_text(f"✅ {site_ismi} filtresi kaldırıldı!")
    else:
        await update.message.reply_text(f"❌ {site_ismi} adında bir filtre bulunamadı!")


# --- Yönetici kontrolü ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

# --- /filter ---
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bu komutu sadece yönetici kullanabilir!")
        return
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Kullanım: /filter <site_ismi> <site_linki>")
        return
    site_ismi = context.args[0].lower()
    site_linki = context.args[1]
    filters_dict[site_ismi] = site_linki
    await update.message.reply_text(f"✅ Filtre eklendi: {site_ismi} → {site_linki}")

# --- /lock ve /unlock ---
async def lock_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bu komutu sadece yönetici kullanabilir!")
        return
    await context.bot.set_chat_permissions(update.effective_chat.id, permissions=None)
    await update.message.reply_text("🔒 Kanal kilitlendi!")

async def unlock_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bu komutu sadece yönetici kullanabilir!")
        return
    await context.bot.set_chat_permissions(update.effective_chat.id, permissions=ChatPermissions(can_send_messages=True))
    await update.message.reply_text("🔓 Kanal kilidi açıldı!")

# --- Ban / Unban / Mute / Unmute ---
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    user = None
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif context.args:
        try:
            user_id = int(context.args[0])
            user = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        except:
            await update.message.reply_text("❌ Geçersiz kullanıcı!")
            return
    if not user:
        await update.message.reply_text("❌ Banlamak için birini yanıtlayın veya user_id girin!")
        return
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"🔨 {user.full_name} banlandı!")
    except:
        await update.message.reply_text("❌ Bu kullanıcıyı banlayamadım!")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    if not context.args:
        await update.message.reply_text("❌ Kullanım: /unban <user_id>")
        return
    try:
        user_id = int(context.args[0])
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"✅ {user_id} banı kaldırıldı!")
    except:
        await update.message.reply_text("❌ Bu kullanıcıyı unbanlayamadım!")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    user = None
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    if not user:
        await update.message.reply_text("❌ Susturmak için birini yanıtlayın!")
        return
    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, user.id, permissions=ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"🔇 {user.full_name} susturuldu!")
    except:
        await update.message.reply_text("❌ Bu kullanıcıyı susturamadım!")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    user = None
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    if not user:
        await update.message.reply_text("❌ Konuşturmak için birini yanıtlayın!")
        return
    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, user.id, permissions=ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"🔊 {user.full_name} artık konuşabilir!")
    except:
        await update.message.reply_text("❌ Bu kullanıcıyı konuşturamadım!")

# --- /sil ---
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Sadece yönetici kullanabilir!")
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Kullanım: /sil <adet>")
        return
    count = int(context.args[0])
    messages = await context.bot.get_chat_history(update.effective_chat.id, limit=count)
    for msg in messages:
        try:
            await msg.delete()
        except:
            continue
    await update.message.reply_text(f"🗑️ Son {count} mesaj silindi!")

# --- Mesaj filtreleme ---
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()
        for key, value in filters_dict.items():
            if key in text:
                await update.message.reply_text(value)

# --- Bot başlat ---
app = ApplicationBuilder().token(TOKEN).build()

# --- Handlerlar ---
app.add_handler(CommandHandler("filter", add_filter))
app.add_handler(CommandHandler("lock", lock_channel))
app.add_handler(CommandHandler("unlock", unlock_channel))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("sil", delete_messages))
app.add_handler(MessageHandler(tg_filters.TEXT & ~tg_filters.COMMAND, check_message))
app.add_handler(CommandHandler("filtre", list_filters))
app.add_handler(CommandHandler("removefilter", remove_filter))


print("Bot başlatılıyor...")
app.run_polling()

