from telethon import TelegramClient, events
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# === Bot credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === File paths ===
gif_path = "Butterfree_Gigantamax.gif"  # Make sure this has real transparency
bg_image_path = "IMG_20240713_105340_289_20250717_045940_0000.jpg"
output_path = "output.mp4"

# === Initialize bot ===
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# === On /start command ===
@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    await event.respond("🎥 Please wait while I generate your video...")

    # Step 1: Generate the video
    bg_clip = ImageClip(bg_image_path).set_duration(5)
    gif_clip = VideoFileClip(gif_path, has_mask=True).resize(0.5).set_position("center")
    final_clip = CompositeVideoClip([bg_clip, gif_clip])
    final_clip.write_videofile(output_path, fps=24)

    # Step 2: Send the video
    await bot.send_file(user_id, output_path, caption="🌟 Here's your generated video!")

# === Run bot ===
print("✅ Bot is running. Send /start to trigger video creation.")
bot.run_until_disconnected()
