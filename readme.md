# Crypto Price Alert Bot

A Telegram bot that allows users to track cryptocurrency prices and set price alerts. Users can track price increases, decreases, and exact price matches. Supports multiple cryptocurrencies via the Binance API.

---

## 🚀 Features

- Track live cryptocurrency prices.
- Set alerts for:
  - **Price Decreases (`L`)**.
  - **Exact Matches (`E`)**.
- Manage alerts: list and stop specific alerts.
- User-friendly commands.

---

## 🛠 Installation

Follow these steps to install and run the bot on your server:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/crypto-price-alert-bot.git
cd crypto-price-alert-bot
```
## 2. Set Up Python Environment
Ensure Python 3.8+ is installed on your system. Then, install the required libraries:
```bash
pip install -r requirements.txt
```
### 3. Edit Bot Configuration
Update the bot token in the crypto_bot.py file:

##### application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
##### Replace {YOUR_TELEGRAM_BOT_TOKEN} with your Telegram bot token obtained from BotFather.

### 4. Run the Bot
Start the bot using:
```bash
python3 crypto_bot.py
```
### 5. Interacting with the Bot
Use the /start command to begin.

Set alerts using /alert <symbol> <price> [L/E].

Example: /alert BTCUSDT 40000 (price >= 40000).

Example: /alert BTCUSDT 40000 L (price <= 40000).

Example: /alert BTCUSDT 40000 E (price == 40000).

View all active alerts with /listalerts.

Stop a specific alert using /stopalert <symbol> <price> [L/E].

## Commands

| Command             | Description                                                                |
| ----------------- | ------------------------------------------------------------------ |
| `/start` | Start interacting with the bot.|
| `/price <symbol>` | Check the live price of a cryptocurrency (e.g., BTCUSDT). |
| `/alert` | Set a price alert (L, E). |
| `/listalerts` | View all your active alerts. |
| `/stopalert` | Stop a specific alert by symbol and price. |

