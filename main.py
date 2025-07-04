import re
import os
from telethon import TelegramClient, events

# --- Bot credentials ---
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7325887777:AAEMq8oIEfLQOx1ErmV7Si196woTMdN93MA"

# --- Start the client session ---
client = TelegramClient("bot_session_cardmsg", api_id, api_hash).start(bot_token=bot_token)

# --- Extract chat ID and message ID from Telegram message link ---
def extract_ids_from_link(link):
    match = re.search(r't\.me/c/(\d+)/(\d+)', link)
    if match:
        chat_id = int("-100" + match.group(1))
        msg_id = int(match.group(2))
        return chat_id, msg_id
    return None, None

# --- Handle /card command ---
@client.on(events.NewMessage(pattern=r"^/card\s+(https://t\.me/c/\d+/\d+)"))
async def card_handler(event):
    try:
        link = event.pattern_match.group(1)
        chat_id, msg_id = extract_ids_from_link(link)

        if not chat_id:
            await event.reply("❌ Invalid link format. Please send a valid t.me/c/... link.")
            return

        # Fetch the original message
        message = await client.get_messages(chat_id, ids=msg_id)

        if not message or not message.media:
            await event.reply("⚠️ That message has no image/media.")
            return

        # Download the image locally
        file_path = await message.download_media(file="card.jpg")

        # Send the image as a photo
        await client.send_file(
            event.chat_id,
            file_path,
            caption="🃏 Here's your card from the message!",
            reply_to=event.id,
            force_document=False  # ✅ Send as photo, not document
        )

        # Optional: delete the file after sending
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await event.reply(f"⚠️ Error: {e}")

# --- Run the bot ---
client.run_until_disconnected()
