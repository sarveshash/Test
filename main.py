import json
import time
import os
import asyncio
from telethon import TelegramClient, events

# --- Bot credentials ---
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7325887777:AAEMq8oIEfLQOx1ErmV7Si196woTMdN93MA"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

path = "/root/genetic_apex_links.json"

# --- Load links from JSON ---
with open(path, "r") as f:
    link_map = json.load(f)

# --- Progress bar helper ---
def make_progress_bar(percent, width=30):
    filled = int(width * percent // 100)
    return f"[{'█' * filled}{'.' * (width - filled)}]"

# --- Download media with shared tracker ---
async def download_media(msg, filename, tracker, progress_message, card_code):
    last_update_time = 0

    def callback(current, total):
        delta = current - tracker["last_current"]
        tracker["downloaded"] += delta
        tracker["last_current"] = current

    async def update_progress():
        percent = (tracker["downloaded"] / tracker["total"]) * 100
        bar = make_progress_bar(percent)
        elapsed = time.time() - tracker["start"]
        speed = tracker["downloaded"] / elapsed if elapsed > 0 else 0
        eta = (tracker["total"] - tracker["downloaded"]) / speed if speed > 0 else 0

        text = (
            f"▶️ Downloading {card_code}\n"
            f"{bar} {percent:5.1f}% | {tracker['downloaded']/1024/1024:.2f}MB / "
            f"{tracker['total']/1024/1024:.2f}MB | {speed/1024/1024:.2f} MB/s | ETA: {int(eta)}s"
        )
        await progress_message.edit(text)

    # Wrap progress callback
    async def progress_wrapper(current, total):
        callback(current, total)
        nonlocal last_update_time
        if time.time() - last_update_time >= 1:
            await update_progress()
            last_update_time = time.time()

    # Start download
    filename = await msg.download_media(file=filename, progress_callback=progress_wrapper)
    return filename

# --- /update command handler ---
@client.on(events.NewMessage(pattern='/update'))
async def update_handler(event):
    await event.reply("📦 Update started... Calculating total size...")

    chat_id = -1002887553673
    os.makedirs("cards", exist_ok=True)

    # --- Step 1: Calculate total size ---
    total_bytes = 0
    messages = []
    for card_code, link in link_map.items():
        msg_id = int(link.split("/")[-1])
        msg = await client.get_messages(chat_id, ids=msg_id)
        if msg and msg.media and msg.file:
            total_bytes += msg.file.size
            messages.append((card_code, msg))
        else:
            print(f"\n⚠️ Message ID {msg_id} has no media or not found.")

    if total_bytes == 0:
        await event.reply("❌ No downloadable media found.")
        return

    # --- Step 2: Initialize shared progress tracker ---
    tracker = {
        "total": total_bytes,
        "downloaded": 0,
        "start": time.time(),
        "last_current": 0
    }

    # --- Create initial progress message ---
    progress_msg = await event.respond("▶️ Starting download...")

    # --- Step 3: Download each file and update cumulative progress ---
    count = 0
    for card_code, msg in messages:
        filename = f"cards/{card_code}.mp4"
        tracker["last_current"] = 0  # Reset before each file
        print(f"\n▶️ Downloading {card_code}")
        await download_media(msg, filename, tracker, progress_msg, card_code)
        count += 1

    await progress_msg.edit(f"✅ All files downloaded.\nTotal: {count} card files.")
    print("\n🎉 All files downloaded.")

# --- Run bot ---
print("🤖 Bot is running... Waiting for /update")
client.run_until_disconnected()
