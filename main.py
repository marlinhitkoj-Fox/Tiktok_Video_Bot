import os
import yt_dlp
from pyrogram import Client, filters

# Environment Variables ယူခြင်း
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("tt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start command အတွက်
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 **Welcome to TikTok Downloader!**\n\nJust send me a TikTok link and I will send you the video without watermark.")

# TikTok link လက်ခံခြင်း
@app.on_message(filters.regex(r'https?://.*tiktok\.com/.*'))
async def tiktok_dl(client, message):
    url = message.text
    # "⌛ Removing Logo... Please wait" ဆိုတဲ့ စာသား အရင်ပို့မယ်
    status_msg = await message.reply("⌛ **Removing Logo... Please wait.**")
    
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'No Title') # Video ရဲ့ Title ကို ယူခြင်း
            
        # ဗီဒီယို ပို့မယ် (Caption ထဲမှာ Title နဲ့ အောင်မြင်ကြောင်း စာပါမယ်)
        await message.reply_video(
            video_url, 
            caption=f"🎬 **{title}**\n\n✅ **Logo Removed Successfully!**"
        )
        
        # "Removing Logo" ဆိုတဲ့ စာတိုလေးကို ပြန်ဖျက်လိုက်မယ်
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit(f"❌ **Error:** Link is invalid or server is down.")

app.run()
