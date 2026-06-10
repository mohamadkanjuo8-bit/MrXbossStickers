os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

STATES = {
    "غاضب": {
        "url": "https://i.imgur.com/JzEEqHQ.jpeg",
        "texts": ["أنا غاضب جداً 😡", "لا تقربني 😡", "اخرج من وجهي 😡"]
    },
    "فرحان": {
        "url": "https://i.imgur.com/WpCKCGj.jpeg",
        "texts": ["اليوم أحلى يوم 😄", "أنا فرحان كتير 😄", "الحياة حلوة 😄"]
    },
    "حزين": {
        "url": "https://i.imgur.com/Gj6CYHT.jpeg",
        "texts": ["قلبي تعبان 😢", "ما في أحد يفهمني 😢", "حياتي صعبة 😢"]
    },
    "متفاجئ": {
        "url": "https://i.imgur.com/Zj6CYHT.jpeg",
        "texts": ["شو هاد؟! 😲", "ما توقعت هيك 😲", "لا صحيح؟! 😲"]
    },
    "نايم": {
        "url": "https://i.imgur.com/Aj6CYHT.jpeg",
        "texts": ["زzzz 😴", "لا تزعجوني 😴", "بدي أنام بس 😴"]
    },
}

user_last = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! 😄\nاكتب: غاضب، فرحان، حزين، متفاجئ، نايم\nأو: غير: نصك هون")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    uid = update.message.from_user.id

    if text.startswith("غير:"):
        new_text = text.replace("غير:", "").strip()
        if uid in user_last:
            await send_img(update, user_last[uid], new_text)
        else:
            await update.message.reply_text("اكتب حالة أول 😄")
        return

    if text in STATES:
        user_last[uid] = text
        t = random.choice(STATES[text]["texts"])
        await send_img(update, text, t)
    else:
        await update.message.reply_text("اكتب: غاضب، فرحان، حزين، متفاجئ، أو نايم 😄")

async def send_img(update, state, text):
    try:
        url = STATES[state]["url"]
        r = requests.get(url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((20, 20), text, fill="white", font=font)
        out = BytesIO()
        img.save(out, format="JPEG")
        out.seek(0)
        await update.message.reply_photo(photo=out)
    except:
        await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
