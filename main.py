# main.py - Render.com uyumlu, Flask'sız, sadece Telegram botu, kanal kontrolü + mesaj silme

import os
import random
import re
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# BOT TOKEN
TOKEN = "8083213548:AAGM1NQ-AzbY_uuQT01nLnGTLx72bDbUTDw"

# ADMIN ID
ADMIN_ID = 8258235296

# ZORUNLU KANAL
KANAL_USERNAME = "@lordsystemv3"
KANAL_LINK = "https://t.me/lordsystemv3"

# Destek hattı
DESTEK_HAT = "@LordDestekHat"

# Kart listesi
kartlar = []
kullanilan_kartlar = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    animasyon = [
        "⚡ LORD LIVE CC SİSTEM AKTİF ⚡",
        f"Hoş geldin {user.first_name} king 👑",
        "Ultra güçlü mod çalışıyor 🔥",
        f"Önce {KANAL_USERNAME} kanalına katılman lazım 💢",
        "Katıldıktan sonra /livecc yaz, canlı kart kap 💳"
    ]

    mesaj = await update.message.reply_text("Sistem yükleniyor... 🚀")
    for text in animasyon:
        await asyncio.sleep(0.8)
        await mesaj.edit_text(text)

    keyboard = [[InlineKeyboardButton("Kanala Katıl 🔥", url=KANAL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Kanala katılmadan devam edemezsin aşkım 😏\nKatıldıktan sonra tekrar /start yaz.", reply_markup=reply_markup)

async def livecc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        chat_member = await context.bot.get_chat_member(chat_id=KANAL_USERNAME, user_id=user_id)
        if chat_member.status in ['left', 'kicked']:
            keyboard = [[InlineKeyboardButton("Kanala Katıl Şimdi 🔥", url=KANAL_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"{KANAL_USERNAME} kanalına katılmadan live CC alamazsın king’im 😔\nKatıl ve tekrar /livecc yaz.", reply_markup=reply_markup)
            return
    except:
        await update.message.reply_text("Kanal kontrolü yapılamadı, lütfen daha sonra dene king’im 😔")
        return

    global kartlar, kullanilan_kartlar

    if not kartlar:
        await update.message.reply_text("Admin henüz live CC yüklemedi aşkım 🥺\nBekle biraz...")
        return

    musait_kartlar = [k for k in kartlar if k not in kullanilan_kartlar]
    if not musait_kartlar:
        await update.message.reply_text("Stokta live kart kalmadı king’im 😔\nAdmin yeniden yüklesin...")
        return

    secilen = random.choice(musait_kartlar)
    kullanilan_kartlar.add(secilen)

    num, exp, cvv = secilen
    metin = f"""🔥 LORD LIVE CC AKTİF 🔥

Numara: {num}
Son Kullanma: {exp}
CVV: {cvv}

Ultra güçlü kart, hemen kullan king 👑
Destek: {DESTEK_HAT}"""

    await update.message.reply_text(metin)

    # Kullanıcının komut mesajını sil (kanalda olmasa da chat'te siler)
    try:
        await update.message.delete()
    except:
        pass

async def admin_yukle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Sadece admin yükleyebilir bebeğim 😏")
        return

    if not update.message.document or not update.message.document.file_name.lower().endswith('.txt'):
        await update.message.reply_text("Sadece .txt dosyası yükle king’im 💚")
        return

    file = await update.message.document.get_file()
    file_path = "live_kartlar.txt"
    await file.download_to_drive(file_path)

    global kartlar
    kartlar = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.search(r'(\d{13,19})[^0-9]*?(\d{1,2})[/\-](\d{2,4})[^0-9]*?(\d{3,4})', line)
            if match:
                num, mm, yy, cvv = match.groups()
                mm = mm.zfill(2)
                yy = yy[-2:] if len(yy) == 4 else yy
                kartlar.append((num, f"{mm}/{yy}", cvv))

    await update.message.reply_text(f"{len(kartlar)} tane live kart yüklendi king’im 👑\nKullanıcılar artık /livecc ile alabilir 🔥")
    os.remove(file_path)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("livecc", livecc))
    app.add_handler(CommandHandler("live", livecc))
    app.add_handler(MessageHandler(filters.Document.ALL & filters.User(user_id=ADMIN_ID), admin_yukle))

    print("Lord Live CC Bot başladı... 🔥")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
