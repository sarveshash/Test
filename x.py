from telethon.sync import TelegramClient

api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"

client = TelegramClient("user_session", api_id, api_hash)
client.start()  # You'll be prompted for phone number + Telegram code

client.send_file("me", "bg_only.mp4", caption="🎬 Here's your video from VPS.")
print("✅ Sent to your Telegram Saved Messages.")
