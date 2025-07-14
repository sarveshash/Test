from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from telethon import TelegramClient
import asyncio

# ========== STEP 1: PROCESS THE GIF ON IMAGE ==========

gif_path = "Butterfree_Gigantamax.gif"
bg_image_path = "xyz.png"
output_video_path = "final.mp4"

# Load GIF and background image
gif = VideoFileClip(gif_path)
bg = ImageClip(bg_image_path).set_duration(gif.duration)

# Resize background to match GIF size (optional)
bg = bg.resize(gif.size)

# Composite: GIF on top of image
final = CompositeVideoClip([bg, gif.set_position("center")])
final.write_videofile(output_video_path, codec="libx264", preset="ultrafast", fps=24)

# ========== STEP 2: SEND VIDEO TO BOT ON /start ==========

# Your Telegram API credentials (user account)
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_username = "NintendroTestServerBot"  # Replace with your actual bot username (without @)

client = TelegramClient("user_session", api_id, api_hash)

async def send_video():
    await client.start()
    await client.send_file(bot_username, output_video_path, caption="/start")
    print("✅ Video sent to bot with /start")

asyncio.run(send_video())
