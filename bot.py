import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8654140402:AAHTKYb_8v3LSs41KqV9rRdVgGO9antu8dM"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" in url:
        await update.message.reply_text("⏳ جاري معالجة الرابط وجلب المحتوى...")
        ydl_opts = {'outtmpl': 'downloaded_media.mp4'}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await update.message.reply_video(video=open('downloaded_media.mp4', 'rb'))
        except Exception as e:
            await update.message.reply_text("عذراً، حدث خطأ أثناء محاولة جلب الفيديو. تأكد أن الرابط عام وصحيح.")
    else:
        await update.message.reply_text("الرجاء إرسال رابط انستغرام صالح.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 البوت يعمل الآن وجاهز لاستقبال الرسائل...")
    application.run_polling()
