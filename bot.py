import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

TOKEN = os.environ.get("BOT_TOKEN")

STATES = {
    "غاضب": ["أنا غاضب جداً 😡", "لا تقربني 😡", "اخرج من وجهي 😡"],
    "فرحان": ["اليوم أحلى يوم 😄", "أنا فرحان كتير 😄", "الحياة حلوة 😄"],
    "حزين": ["قلبي تعبان 😢", "ما في أحد يفهمني 😢", "حياتي صعبة 😢"],
    "متفاجئ": ["شو هاد؟! 😲", "ما توقعت هيك 😲", "لا صحيح؟! 😲"],
    "نايم": ["زzzz 😴", "لا تزعجوني 😴", "بدي أنام بس 😴"],
}

user_last = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! 😄\nاكتب: غاضب، فرحان، حزين، متفاجئ، نايم")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    uid = update.message.from_user.id
    if text.startswith("غير:"):
        new_text = text.replace("غير:", "").strip()
        await update.message.reply_text(new_text)
        return
    if text in STATES:
        user_last[uid] = text
        t = random.choice(STATES[text])
        await update.message.reply_text(t)
    else:
        await update.message.reply_text("اكتب: غاضب، فرحان، حزين، متفاجئ، أو نايم 😄")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
