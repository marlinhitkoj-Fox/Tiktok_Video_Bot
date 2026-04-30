import os
import asyncio
from pyrogram import Client, filters

# Event Loop error မတက်အောင် ကာကွယ်ခြင်း
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Render ရဲ့ Environment Variables ကနေ ဖတ်မယ်
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "tiktok_bot",
    bot_token=BOT_TOKEN,
    api_id=12345,       # သင့် API ID ထည့်ပါ (နဂိုအတိုင်းထားလဲရသည်)
    api_hash="your_hash" # သင့် API Hash ထည့်ပါ (နဂိုအတိုင်းထားလဲရသည်)
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 **TikTok Video Downloader မှ ကြိုဆိုပါတယ်!**\n\n"
        "TikTok Link ကို ပို့ပေးလိုက်ပါ၊ ကျွန်တော် Watermark ဖျောက်ပြီး ဒေါင်းလုဒ်ဆွဲပေးပါ့မယ်။"
    )

@app.on_message(filters.regex(r'http[s]?://.*tiktok\.com/.*'))
async def handle_tiktok(client, message):
    # ၁။ ခေတ္တစောင့်ဆိုင်းရန် စာသားပို့ခြင်း
    status_msg = await message.reply_text("⏳ **Link ကို စစ်ဆေးနေပါပြီ... Watermark ဖျောက်နေပါသည်၊ ခဏစောင့်ဆိုင်းပေးပါ။**")
    
    try:
        # ဒီနေရာမှာ Video ဒေါင်းတဲ့ Logic ရှိရပါမယ် (ဥပမာ- API တစ်ခုခုသုံးထားတာမျိုး)
        # အခုက စာသားပြင်ချင်တာဆိုတော့ ပြန်ပို့မယ့် Caption ကို အောက်မှာ ပြင်ပေးထားပါတယ်
        
        video_url = "video_file_path" # ဒေါင်းထားတဲ့ video ဖိုင်လမ်းကြောင်း
        
        # ၂။ Video ပြန်ပို့တဲ့အခါ ပါမယ့် စာသား (Caption)
        caption_text = (
            "✅ **Video ဒေါင်းလုဒ်ဆွဲခြင်း အောင်မြင်ပါသည်။**\n\n"
            "✨ __Watermark ဖယ်ရှားပေးထားပြီးပါပြီ။__\n\n"
            "📌 **TikTok Tags:**\n"
            "#TikTokMyanmar #VideoDownloader #NoWatermark #TiktokBot #Myanmar"
        )
        
        # Video ပို့ခြင်း (ဒီနေရာမှာ သင့်ရဲ့ download logic နဲ့ ချိတ်ဆက်ရန်လိုပါသည်)
        # await message.reply_video(video=video_url, caption=caption_text)
        
        # အဆင့် (၁) က စာသားကို ဖျက်ခြင်း
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit(f"❌ အမှားအယွင်းတစ်ခု ရှိသွားပါသည်- {str(e)}")

if __name__ == "__main__":
    app.run()
