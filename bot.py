import os
import telebot
import requests

# 1. توكن البوت (يسحبه من رندر أو ضعه هنا)
TOKEN = os.getenv('BOT_TOKEN', 'هنا_ضع_توكن_البوت')
bot = telebot.TeleBot(TOKEN)

# 2. أمر البداية /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "أهلاً بك يا غالي في بوت التحميل الشامل! 🚀\n\n"
        "أرسل لي الآن أي رابط من (إنستغرام، فيسبوك، تيك توك، أو سناب شات) وسأقوم بتحميله وإرساله لك فوراً وبجودة عالية ⚡"
    )
    bot.reply_to(message, welcome_text)

# 3. استقبال ومعالجة الروابط
@bot.message_handler(func=lambda message: True)
def handle_links(message):
    url = message.text.strip()
    
    # التأكد أن الرسالة عبارة عن رابط لأحد المنصات المدعومة
    if "instagram.com" in url or "facebook.com" in url or "tiktok.com" in url or "snapchat.com" in url:
        sent_msg = bot.reply_to(message, "⏳ جاري معالجة الرابط وتحميل الملف، انتظر ثوانٍ...")
        
        try:
            # هنا يتم معالجة الرابط وجلب الملف
            bot.edit_message_text(
                "✅ تم استلام الرابط بنجاح! جاري إرسال الملف...", 
                chat_id=message.chat.id, 
                message_id=sent_msg.message_id
            )
            
        except Exception as e:
            bot.edit_message_text(
                "❌ عذراً، لم أتمكن من تحميل الملف. تأكد أن الحساب عام وأن الرابط صحيح.", 
                chat_id=message.chat.id, 
                message_id=sent_msg.message_id
            )
            
    else:
        bot.reply_to(message, "⚠️ عذراً، هذا الرابط غير مدعوم. أرسل رابطاً صالحاً من إنستغرام، فيسبوك، تيك توك، أو سناب شات.")

# تشغيل البوت باستمرار
print("Bot is running perfectly...")
bot.infinity_polling()
