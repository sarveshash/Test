from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw
import random
import io

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

# === Bot instance ===
app = Client("poke_hp_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# === HP Image Generator ===
def create_hp_image(poke1_path, poke2_path, hp1, hp2):
    # Load and resize Pokémon images (70%)
    poke1 = Image.open(poke1_path).convert("RGBA")
    poke2 = Image.open(poke2_path).convert("RGBA")
    poke1 = poke1.resize((int(poke1.width * 0.7), int(poke1.height * 0.7)))
    poke2 = poke2.resize((int(poke2.width * 0.7), int(poke2.height * 0.7)))

    # Create canvas
    canvas = Image.new("RGBA", (512, 512), (255, 255, 255, 255))

    # Paste Pokémon on canvas
    canvas.paste(poke1, (10, 10), poke1)
    canvas.paste(poke2, (10, canvas.height - poke2.height - 10), poke2)

    # Draw HP bars
    draw = ImageDraw.Draw(canvas)
    bar_width = 150
    bar_height = 15

    def draw_hp_bar(x, y, percent, color):
        # Background bar
        draw.rectangle([x, y, x + bar_width, y + bar_height], fill=(220, 220, 220))
        # Filled HP
        draw.rectangle([x, y, x + int(bar_width * percent / 100), y + bar_height], fill=color)

    # Draw top-right and bottom-right bars
    draw_hp_bar(canvas.width - bar_width - 10, 10, hp1, (0, 255, 0))  # Poke1 HP bar (green)
    draw_hp_bar(canvas.width - bar_width - 10, canvas.height - bar_height - 10, hp2, (255, 0, 0))  # Poke2 HP bar (red)

    # Save image to memory
    img_bytes = io.BytesIO()
    canvas.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# === /bar Command ===
@app.on_message(filters.command("bar"))
async def send_hp_bar(client, message):
    hp1 = random.randint(10, 100)
    hp2 = random.randint(10, 100)
    image = create_hp_image("poke1.png", "poke2.png", hp1, hp2)

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Recheck", callback_data="recheck_hp")]
    ])

    await message.reply_photo(
        photo=image,
        caption=f"Poke1 HP: {hp1}%\nPoke2 HP: {hp2}%",
        reply_markup=markup
    )

# === Callback for 🔁 Recheck ===
@app.on_callback_query(filters.regex("recheck_hp"))
async def refresh_hp_bar(client, callback_query):
    hp1 = random.randint(10, 100)
    hp2 = random.randint(10, 100)
    image = create_hp_image("poke1.png", "poke2.png", hp1, hp2)

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Recheck", callback_data="recheck_hp")]
    ])

    await callback_query.edit_message_media(
        media=("photo", image),
        reply_markup=markup
    )

# === Start the bot ===
app.run()
