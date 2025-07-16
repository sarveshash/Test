from telethon import TelegramClient, events
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image as PILImage
import numpy as np
import uuid
import os

# === Telegram Bot Credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === Files ===
gif_path = "Butterfree_Gigantamax.gif"
bg_image_path = "IMG_20240713_105340_289_20250717_045940_0000.jpg"

# === Initialize Telegram Bot ===
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern="/start"))
async def handler(event):
    await event.respond("🎞 Creating your custom Butterfree video... Please wait.")

    output_path = f"final_{uuid.uuid4().hex[:8]}.mp4"

    try:
        # Load GIF
        gif = VideoFileClip(gif_path)

        # Load background image using Pillow (safe for headless VPS)
        pil_img = PILImage.open(bg_image_path).convert("RGB")
        pil_img = pil_img.resize(gif.size)
        bg_np = np.array(pil_img)
        bg = ImageClip(bg_np).set_duration(gif.duration)

        # Combine background and GIF
        final = CompositeVideoClip([bg, gif.set_position("center")])
        final.write_videofile(output_path, codec="libx264", preset="ultrafast", fps=24, verbose=False, logger=None)

        # Free memory
        gif.close()
        bg.close()
        final.close()

        # Send the result to user
        await bot.send_file(event.chat_id, output_path, caption="✅ Here’s your Butterfree video!")

    except Exception as e:
        await event.respond(f"❌ Error occurred:\n{e}")

    finally:
        # Clean up video file
        if os.path.exists(output_path):
            os.remove(output_path)

print("🤖 Bot is running... Send /start to receive your video.")
bot.run_until_disconnected()
