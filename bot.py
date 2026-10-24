import os
import telebot
import requests

# 1. توكن البوت
TOKEN = os.getenv('BOT_TOKEN', 'هنا_ضع_توكن_البوت')
bot = telebot.TeleBot(TOKEN)

# 2. أمر البداية /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "أهلاً بك يا غالي في بوت التحميل الشامل! 🚀\n\n"
        "أرسل لي الآن أي رابط (إنستغرام، فيسبوك، تيك توك، أو سناب شات) وسأقوم بتحميله وإرساله لك فوراً ⚡"
    )
    bot.reply_to(message, welcome_text)

# 3. استقبال ومعالجة الروابط وتحميلها
@bot.message_handler(func=lambda message: True)
def handle_links(message):
    url = message.text.strip()
    
    # التأكد من أن الرابط يتبع لإحدى المنصات المدعومة
    if "instagram.com" in url or "facebook.com" in url or "tiktok.com" in url or "snapchat.com" in url:
        sent_msg = bot.reply_to(message, "⏳ جاري جلب الملف، يرجى الانتظار...")
        
        try:
            # استخدام API موثوق وسريع للتحميل
            api_url = "https://api.cobalt.tools/api/json"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "url": url
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            res_data = response.json()
            
            status = res_data.get("status")
            
            if status in ["stream", "redirect"]:
                media_url = res_data.get("url")
                bot.edit_message_text(
                    "✅ تم التحميل بنجاح، جاري إرسال الملف...", 
                    chat_id=message.chat.id, 
                    message_id=sent_msg.message_id
                )
                bot.send_video(message.chat.id, media_url, caption="تم التحميل بواسطة البوت 📥")
                
            elif status == "picker":
                media_url = res_data["picker"][0]["url"]
                bot.edit_message_text(
                    "✅ تم التحميل بنجاح، جاري إرسال الملف...", 
                    chat_id=message.chat.id, 
                    message_id=sent_msg.message_id
                )
                
