import random
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, events, Button

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


# Generate a simple bar image
def create_bar_image(percent):
    width, height = 400, 80
    bar_width = int((percent / 100) * (width - 40))

    img = Image.new("RGB", (width, height), (20, 20, 20))
    draw = ImageDraw.Draw(img)

    # Bar border
    draw.rectangle([20, 30, width - 20, 50], outline="white", width=2)
    # Bar fill
    draw.rectangle([20, 30, 20 + bar_width, 50], fill="limegreen")

    # Percent text
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    text = f"{percent}%"
    text_w, _ = draw.textsize(text, font=font)
    draw.text(((width - text_w) / 2, 5), text, font=font, fill="white")

    path = f"/tmp/bar_{percent}.png"
    img.save(path)
    return path


@bot.on(events.NewMessage(pattern='/bar'))
async def send_bar_image(event):
    percent = random.randint(1, 100)
    image_path = create_bar_image(percent)

    await bot.send_file(
        event.chat_id,
        image_path,
        buttons=[[Button.inline("🔁 Recheck", b"recheck")]]
    )


@bot.on(events.CallbackQuery(data=b"recheck"))
async def handle_recheck(event):
    percent = random.randint(1, 100)
    image_path = create_bar_image(percent)

    await event.edit(file=image_path, buttons=[
        [Button.inline("🔁 Recheck", b"recheck")]
    ])


bot.run_until_disconnected()
