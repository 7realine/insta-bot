import os
import telebot
import yt_dlp

# 1. توكن البوت
TOKEN = os.getenv('BOT_TOKEN', 'هنا_ضع_توكن_البوت')
bot = telebot.TeleBot(TOKEN)

# 2. أمر البداية /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "أهلاً بك يا غالي في بوت التحميل الشامل (الستوريات والريلز) 🚀\n\n"
        "أرسل لي الآن أي رابط (إنستغرام ستوري أو ريلز، فيسبوك، تيك توك، أو سناب شات) وسأقوم بتحميله وإرساله لك فوراً ⚡"
    )
    bot.reply_to(message, welcome_text)

# 3. استقبال ومعالجة الروابط وتحميلها
@bot.message_handler(func=lambda message: True)
def handle_links(message):
    url = message.text.strip()
    
    # التأكد من أن الرابط يتبع لإحدى المنصات المدعومة
    if any(domain in url for domain in ["instagram.com", "facebook.com", "tiktok.com", "snapchat.com"]):
        sent_msg = bot.reply_to(message, "⏳ جاري تحميل الملف (سواء ستوري أو فيديو)، انتظر لحظات...")
        
        filename = None
        try:
            # إعدادات yt-dlp للتعامل مع الستوريات والفيديوهات
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_media.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            bot.edit_message_text(
                "✅ تم التحميل بنجاح، جاري إرسال الملف...", 
                chat_id=message.chat.id, 
                message_id=sent_msg.message_id
            )
            
            with open(filename, 'rb') as media_file:
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    bot.send_photo(message.chat.id, media_file, caption="تم التحميل بواسطة البوت 📥")
                else:
                    bot.send_video(message.chat.id, media_file, caption="تم التحميل بواسطة البوت 📥")
            
            # تنظيف الملف من السيرفر
            if filename and os.path.exists(filename):
                os.remove(filename)
                
        except Exception as e:
            if filename and os.path.exists(filename):
                try:
                    os.remove(filename)
                except:
                    pass
                    
            bot.edit_message_text(
                "❌ عذراً، لم أتمكن من تحميل هذا الرابط. قد يكون الحساب خاصاً أو الستوري منتهياً.", 
                chat_id=message.chat.id, 
                message_id=sent_msg.message_id
            )
            
    else:
        bot.reply_to(message, "⚠️ الرابط غير مدعوم. يرجى إرسال رابط صالح من إنستغرام، فيسبوك، تيك توك، أو سناب شات.")

# تشغيل البوت
print("Bot is running with yt-dlp...")
bot.infinity_polling()
