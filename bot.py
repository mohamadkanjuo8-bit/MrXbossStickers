import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

STATES = {
    "غاضب": {"texts": ["أنا غاضب جداً 😡", "لا تقربني 😡", "اخرج من وجهي 😡"]},
    "فرحان": {"texts": ["اليوم أحلى يوم 😄", "أنا فرحان كتير 😄", "الحياة حلوة 😄"]},
    "حزين": {"texts": ["قلبي تعبان 😢", "ما في أحد يفهمني 😢", "حياتي صعبة 😢"]},
    "متفاجئ": {"texts": ["شو هاد؟! 😲", "ما توقعت هيك 😲", "لا صحيح؟! 😲"]},
    "نايم": {"texts": ["زzzz 😴", "لا تزعجوني 😴", "بدي أنام بس 😴"]},
}

user_last = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! 😄\nاكتب: غاضب، فرحان، حزين، متفاجئ، نايم")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    uid = update.message.from_user.id

    if text.startswith("غير:"):
        new_text = text.replace("غير:", "").strip()
        if uid in user_last:
            t = user_last[uid]
            await update.message.reply_text(f"تم التغيير: {new_text}")
        else:
            await update.message.reply_text("اكتب حالة أول 😄")
        return

    if text in STATES:
        user_last[uid] = text
        t = random.choice(STATES[text]["texts"])
        await update.message.reply_text(t)
    else:
        await update.message.reply_text("اكتب: غاضب، فرحان، حزين، متفاجئ، أو نايم 😄")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
