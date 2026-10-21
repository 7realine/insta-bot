import os
import logging
from flask import Flask
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# 1. إعداد سيرفر الويب المصغر لإبقاء البوت مستيقظاً 24/7 على Render
web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get('PORT', 8080))
    web_app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت والقناة
CHANNEL_ID = -1002040431490
CHANNEL_LINK = "https://t.me/w6aqq"
TOKEN = os.getenv("BOT_TOKEN", "8654140402:AAHTKYb_8v3LSs41KqV9rRdVgGO9antu8dM")

# التحقق من اشتراك المستخدم في القناة
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
        "⚠️ **عذراً عزيزي!**\n\nيجب عليك الاشتراك
    
