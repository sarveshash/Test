from telethon import TelegramClient, events, Button
from PIL import Image, ImageDraw
import io
import random

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === Client setup ===
bot = TelegramClient('poke_hp_bot', api_id, api_hash).start(bot_token=bot_token)

# === Image drawing function ===
def create_hp_image(poke1_path, poke2_path, hp1, hp2):
    # Load images and resize to 70%
    poke1 = Image.open(poke1_path).convert("RGBA")
    poke2 = Image.open(poke2_path).convert("RGBA")
    poke1 = poke1.resize((int(poke1.width * 0.7), int(poke1.height * 0.7)))
    poke2 = poke2.resize((int(poke2.width * 0.7), int(poke2.height * 0.7)))

    # Create canvas
    canvas = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    canvas.paste(poke1, (10, 10), poke1)
    canvas.paste(poke2, (10, canvas.height - poke2.height - 10), poke2)

    # Draw HP bars
    draw = ImageDraw.Draw(canvas)
    bar_width = 150
    bar_height = 15

    def draw_hp_bar(x, y, percent, color):
        draw.rectangle([x, y, x + bar_width, y + bar_height], fill=(220, 220, 220))  # Background
        draw.rectangle([x, y, x + int(bar_width * percent / 100), y + bar_height], fill=color)  # Fill

    draw_hp_bar(canvas.width - bar_width - 10, 10, hp1, (0, 255, 0))  # Pikachu (Top-Right)
    draw_hp_bar(canvas.width - bar_width - 10, canvas.height - bar_height - 10, hp2, (255, 0, 0))  # Lucario (Bottom-Right)

    # Save to BytesIO
    image_stream = io.BytesIO()
    canvas.save(image_stream, format="PNG")
    image_stream.seek(0)
    return image_stream

# === Command: /bar ===
@bot.on(events.NewMessage(pattern='/bar'))
async def send_hp_image(event):
    hp1 = random.randint(10, 100)
    hp2 = random.randint(10, 100)
    image = create_hp_image("pikachu.webp", "lucario.webp", hp1, hp2)

    await bot.send_file(
        event.chat_id,
        file=image,
        caption=f"Pikachu HP: {hp1}%\nLucario HP: {hp2}%",
        buttons=[Button.inline("🔁 Recheck", b"recheck")]
    )

# === Inline callback for "🔁 Recheck" ===
@bot.on(events.CallbackQuery(data=b"recheck"))
async def recheck_hp(event):
    hp1 = random.randint(10, 100)
    hp2 = random.randint(10, 100)
    image = create_hp_image("pikachu.webp", "lucario.webp", hp1, hp2)

    await event.edit(
        file=image,
        text=f"Pikachu HP: {hp1}%\nLucario HP: {hp2}%",
        buttons=[Button.inline("🔁 Recheck", b"recheck")]
    )

# === Start the bot ===
print("Bot is running...")
bot.run_until_disconnected()
