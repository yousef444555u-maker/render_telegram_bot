import asyncio, logging, os, re, tempfile, uuid
from urllib.parse import urlparse
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود!")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا! أرسل رابط الفيديو (m3u8, mp4, hls, youtube...) وأنا أحمله لك 🎬")
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("أرسل رابط صحيح يبدأ بـ http")
        return
    status_msg = await update.message.reply_text("⏳ جاري التحميل...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, f"{uuid.uuid4()}.mp4")
            ydl_opts = {'outtmpl': output_path,'format': 'best[ext=mp4]/best','merge_output_format': 'mp4','quiet': True,'no_warnings': True,'http_headers': {'User-Agent': 'Mozilla/5.0'}}
            def run_download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            await asyncio.to_thread(run_download)
            files = os.listdir(tmpdir)
            if not files:
                raise Exception("فشل التحميل")
            video_file = os.path.join(tmpdir, files[0])
            await status_msg.edit_text("📤 جاري الرفع...")
            await update.message.reply_video(video=open(video_file, 'rb'), caption="تم ✅", supports_streaming=True)
            await status_msg.delete()
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text(f"❌ فشل: {str(e)[:200]}")
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
if __name__ == "__main__":
    main()
