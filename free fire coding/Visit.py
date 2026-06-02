import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Apna BotFather ka token yaha daalo
BOT_TOKEN = "bot-token"
API_TEMPLATE = "https://star-visit-api.vercel.app/{region}/{uid}"
HIT_COUNT = 1  # Kitni baar API hit karni hai

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅ: /visit <region> <uid>")

async def visit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("ᴜsᴀɢᴇ: /visit <region> <uid>")
        return

    region = context.args[0]
    uid = context.args[1]

    # Processing message
    processing_msg = await update.message.reply_text("⏳ 𝙿𝚁𝙾𝙲𝙲𝙴𝚂𝚂𝙸𝙽𝙶....!")

    total_success = 0
    total_failed = 0
    total_visits = 0
    nickname = "Unknown"

    for i in range(HIT_COUNT):
        url = API_TEMPLATE.format(uid=uid, region=region)
        try:
            r = requests.get(url)
            data = r.json()
            total_success += int(data.get("SuccessfulVisits", 0))
            total_failed += int(data.get("FailedVisits", 0))
            total_visits += int(data.get("TotalVisits", 0))
            nickname = data.get("PlayerNickname", nickname)
        except:
            pass

    msg = (
        f"✅ 𝗩𝗜𝗦𝗜𝗧 𝗦𝗘𝗡𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟!\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 𝐍ᴀᴍᴇ: {data.get('nickname', 'Unknown')}\n"
        f"🆔 𝐔ɪᴅ: {data.get('uid', uid)}\n"
        f"🌍 𝐑ᴇɢɪᴏɴ: {data.get('region', region)}\n"
        f"📊 𝐋ᴇᴠᴇʟ: {data.get('level', 0)}\n"
        f"❤ 𝐋ɪᴋᴇꜱ: {data.get('likes', 0)}\n\n"
        f"✅ 𝐒ᴜᴄᴄᴇꜱꜱ: {data.get('success', 0)}\n"
        f"❌ 𝐅ᴀɪʟᴇᴅ: {data.get('fail', 0)}\n"
        f"🎁 𝐓ᴏᴛᴀʟ: 10000\n"
        f"🔴 𝐃ᴀɪʟʏ 𝐔ꜱᴇᴅ: ♾️/♾️\n\n"
        f"👮 𝗢𝗪𝗡𝗘𝗥: @STAR_GMR\n"
        f"🟢 𝗝𝗢𝗜𝗡: @STAR_METHODE"
    )

    # Edit "Processing..." message with final result
    await processing_msg.edit_text(msg)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("visit", visit))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()