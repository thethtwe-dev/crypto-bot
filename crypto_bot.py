# Made with love by Thet Htwe [ https://github.com/thethtwe-dev ]

import asyncio
import nest_asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

nest_asyncio.apply()

BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

alerts = {}

def get_crypto_price(symbol):
    try:
        response = requests.get(BINANCE_PRICE_URL, params={"symbol": symbol})
        response.raise_for_status() 
        data = response.json()
        return float(data["price"])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")
        return None

# Function to handle the /price command
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        price = get_crypto_price(symbol)
        if price:
            await update.message.reply_text(f"The current price of {symbol} is {price:.2f} USDT.")
        else:
            await update.message.reply_text("Unable to fetch the price. Please check the symbol and try again.")
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again.")

# Function to handle the /alert command
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        target_price = float(context.args[1])
        comparison = "L" if len(context.args) > 2 and context.args[2].upper() == "L" else "E" if len(context.args) > 2 and context.args[2].upper() == "E" else ">="
        user_id = update.effective_user.id

        # Add the new alert
        if symbol not in alerts:
            alerts[symbol] = []
        alerts[symbol].append({"user_id": user_id, "price": target_price, "comparison": comparison})

        comparison_text = "less than or equal to" if comparison == "L" else "exactly" if comparison == "E" else "greater than or equal to"
        await update.message.reply_text(f"Alert set for {symbol} at {target_price:.2f} USDT ({comparison_text}).")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /alert <symbol> <target_price> [L for lower, E for exact]")

# Function to list all alerts
async def listalerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_alerts = []

    # Collect all alerts for the user
    for symbol, alert_list in alerts.items():
        for alert in alert_list:
            if alert["user_id"] == user_id:
                comparison_text = "<=" if alert["comparison"] == "L" else "==" if alert["comparison"] == "E" else ">="
                user_alerts.append(f"{symbol} at {alert['price']:.2f} USDT (comparison: {comparison_text})")

    if user_alerts:
        await update.message.reply_text("Your active alerts:\n" + "\n".join(user_alerts))
    else:
        await update.message.reply_text("You have no active alerts.")

# Function to stop a specific alert
async def stopalert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        target_price = float(context.args[1])
        comparison = "L" if len(context.args) > 2 and context.args[2].upper() == "L" else "E" if len(context.args) > 2 and context.args[2].upper() == "E" else ">="
        user_id = update.effective_user.id

        if symbol in alerts:
            # Remove the specific alert
            alerts[symbol] = [
                alert for alert in alerts[symbol]
                if not (alert["user_id"] == user_id and alert["price"] == target_price and alert["comparison"] == comparison)
            ]
            # Clean up if no alerts left for the symbol
            if not alerts[symbol]:
                del alerts[symbol]

            comparison_text = "less than or equal to" if comparison == "L" else "exactly" if comparison == "E" else "greater than or equal to"
            await update.message.reply_text(f"Stopped alert for {symbol} at {target_price:.2f} USDT ({comparison_text}).")
        else:
            await update.message.reply_text("No such alert found.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /stopalert <symbol> <target_price> [L for lower, E for exact]")

# Background task to monitor alerts
async def monitor_alerts(application):
    while True:
        for symbol, alert_list in list(alerts.items()):
            current_price = get_crypto_price(symbol)
            if current_price:
                for alert in alert_list[:]:
                    if (
                        (alert["comparison"] == ">=" and current_price >= alert["price"])
                        or (alert["comparison"] == "L" and current_price <= alert["price"])
                        or (alert["comparison"] == "E" and current_price == alert["price"])
                    ):
                        comparison_text = "less than or equal to" if alert["comparison"] == "L" else "exactly" if alert["comparison"] == "E" else "greater than or equal to"
                        await application.bot.send_message(
                            chat_id=alert["user_id"],
                            text=f"🚨 Price Alert! {symbol} has reached {current_price:.2f} USDT ({comparison_text} {alert['price']:.2f} USDT)."
                        )
                        alert_list.remove(alert)
            if not alert_list:
                del alerts[symbol]
        await asyncio.sleep(30)

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Crypto Myanmar Bot!\n\n"
        "Use /price <symbol> to check prices.\n\n"
        "Use /alert <symbol> <target_price> \n[L for lower, E for exact] to set price alerts.\n\n"
        "Use /listalerts to view all your alerts.\n\n"
        "Use /stopalert <symbol> <target_price> \n[L for lower, E for exact] to stop a specific alert.\n\n"
        "Example: /price BTCUSDT\n"
        "Example: /alert BTCUSDT 40000\n"
        "Example: /alert BTCUSDT 40000 L\n"
        "Example: /alert BTCUSDT 40000 E\n\n"
        "www.crypto-myanmar.com"
    )

# Main function to start the bot
async def main():
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("alert", alert))
    application.add_handler(CommandHandler("listalerts", listalerts))
    application.add_handler(CommandHandler("stopalert", stopalert))

    # Start monitoring alerts
    application.create_task(monitor_alerts(application))

    # Run the bot
    print("Bot is running...")
    await application.run_polling()

# Run the bot without asyncio conflicts
if __name__ == "__main__":
    asyncio.run(main())
