import random
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, events, Button

# === Telegram credentials ===
api_id = 27715449
api_hash = "dd3da7c5045f7679ff1f0ed0c82404e0"
bot_token = "7981770051:AAH5isv89k-20WiAXJZwW7hjaG0S6Dvrkdg"

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


# Function to generate image of a bar
def create_bar_image(percent):
    width, height = 400, 100
    bar_width = int((percent / 100) * (width - 40))

    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Draw border
    draw.rectangle([20, 40, width - 20, 70], outline="white", width=2)
    # Draw filled part
    draw.rectangle([20, 40, 20 + bar_width, 70], fill="green")

    # Draw percentage text
    font = ImageFont.truetype("arial.ttf", 30)
    text = f"{percent}%"
    text_w, text_h = draw.textsize(text, font=font)
    draw.text(((width - text_w) / 2, 10), text, fill="white", font=font)

    path = f"/tmp/bar_{percent}.png"
    img.save(path)
    return path


@bot.on(events.NewMessage(pattern='/bar'))
async def send_hp_image(event):
    percent = random.randint(0, 100)
    image_path = create_bar_image(percent)

    await bot.send_file(
        event.chat_id,
        image_path,
        caption=f"📊 {percent}% progress",
        buttons=[[Button.inline("🔁 Recheck", b'recheck')]]
    )


@bot.on(events.CallbackQuery(data=b'recheck'))
async def recheck_handler(event):
    percent = random.randint(0, 100)
    image_path = create_bar_image(percent)

    await event.edit(file=image_path, caption=f"📊 {percent}% progress", buttons=[
        [Button.inline("🔁 Recheck", b'recheck')]
    ])


bot.run_until_disconnected()
