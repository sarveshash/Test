from telethon import TelegramClient, events
from PIL import Image, ImageDraw
import random
import io

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG-G7QJv-Y"

# === File paths ===
poke1_path = "pikachu.png"
poke2_path = "lucario.png"

# === Create client ===
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# === Resize and place Pokémon ===
def create_battle_image():
    canvas = Image.new("RGBA", (512, 512), (255, 255, 255, 255))

    poke1 = Image.open(poke1_path).convert("RGBA")
    poke2 = Image.open(poke2_path).convert("RGBA")

    # Resize by 70%
    poke1 = poke1.resize((int(poke1.width * 0.7), int(poke1.height * 0.7)))
    poke2 = poke2.resize((int(poke2.width * 0.7), int(poke2.height * 0.7)))

    # Place Pokémon
    canvas.paste(poke1, (0, 0), poke1)
    canvas.paste(poke2, (0, canvas.height - poke2.height), poke2)

    draw = ImageDraw.Draw(canvas)

    # Random HP %s
    hp1 = random.randint(1, 100)
    hp2 = random.randint(1, 100)

    # Draw HP bars
    def draw_bar(x, y, percent, color):
        draw.rectangle([x, y, x + 104, y + 10], fill="grey")  # background
        draw.rectangle([x, y, x + int(104 * percent / 100), y + 10], fill=color)

    draw_bar(canvas.width - 120, 10, hp1, "green")  # Top right
    draw_bar(canvas.width - 120, canvas.height - 20, hp2, "red")  # Bottom right

    output = io.BytesIO()
    canvas.save(output, format='PNG')
    output.name = "battle.png"
    output.seek(0)
    return output

# === Command handler ===
@bot.on(events.NewMessage(pattern="/bar"))
async def send_hp_image(event):
    image_bytes = create_battle_image()
    await bot.send_file(event.chat_id, file=image_bytes, caption="Battle Scene!", force_document=False)

print("Bot is running...")
bot.run_until_disconnected()
