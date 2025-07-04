import json
import time
import os
import asyncio
import random
from telethon import TelegramClient, events

# --- Bot credentials ---
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7325887777:AAEMQ8oIEfLQOx1ErmV7Si196woTM"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Optional path for your JSON file if needed
path = "/storage/emulated/0/genetic_apex_links.json"
if os.path.exists(path):
    with open(path, "r") as f:
        link_map = json.load(f)

# --- Progress bar helper ---
def make_progress_bar(percent, width=50):
    filled = int(width * percent // 100)
    return f"[{'█' * filled}{'.' * (width - filled)}]"

# --- Simulated /simulate download command ---
@client.on(events.NewMessage(pattern='/simulate'))
async def simulate_handler(event):
    total_size_mb = 890.0
    downloaded = 0.0
    start_time = time.time()
    msg = await event.respond("📦 Simulating download of 890MB...")

    def format_status():
        percent = (downloaded / total_size_mb) * 100
        bar = make_progress_bar(percent)
        elapsed = time.time() - start_time
        speed = downloaded / elapsed if elapsed > 0 else 0
        eta = (total_size_mb - downloaded) / speed if speed > 0 else 0
        return (
            f"▶️ Downloading FAKE_FILE.mp4\n"
            f"{bar} {percent:.1f}% | {downloaded:.2f}MB / {total_size_mb:.0f}MB | "
            f"{speed:.2f} MB/s | ETA: {int(eta)}s"
        )

    last_update = 0
    while downloaded < total_size_mb:
        await asyncio.sleep(0.4)
        chunk = random.uniform(2.0, 5.5)  # Simulated realistic speed
        downloaded += chunk
        if downloaded > total_size_mb:
            downloaded = total_size_mb

        if time.time() - last_update >= 1:
            await msg.edit(format_status())
            last_update = time.time()

    await msg.edit("✅ Simulated 890MB file downloaded successfully (showoff complete).")

# --- Run the bot ---
print("🤖 Bot is running... Waiting for commands...")
client.run_until_disconnected()
