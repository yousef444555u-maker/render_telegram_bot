import asyncio
import logging
import os
import tempfile
import uuid
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل رابط الفيديو من تيك توك أو يوتيوب أو انستا 🎬")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        return

    status = await update.message.reply_text("⏳ جاري التحميل... لا تسكر البوت")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = os.path.join(tmp, f"{uuid.uuid4()}.mp4")
            ydl_opts = {
                "outtmpl": out_path,
                "format": "best[ext=mp4][height<=720]/best",
                "quiet": True,
                "noplaylist": True,
            }

            def dl():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            await asyncio.to_thread(dl)

            files = os.listdir(tmp)
            if not files:
                raise Exception("فشل التحميل")

            video_file = os.path.join(tmp, files[0])

            await status.edit_text("📤 جاري الرفع لتيليجرام...")

            await update.message.reply_video(
                video=open(video_file, "rb"),
                caption="تم التحميل ✅ @yousef_bot"
            )
            await status.delete()

    except Exception as e:
        try:
            await status.edit_text(f"❌ فشل: {str(e)[:200]}")
        except:
            await update.message.reply_text(f"❌ فشل: {str(e)[:200]}")

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing!")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("Bot started polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
