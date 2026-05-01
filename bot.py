import telebot
import requests
import time

# မင်းရဲ့ Bot Token အသစ်ကို ဒီမှာ ထည့်ပါ
TOKEN = "8677413305:AAHXOuDcxio0jchySyJPpnCo8FScFXugL4U"
bot = telebot.TeleBot(TOKEN)

# TikTok API Function
def get_tiktok_video(url):
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        res = requests.get(api_url, timeout=15).json()
        if res['code'] == 0:
            return res['data']['play']
        return None
    except:
        return None

# /start command နှိပ်လိုက်ရင် ပြမယ့်စာ
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "Welcome... 👋🤓\n\n"
        "I am a TikTok Downloader Bot.\n"
        "Please send me a **TikTok Video Link** to download without watermark!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# TikTok Link ရောက်လာရင် အလုပ်လုပ်မယ့်အပိုင်း
@bot.message_handler(func=lambda m: m.text and "tiktok.com" in m.text)
def handle_tiktok(message):
    # စောင့်ဆိုင်းရန် စာသားပို့မည်
    waiting_msg = bot.reply_to(message, "⏳ **Logo is being removed... Please wait.**")
    
    video_url = get_tiktok_video(message.text)
    
    if video_url:
        try:
            # Video ကို Caption နဲ့တကွ ပြန်ပို့မည်
            bot.send_video(
                message.chat.id, 
                video_url, 
                caption="✅ **Logo Removed Successfully!**",
                reply_to_message_id=message.message_id
            )
            # စောင့်ခိုင်းထားတဲ့စာကို ဖျက်ပစ်မည်
            bot.delete_message(message.chat.id, waiting_msg.message_id)
        except:
            bot.edit_message_text("❌ **Sorry, something went wrong while sending the video.**", message.chat.id, waiting_msg.message_id)
    else:
        bot.edit_message_text("❌ **Invalid Link or Server Error! Please try again later.**", message.chat.id, waiting_msg.message_id)

# Link မဟုတ်တဲ့ အခြား စာသား/ပုံ/File တွေ ပို့လာရင် ပြန်ပြောမယ့်အပိုင်း
@bot.message_handler(func=lambda m: True)
def handle_others(message):
    bot.reply_to(message, "⚠️ **Please send a valid TikTok video link!** I cannot process other types of messages. 🤓")

# Bot ကို စတင် Run ခြင်း
print("Your Bot is Online now!")
bot.infinity_polling()
￼Enter
