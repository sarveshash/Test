from telethon.sync import TelegramClient

api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# Start client
bot = TelegramClient("send_to_me", api_id, api_hash).start(bot_token=bot_token)

# Send to your Saved Messages
bot.send_file("me", "bg_only.mp4", caption="🎬 Here's your generated video.")
print("✅ Sent to your Telegram Saved Messages.")
