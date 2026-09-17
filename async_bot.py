import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

# هذا الوصف الكامل للبوت
SYSTEM_PROMPT = """
انت مساعد دراسة شاطر من سرمدا - إدلب.
تشرح لكل المواد: رياضيات، فيزياء، كيمياء، عربي، فرنسي، انكليزي، تاريخ، جغرافيا، علوم.
أسلوبك: لهجة سورية بسيطة ومفهومة، صبور، تشجع الطالب.
مهماتك:
1- تشرح الدروس خطوة بخطوة
2- تعمل اختبارات صغيرة
3- تلخص الدروس
4- تساعد بالواجب بس ما تعطي الحل مباشرة، تشرح الطريقة
5- اذا الطالب ما حدد المادة، اسألو شو المادة
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
أهلا وسهلا! أنا بوت سرمدا التعليمي 📚

شو بقدر ساعدك؟

📖 شرح دروس - كل المواد
📝 تلخيص
🧪 اختبارات
✏️ مساعدة بالواجبات

بس قلي: شو المادة وشو الدرس؟ 
مثال: "اشرحلي درس المعادلات رياضيات تاسع"

الأوامر:
/subjects - شو المواد يلي بدرّسها
/help - مساعدة
"""
    await update.message.reply_text(text)

async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("المواد: رياضيات، فيزياء، كيمياء، عربي، فرنسي، انكليزي، تاريخ، جغرافيا، علوم - من الصف السابع للبكالوريا")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب سؤالك مباشرة، مثال: لخصلي درس الثورة الفرنسية، أو حل معي هالمسألة...")

# هون الذكاء - رح نطورو بعدين ب API
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # رد مبدئي ذكي بدون API خارجي
    reply = f"""تمام، سؤالك هو: "{user_text}"

لسا عم أجهز الذكاء الكامل للبوت 🤖

حالياً بقدر ساعدك هيك:
اذا بدك شرح قلي: اشرحلي + اسم الدرس
اذا بدك تلخيص قلي: لخصلي + الدرس
اذا بدك اختبار قلي: عملي اختبار + المادة

قريباً رح أربطو مع ذكاء اصطناعي قوي ويصير يجاوب على كل شي باللهجة السورية!

شو المادة يلي بدك ياها هلق؟"""
    
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Sarmada Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
