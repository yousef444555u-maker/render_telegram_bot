import asyncio, logging, os, tempfile, uuid
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("أهلا! ارسل رابط الفيديو")

async def download_video(update, context):
    url = update.message.text.strip()
    if not url.startswith("http"):
        return
    msg = await update.message.reply_text("⏳ جاري التحميل...")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, f"{uuid.uuid4()}.mp4")
            opts = {"outtmpl": out, "format": "best[ext=mp4]/best", "quiet": True}
            await asyncio.to_thread(lambda: yt_dlp.YoutubeDL(opts).download([url]))
            files = os.listdir(tmp)
            vf = os.path.join(tmp, files[0])
            await msg.edit_text("📤 جاري الرفع...")
            await update.message.reply_video(video=open(vf, "rb"), caption="تم ✅")
            await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ خطأ: {e}"[:300])

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == "__main__":
    main()
