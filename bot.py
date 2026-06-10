import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

STATES = {
    "غاضب": {
        "urls": [
            "https://i.imgur.com/angry1.jpg",
            "https://i.imgur.com/angry2.jpg",
        ],
        "texts": ["أنا غاضب جداً 😡", "لا تقربني هلق 😡", "اخرج من وجهي 😡"]
    },
    "فرحان": {
        "urls": [
            "https://i.imgur.com/happy1.jpg",
            "https://i.imgur.com/happy2.jpg",
        ],
        "texts": ["اليوم أحلى يوم 😄", "أنا فرحان كتير 😄", "الحياة حلوة 😄"]
    },
    "حزين": {
        "urls": [
            "https://i.imgur.com/sad1.jpg",
            "https://i.imgur.com/sad2.jpg",
        ],
        "texts": ["قلبي تعبان 😢", "ما في أحد يفهمني 😢", "حياتي صعبة 😢"]
    },
    "متفاجئ": {
        "urls": [
            "https://i.imgur.com/surprised1.jpg",
            "https://i.imgur.com/surprised2.jpg",
        ],
        "texts": ["شو هاد؟! 😲", "ما توقعت هيك 😲", "لا صحيح؟! 😲"]
    },
    "نايم": {
        "urls": [
            "https://i.imgur.com/sleep1.jpg",
            "https://i.imgur.com/sleep2.jpg",
        ],
        "texts": ["زzzz 😴", "لا تزعجوني 😴", "بدي أنام بس 😴"]
    },
}

user_last_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً! 😄\nاكتب حالتك مثلاً:\nغاضب، فرحان، حزين، متفاجئ، نايم\n\nأو اكتب 'غير: نصك هون' لتغيير الكتابة"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.message.from_user.id

    if text.startswith("غير:"):
        new_text = text.replace("غير:", "").strip()
        if user_id in user_last_state:
            state = user_last_state[user_id]
            await send_image_with_text(update, state, new_text)
        else:
            await update.message.reply_text("اكتب حالة أول مثلاً: غاضب 😄")
        return

    if text in STATES:
        user_last_state[user_id] = text
        auto_text = random.choice(STATES[text]["texts"])
        await send_image_with_text(update, text, auto_text)
    else:
        await update.message.reply_text("اكتب: غاضب، فرحان، حزين، متفاجئ، أو نايم 😄")

async def send_image_with_text(update, state, text):
    url = random.choice(STATES[state]["urls"])
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((20, 20), text, fill="white", font=font)
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    await update.message.reply_photo(photo=output)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
