import sys
sys.path.append('/usr/local/lib/python3.10/dist-packages')  # Fix MoviePy import path

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from telethon import TelegramClient
import asyncio

# === MoviePy: Overlay GIF on Image ===
gif_path = "input.gif"         # Replace with your actual GIF file
bg_image_path = "bg.png"       # Replace with your background image
output_video_path = "final.mp4"

# Load GIF and background image
gif = VideoFileClip(gif_path)
bg = ImageClip(bg_image_path).set_duration(gif.duration).resize(gif.size)

# Composite: place GIF centered over background
final = CompositeVideoClip([bg, gif.set_position("center")])
final.write_videofile(output_video_path, codec="libx264", preset="ultrafast", fps=24)

# === Telethon: Send video to your bot with caption /start ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_username = "NintendroTestServerBot"  # Your bot's username without @

client = TelegramClient("user_session", api_id, api_hash)

async def send_video():
    await client.start()
    await client.send_file(bot_username, output_video_path, caption="/start")
    print("✅ Video sent to @NintendroTestServerBot with /start caption.")

asyncio.run(send_video())
