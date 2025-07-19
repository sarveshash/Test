import random
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, events, Button

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

bot = TelegramClient('bvot', api_id, api_hash).start(bot_token=bot_token)


# Create image with 2 bars and 2 Pokémon
def create_dual_bar_image(p1_percent, p2_percent):
    width, height = 500, 250
    img = Image.new("RGB", (width, height), (20, 20, 20))
    draw = ImageDraw.Draw(img)

    # Load Pokémon images
    pikachu = Image.open("pikachu.png").resize((100, 100))
    lucario = Image.open("lucario.png").resize((100, 100))

    img.paste(pikachu, (20, 20))
    img.paste(lucario, (20, 130))

    bar_x = 140
    bar_w = 330
    bar_h = 25

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    def draw_bar(y, percent):
        filled = int((percent / 100) * bar_w)
        draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h], outline="white", width=2)
        draw.rectangle([bar_x, y, bar_x + filled, y + bar_h], fill="limegreen")
        draw.text((bar_x + bar_w + 5, y), f"{percent}%", fill="white", font=font)

    draw_bar(50, p1_percent)
    draw_bar(160, p2_percent)

    path = f"/tmp/battle_{p1_percent}_{p2_percent}.png"
    img.save(path)
    return path


@bot.on(events.NewMessage(pattern='/bar'))
async def send_dual_bar_image(event):
    p1 = random.randint(1, 100)
    p2 = random.randint(1, 100)
    image_path = create_dual_bar_image(p1, p2)

    await bot.send_file(
        event.chat_id,
        image_path,
        
        buttons=[[Button.inline("🔁 Recheck", b"recheck")]]
    )


@bot.on(events.CallbackQuery(data=b'recheck'))
async def handle_recheck(event):
    p1 = random.randint(1, 100)
    p2 = random.randint(1, 100)
    image_path = create_dual_bar_image(p1, p2)



    await event.edit(
        
        image_path,
        
        buttons=[[Button.inline("🔁 Recheck", b"recheck")]]
    )


bot.run_until_disconnected()
