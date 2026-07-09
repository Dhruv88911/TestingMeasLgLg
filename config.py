"""
Configuration for LYHENG JEWELRY Gold Price Telegram Bot.
Adjust text positions, font sizes, and colors to match your template.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── Telegram Bot ──────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ─── Timezone ──────────────────────────────────────────────────
TIMEZONE = "Asia/Phnom_Penh"

# ─── Price Settings ────────────────────────────────────────────
PRICE_GAP = 10  # ទិញចូល = លក់ចេញ - PRICE_GAP

# ─── Paths ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "template", "template.png")
FONT_DIR = os.path.join(BASE_DIR, "fonts")
KHMER_FONT_PATH = os.path.join(FONT_DIR, "NotoSansKhmer-Bold.ttf")
PRICE_FONT_PATH = os.path.join(FONT_DIR, "Kaftus.ttf")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# ─── Khmer Text ────────────────────────────────────────────────
# "អត្រាសម្រាប់ថ្ងៃទី" = "Rate for date"
DATE_PREFIX = "\u17a2\u178f\u17d2\u179a\u17b6\u179f\u179f\u17c6\u179a\u17b6\u1794\u17cb\u1790\u17d2\u1784\u17c3\u1791\u17b8"

# ─── Text Positions (x, y) ────────────────────────────────────
# Based on a 1080x1080 template. Adjust to match your template.
# x,y = center point for the text element.
DATE_POSITION = (1350, 650)          # Date/time line (centered horizontally)
SELL_PRICE_POSITION = (750, 1100)    # Center of left price box (លក់ចេញ)
BUY_PRICE_POSITION = (1350, 1100)    # Center of right price box (ទិញចូល)

# ─── Font Sizes ────────────────────────────────────────────────
DATE_FONT_SIZE = 90
PRICE_FONT_SIZE = 170
DOLLAR_FONT_SIZE = 50

# ─── Colors (RGB or Hex) ──────────────────────────────────────
DATE_COLOR = "#debc74"               # Gold
PRICE_COLOR = (0, 0, 0)             # Black
DOLLAR_COLOR = (200, 20, 20)        # Red
