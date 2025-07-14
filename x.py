import os
import uuid
import asyncio
import numpy as np
from PIL import Image as PILImage
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from telethon import TelegramClient, events

# === Telegram Bot Credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === File paths ===
gif_path = "Butterfree_Gigantamax.gif"
bg_image_path = "xyz.png"

# === Start Telethon Bot ===
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    await event.respond("✨ Generating your Butterfree video...")

    # Generate a unique video filename
    output_path = f"final_{uuid.uuid4().hex[:8]}.mp4"

    try:
        # Load GIF
        gif = VideoFileClip(gif_path).set_opacity(1)

        # Load background image using PIL (safe for VPS)
        pil_img = PILImage.open(bg_image_path).convert("RGB")
        pil_img = pil_img.resize(gif.size)
        bg_np = np.array(pil_img)

        # Convert background to MoviePy clip
        bg = ImageClip(bg_np).set_duration(gif.duration)

        # Composite final video
        final = CompositeVideoClip([bg, gif.set_position("center")])
        final.write_videofile(output_path, codec="libx264", preset="ultrafast", fps=24, logger=None)

        # Send video to user
        await bot.send_file(event.chat_id, output_path, caption="🎬 Here’s your Butterfree video!")

    except Exception as e:
        await event.respond(f"❌ Error: {e}")

    finally:
        # Clean up video file after sending
        if os.path.exists(output_path):
            os.remove(output_path)

print("🤖 Bot is running. Send /start to generate your video.")
bot.run_until_disconnected()
