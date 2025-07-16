from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from telethon import TelegramClient
import asyncio

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === File paths ===
gif_path = "Butterfree_Gigantamax.gif"
bg_image_path = "IMG_20240713_105340_289_20250717_045940_0000.jpg"
output_path = "output.mp4"

# === Step 1: Generate video ===
bg_clip = ImageClip(bg_image_path).set_duration(5)
gif_clip = VideoFileClip(gif_path).resize(0.5).set_position("center")
final_clip = CompositeVideoClip([bg_clip, gif_clip])
final_clip.write_videofile(output_path, fps=24)

# === Step 2: Send using Telethon ===
async def send_video():
    client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
    async with client:
        await client.send_file('me', output_path, caption="🌟 Here's your generated video!")

asyncio.run(send_video())
