from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
from datetime import datetime
import pytz

# ================== BOT TOKEN ==================
TOKEN = "8533506276:AAEwW3k2fLVKMycFnzsgqJ5xEEAqpAq_ZS8"
# ===============================================

# -------- CONSTANTS --------
BIG_IMAGE = "https://files.catbox.moe/uza111.jpg"
SMALL_IMAGE = "https://files.catbox.moe/cf1lm0.jpg"

GOGO_STICKER_ID = "CAACAgUAAxkBAAFA6_BpboDGF4FZLIhGLMvug-cRmV6YMAACUgMAAtKqAVVNzYqUuDTsQjgE"

REGISTER_LINK = "https://www.tsgame2026.pro/#/register?invitationCode=47222117237"
CHANNEL_LINK = "https://t.me/+WPMYE2ABsIVhZjM1"

# -------- LAST PERIOD TRACK --------
last_sent_period = None

# -------- WINGO 1-MIN PERIOD LOGIC (EXACT LIKE APP) --------
def generate_wingo_period():
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)

    seconds = now.second
    minutes = now.minute
    hours = now.hour

    total_minutes = hours * 60 + minutes

    date_part = now.strftime("%Y%m%d")

    # 🔥 CORRECT BASE (MATCHING YOUR GAME)
    base = 11177 + total_minutes

    period = f"{date_part}1000{base}"
    return period, seconds
# ---------------- /start COMMAND ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name  # Auto user name

    keyboard = [
        ["🔮 Get Prediction"],
        ["🔗 Register Link", "📢 Prediction Channel"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        f"✨ Welcome, {user_name}! ✨\nPlease select an option below:",
        reply_markup=reply_markup
    )

# ---------------- GET PREDICTION HANDLER ----------------
async def handle_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_sent_period

    period, seconds = generate_wingo_period()

    # If same period already sent → wait
    if last_sent_period == period:
        remaining = 60 - seconds
        await update.message.reply_text(
            f"⏳ Wait for next period...\nNext prediction in {remaining} seconds."
        )
        return

    # New period → allow prediction
    last_sent_period = period

    # Random prediction
    big_small = random.choice(["Big", "Small"])
    colour = random.choice(["Green", "Red", "Violet"])
    numbers = random.choice([
        "0 or 5",
        "1 or 6",
        "2 or 7",
        "3 or 8",
        "4 or 9"
    ])

    # Send Big / Small image
    if big_small == "Big":
        await update.message.reply_photo(photo=BIG_IMAGE)
    else:
        await update.message.reply_photo(photo=SMALL_IMAGE)

    # Send prediction text
    message = f"""
🎰 Prediction for WinGO 1 MIN 🎰

📅 Period: {period}
🛒 Purchase: {big_small}

⚠️ Risky Predictions:
👉 Colour: {colour}
👉 Numbers: {numbers}

💡 Strategy Tip:
Use the 2x strategy for better chances of profit and winning.

📊 Fund Management:
Always play through fund management 5 level.

⏱️ This prediction is valid for the NEXT 1 minute only.
"""

    await update.message.reply_text(message)

    # Send GoGo sticker
    await update.message.reply_sticker(sticker=GOGO_STICKER_ID)

# ---------------- REGISTER LINK HANDLER ----------------
async def handle_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔗 Register here:\n{REGISTER_LINK}"
    )

# ---------------- CHANNEL LINK HANDLER ----------------
async def handle_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📢 Join Prediction Channel:\n{CHANNEL_LINK}"
    )

# ---------------- BOT SETUP ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

# Reply keyboard button handlers
app.add_handler(MessageHandler(filters.Regex("^🔮 Get Prediction$"), handle_prediction))
app.add_handler(MessageHandler(filters.Regex("^🔗 Register Link$"), handle_register))
app.add_handler(MessageHandler(filters.Regex("^📢 Prediction Channel$"), handle_channel))

print("🤖 Bot is running with full 1-minute Wingo system...")
app.run_polling()