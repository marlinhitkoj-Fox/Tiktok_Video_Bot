import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

# Render ရဲ့ Python Asyncio ပြဿနာကို ဖြေရှင်းခြင်း
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Render Environment Variables ထဲကနေ တန်ဖိုးတွေယူမယ်
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Bot Setup
app = Client(
    "tiktok_bot",
    bot_token=BOT_TOKEN,
    api_id=27521016, 
    api_hash="96c4a8549929f1092500057088713063"
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 **TikTok Video Downloader မှ ကြိုဆိုပါတယ်!**\n\n"
        "TikTok Link ကို ပို့ပေးလိုက်ပါ၊ ကျွန်တော် Watermark ဖျောက်ပြီး ဒေါင်းလုဒ်ဆွဲပေးပါ့မယ်။"
    )

@app.on_message(filters.regex(r'http[s]?://.*tiktok\.com/.*'))
async def handle_tiktok(client, message):
    # ၁။ စတင်တုံ့ပြန်သည့် စာသား
    status_msg = await message.reply_text("⏳ **Link ကို စစ်ဆေးနေပါပြီ... Watermark ဖျောက်နေပါသည်၊ ခဏစောင့်ဆိုင်းပေးပါ။**")
    
    url = message.text
    video_file = f"video_{message.from_user.id}.mp4"

    # TikTok ဒေါင်းလုဒ်ဆွဲရန် Setting များ
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': video_file,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # ၂။ Video ကို ဒေါင်းလုဒ်ဆွဲခြင်း
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'TikTok Video')
            nickname = info.get('uploader', 'Unknown User')

        # ၃။ ပြန်ပို့မည့် Caption စာသား (Hashtag များအပါအဝင်)
        caption_text = (
            f"✅ **ဒေါင်းလုဒ်ဆွဲခြင်း အောင်မြင်ပါသည်။**\n\n"
            f"📝 **Title:** {title}\n"
            f"👤 **Uploader:** @{nickname}\n\n"
            f"✨ __Watermark ဖယ်ရှားပေးထားပြီးပါပြီ။__\n\n"
            f"📌 #TikTokMyanmar #NoWatermark #TiktokDownloader #MyanmarBot #Trending"
        )

        # ၄။ Video ကို ပြန်ပို့ပြီး status message ကို ဖျက်ခြင်း
        await message.reply_video(video=video_file, caption=caption_text)
        await status_msg.delete()
        
        # ၅။ Server ပေါ်မှာ နေရာမရှုပ်အောင် ဖိုင်ကို ပြန်ဖျက်ခြင်း
        if os.path.exists(video_file):
            os.remove(video_file)

    except Exception as e:
        await status_msg.edit(f"❌ **အမှားအယွင်းတစ်ခု ရှိသွားပါသည်-** \n\n`{str(e)}` \n\nLink မှန်မမှန် ပြန်စစ်ပေးပါ။")

if __name__ == "__main__":
    app.run()
