# 🪙 LYHENG JEWELRY — Gold Price Telegram Bot

A Telegram bot that generates branded gold price images. Send a sell price and the bot automatically creates an image with:

- **Current date & time** (Phnom Penh timezone)
- **លក់ចេញ** (Sell price) = your input
- **ទិញចូល** (Buy price) = your input − $10

## 📁 Project Structure

```
telegram-gold-bot/
├── bot.py              # Main Telegram bot
├── image_gen.py        # Image generation (Pillow)
├── config.py           # All configuration
├── setup.py            # Font download & setup
├── requirements.txt    # Python dependencies
├── .env                # Your bot token (create from .env.example)
├── .env.example        # Example env file
├── template/
│   └── template.png    # YOUR template image (place here)
├── fonts/
│   └── NotoSansKhmer-Bold.ttf  # Downloaded by setup.py
└── output/             # Generated images (optional)
```

## 🚀 Quick Start

### 1. Get a Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the bot token

### 2. Setup

```bash
# Navigate to the project
cd telegram-gold-bot

# Install dependencies
pip install -r requirements.txt

# Run setup (downloads fonts, creates directories)
python setup.py

# Create your .env file
copy .env.example .env
# Edit .env and paste your bot token
```

### 3. Add Your Template

Place your template image (the blank gold price image **without** the date and prices) at:

```
template/template.png
```

> **Important:** Your template should have blank/empty areas where the date, sell price, and buy price will be placed. The bot overlays text at the positions defined in `config.py`.

### 4. Adjust Text Positions

Open `config.py` and adjust the positions to match your template:

```python
# Text Positions (x, y) — center point for each text element
DATE_POSITION = (540, 383)        # Date/time line
SELL_PRICE_POSITION = (265, 555)  # Left price box (លក់ចេញ)
BUY_PRICE_POSITION = (695, 555)   # Right price box (ទិញចូល)
```

> **Tip:** Use an image editor to find the exact pixel coordinates where text should be centered.

### 5. Run the Bot

```bash
python bot.py
```

### 6. Use the Bot

1. Open your bot in Telegram
2. Send a number like `633`
3. The bot generates and sends the gold price image:
   - លក់ចេញ = 633$
   - ទិញចូល = 623$

## ⚙️ Configuration

All settings are in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `PRICE_GAP` | `10` | Difference between sell and buy price |
| `TIMEZONE` | `Asia/Phnom_Penh` | Timezone for date/time |
| `DATE_FONT_SIZE` | `40` | Font size for the date line |
| `PRICE_FONT_SIZE` | `120` | Font size for price numbers |
| `DOLLAR_FONT_SIZE` | `50` | Font size for the $ sign |
| `DATE_COLOR` | White | Color of the date text |
| `PRICE_COLOR` | Black | Color of price numbers |
| `DOLLAR_COLOR` | Red | Color of the $ sign |

## 🔧 Customizing the Khmer Date Text

The date line prefix is set in `config.py`:

```python
DATE_PREFIX = "\u17a2\u178f\u17d2\u179a\u17b6\u179f..."  # "អorg org org org org org org org org"
```

You can change this to any Khmer text you want. The bot will append the date/time after this prefix.

## 📝 Notes

- The bot responds to **any number** sent as a text message
- Non-numeric messages are silently ignored
- The template image should ideally be **1080x1080** pixels (adjust positions in config if different)
