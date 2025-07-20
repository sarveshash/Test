import random, time
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, events, Button

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7325887777:AAEMq8oIEfLQOx1ErmV7Si196woTMdN93MA"

bot = TelegramClient('bvbdbdbot', api_id, api_hash).start(bot_token=bot_token)

# Create image with background + 2 bars + 2 Pokémon
def create_dual_bar_image(p1_percent, p2_percent):
    width, height = 500, 250

    # Load and resize background image
    background = Image.open("bg2.jpg").resize((width, height))
    img = background.copy()
    draw = ImageDraw.Draw(img)

    # Load and resize Pokémon images
    pikachu = Image.open("pikachu.png").resize((100, 100))
    lucario = Image.open("lucario.png").resize((100, 100))

    # Paste Pokémon images
    img.paste(pikachu, (20, 20), pikachu if pikachu.mode == 'RGBA' else None)
    img.paste(lucario, (20, 130), lucario if lucario.mode == 'RGBA' else None)

    # Bar settings
    bar_x = 140
    bar_w = 330
    bar_h = 25

    # Font setup
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    # Function to draw bars
    def draw_bar(y, percent):
        filled = int((percent / 100) * bar_w)
        draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h], outline="white", width=2)
        draw.rectangle([bar_x, y, bar_x + filled, y + bar_h], fill="limegreen")
        draw.text((bar_x + bar_w + 5, y), f"{percent}%", fill="white", font=font)

    # Draw bars for both Pokémon
    draw_bar(50, p1_percent)
    draw_bar(160, p2_percent)

    # Save image
    path = f"battle_{p1_percent}_{p2_percent}.png"
    img.save(path)
    return path


# /bar command: generate and send image with random HPs
@bot.on(events.NewMessage(pattern='/bar'))
async def send_dual_bar_image(event):
    p1 = random.randint(1, 100)
    p2 = random.randint(1, 100) 
    t1=time.time()
    image_path = create_dual_bar_image(p1, p2)
    t2=time.time()
    await event.respond(str(t2-t1)) 
    await bot.send_file(
        event.chat_id,
        image_path,
        buttons=[[Button.inline("🔁 Recheck", b"recheck")]]
    )


# Handle "Recheck" button
@bot.on(events.CallbackQuery(data=b'recheck'))
async def handle_recheck(event):
    p1 = random.randint(1, 100)
    p2 = random.randint(1, 100)
    t1=time.time()
    image_path = create_dual_bar_image(p1, p2)
    t2=time.time()
    await event.respond(str(t2-t1)) 
    await event.edit(
        file=image_path,
        buttons=[[Button.inline("🔁 Recheck", b"recheck")]]
    )


bot.run_until_disconnected()
