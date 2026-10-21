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
        await update.message.reply_text(
            "أهلاً بك! 📥\n"
            "أرسل لي أي رابط من (إنستغرام، تيك توك، يوتيوب، فيسبوك، تويتر/X) أو رابط ستوري وسأقوم بتحميله لك فوراً!"
        )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        return

    url = update.message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    msg = await update.message.reply_text("جاري التحميل ومعالجة المقطع... ⏳")
    
    # إعدادات شمولية لجميع المنصات والستوريات مع الدمج التلقائي للصوت والصورة
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloaded_media.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',
        'noplaylist': True,
    }

    output_filename = 'downloaded_media.mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # التأكد من الصيغة الناتجة للدمج
            base, _ = os.path.splitext(filename)
            if os.path.exists(base + ".mp4"):
                output_filename = base + ".mp4"
            elif os.path.exists(filename):
                output_filename = filename

        with open(output_filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)
        
        await msg.delete()

    except Exception as e:
        logging.error(f"Download error: {e}")
        await msg.edit_text("حدث خطأ أثناء تحميل المقطع. تأكد من أن الحساب/المحتوى عام والرابط صحيح.")

    finally:
        # تنظيف الملفات المؤقتة بعد إرسالها
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
    
