import logging
import os
import time
from telegram
import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext
import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

Enable logging

logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO ) logger = logging.getLogger(name)

User database to store tracking info

user_data = {} pending_payments = {} admin_id = "@aaysh_912" upi_id = "educationalwork02@oksbi" premium_price = 201

Start command

def get_main_menu(): return InlineKeyboardMarkup([ [ InlineKeyboardButton("Stay on Free Plan", callback_data="stay_free"), InlineKeyboardButton("💎 Upgrade to Premium", callback_data="upgrade_premium") ] ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user user_id = user.id first_name = user.first_name

if user_id in user_data:
    await update.message.reply_text(f"Welcome back, {first_name}! What would you like to do today?")
else:
    user_data[user_id] = {
        "is_premium": False,
        "tracked_ids": []
    }
    await update.message.reply_text(
        f" Hi {first_name}! This bot tracks tweets and sends them here.\n\nYou can track 1 X (Twitter) ID for free.",
        reply_markup=get_main_menu()
    )

Handle callback queries (button clicks)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() user_id = query.from_user.id

if query.data == "stay_free":
    await query.edit_message_text("You are on the Free Plan. Tracking 1 ID only. You can upgrade anytime by typing /upgrade.")

elif query.data == "upgrade_premium":
    pending_payments[user_id] = True
    await query.edit_message_text(
        f"Great choice!\n\nSend ₹{premium_price} to UPI ID: {upi_id}\n\nThen, *reply here with the payment screenshot* (exact image only)."
        f"\n\n Please wait while our admin checks it manually. You'll be upgraded soon.\n\nThanks for supporting us! ",
        parse_mode="Markdown"
    )

Handle screenshots or messages

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user user_id = user.id

if user_id in pending_payments:
    # Forward screenshot and user info to admin
    if update.message.photo:
        caption = f"Payment Screenshot\nFrom: @{user.username or user.first_name}\nUser ID: {user_id}\nName: {user.full_name}"
        photo_file = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=admin_id, photo=photo_file, caption=caption)
        await update.message.reply_text("Screenshot received. Our admin will verify and activate Premium shortly. Please wait... ")
    else:
        await update.message.reply_text("Please send only the *payment screenshot*. Don’t send text or anything else.", parse_mode="Markdown")
else:
    await update.message.reply_text("Please use /start to begin or /upgrade to go premium.")

Upgrade manually by admin

async def make_premium(update: Update, context: ContextTypes.DEFAULT_TYPE): if str(update.effective_user.username) == admin_id.strip("@"):  # Admin check try: target_id = int(context.args[0]) user_data[target_id]["is_premium"] = True await update.message.reply_text(f"✅ User {target_id} upgraded to Premium.") except: await update.message.reply_text("❌ Usage: /makepremium <user_id>") else: await update.message.reply_text("⛔ You are not authorized.")

if name == 'main': TOKEN = os.getenv("BOT_TOKEN")  # Set your bot token as an environment variable application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("upgrade", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(CommandHandler("makepremium", make_premium))
application.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot is running...")
application.run_polling()

