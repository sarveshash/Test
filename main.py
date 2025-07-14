from telethon import TelegramClient, events
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import uuid
import os
import asyncio

# === Bot credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === Static asset paths ===
gif_path = "Butterfree_Gigantamax.gif"
bg_image_path = "xyz.png"

# === Start bot ===
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern="/start"))
async def handler(event):
    await event.respond("🎞 Creating your Butterfree video...")

    # Generate unique output name
    output_path = f"final_{uuid.uuid4().hex[:8]}.mp4"

    try:
        # Load clips
        gif = VideoFileClip(gif_path)
        bg = ImageClip(bg_image_path).set_duration(gif.duration).resize(gif.size)

        # Composite
        final = CompositeVideoClip([bg, gif.set_position("center")])

        # Write video
        final.write_videofile(output_path, codec="libx264", preset="ultrafast", fps=24, verbose=False, logger=None)

        # Close clips to free resources
        gif.close()
        bg.close()
        final.close()

        # Send video
        await bot.send_file(event.chat_id, output_path, caption="Here is your Butterfree video!")

    except Exception as e:
        await event.respond(f"❌ Failed to generate video:\n`{e}`")

    finally:
        # Delete video after sending
        if os.path.exists(output_path):
            os.remove(output_path)

print("🤖 Bot is running. Waiting for /start...")
bot.run_until_disconnected()
