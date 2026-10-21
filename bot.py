import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

CHANNEL_ID = -1002040431490
CHANNEL_LINK = "https://t.me/w6aqq"

TOKEN = os.getenv("BOT_TOKEN", "8654140402:AAHTKYb_8v3LSs41KqV9rRdVgGO9antu8dM")

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['owner', 'creator', 'administrator', 'member']:
            return True
    except Exception as e:
        logging.error(f"Error checking sub: {e}")
    
    keyboard = [
        [InlineKeyboardButton("📢 إشترك في القناة هنا", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "⚠️ **عذراً عزيزي!**\n\nيجب عليك الاشتراك في قناة البوت أولاً لاستخدام خدمة التحميل.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_sub(update, context):
        await update.message.reply_text("أهلاً بك! أرسل لي أي رابط إنستغرام وسأقوم بتحميله لك فوراً 📥")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        return

    url = update.message.text
    if "instagram.com" not in url:
        await update.message.reply_text("الرجاء إرسال رابط إنستغرام صحيح.")
        return

    msg = await update.message.reply_text("جاري التحميل... ⏳")
    
    # تم تعديل خيارات التحميل لضمان دمج الصوت والفيديو معاً بأعلى جودة
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open('video.mp4', 'rb'))
        await msg.delete()
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')
    except Exception as e:
        await msg.edit_text("حدث خطأ أثناء تحميل الفيديو، تأكد من أن الحساب عام والرابط صحيح.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
    
