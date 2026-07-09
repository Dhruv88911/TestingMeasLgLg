"""
LYHENG JEWELRY - Gold Price Telegram Bot

Send a price number (e.g. 633) and the bot generates a branded gold price image
with auto-generated date/time, sell price, and buy price (sell - $10).
"""

import os
import logging
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from image_gen import GoldPriceImageGenerator
import config

# ─── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Initialize Image Generator ───────────────────────────────
generator = GoldPriceImageGenerator()


# ─── Command Handlers ─────────────────────────────────────────
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "🟠 *LYHENG JEWELRY - Gold Price Bot*\n\n"
        "ផ្ញើតម្លៃមាស (ឧ. 633) ហើយខ្ញុំនឹងបង្កើតរូបភាពតម្លៃមាស។\n\n"
        "Send me a gold price (e.g. `633`) and I'll generate the price image.\n\n"
        "• លក់ចេញ = your price\n"
        "• ទិញចូល = your price − $10",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        "📖 *How to use:*\n\n"
        "1. Send a number (e.g. `633`)\n"
        "2. Bot generates the gold price image\n"
        "3. លក់ចេញ = 633$, ទិញចូល = 623$\n\n"
        "That's it! 🪙",
        parse_mode="Markdown",
    )


# ─── Message Handlers ─────────────────────────────────────────
async def _generate_and_send_price(update: Update, text: str):
    """Core logic to generate and send the price image."""
    # Try to parse as a number
    try:
        price = int(text)
    except ValueError:
        try:
            price = int(float(text))
        except ValueError:
            # Not a number — tell the user
            await update.message.reply_text("❌ សូមបញ្ចូលលេខត្រឹមត្រូវ។ / Please enter a valid number.")
            return

    # Validate price
    if price <= 0:
        await update.message.reply_text("❌ តម្លៃត្រូវតែជាលេខវិជ្ជមាន។\nPrice must be a positive number.")
        return

    if price <= config.PRICE_GAP:
        await update.message.reply_text(
            f"❌ តម្លៃត្រូវតែធំជាង {config.PRICE_GAP}$។\n"
            f"Price must be greater than ${config.PRICE_GAP}."
        )
        return

    logger.info(f"Generating price image: sell={price}, buy={price - config.PRICE_GAP}")

    try:
        # Generate the image
        image_buffer = generator.generate_bytes(price, fmt="PNG")

        # Get current time for caption
        tz = pytz.timezone(config.TIMEZONE)
        now = datetime.now(tz)
        time_str = now.strftime('%d-%m-%Y %I:%M %p')

        # Send the image without a caption
        buy_price = price - config.PRICE_GAP
        await update.message.reply_photo(
            photo=image_buffer
        )
        
        # Send the text as a separate message
        await update.message.reply_text(
            text=(
                f"🟠 ហាងឆេងមាសនៅពេលនេះ {time_str}\n\n"
                f"លក់ចេញ: {price}$\n"
                f"ទិញចូល: {buy_price}$\n"
        f"\n"
        f"បញ្ចាក់ ហាងឆេងអាចមានការប្រែប្រួល"
            )
        )
        logger.info(f"Price image sent successfully: {price}$ / {buy_price}$")

    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await update.message.reply_text("❌ Error generating image. Please try again.")

async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming price messages (just a number without command)."""
    text = update.message.text.strip()
    
    # If they just send a number, process it.
    # We only process if it looks like a number so we don't reply to random chat.
    try:
        float(text)
    except ValueError:
        return
        
    await _generate_and_send_price(update, text)

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /price command."""
    if not context.args:
        await update.message.reply_text(
            "សូមបញ្ចូលតម្លៃមាសជាមួយពាក្យបញ្ជា។ ឧទាហរណ៍: `/price 633`\n"
            "Please provide a price. Example: `/price 633`",
            parse_mode="Markdown",
        )
        return

    text = context.args[0].strip()
    await _generate_and_send_price(update, text)


# ─── Error Handler ─────────────────────────────────────────────
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error: {context.error}")


# ─── Main ──────────────────────────────────────────────────────
def main():
    """Start the bot."""
    if not config.BOT_TOKEN:
        raise ValueError(
            "❌ BOT_TOKEN not found!\n"
            "Please create a .env file with:\n"
            "  BOT_TOKEN=your_telegram_bot_token_here\n\n"
            "Get a token from @BotFather on Telegram."
        )

    # Build the application
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price))

    # Register error handler
    app.add_error_handler(error_handler)

    # Start polling
    logger.info("🪙 LYHENG JEWELRY Gold Price Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
