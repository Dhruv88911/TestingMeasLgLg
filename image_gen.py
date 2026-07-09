"""
Image generator for LYHENG JEWELRY Gold Price updates.
Overlays dynamic text (date, sell price, buy price) onto the template image.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
import os
import io
import config


class GoldPriceImageGenerator:
    """Generates gold price images by overlaying text on a template."""

    def __init__(self):
        # Validate template exists
        if not os.path.exists(config.TEMPLATE_PATH):
            raise FileNotFoundError(
                f"Template image not found at:\n  {config.TEMPLATE_PATH}\n"
                "Please place your template.png in the 'template/' folder."
            )

        # Validate font exists
        if not os.path.exists(config.KHMER_FONT_PATH):
            raise FileNotFoundError(
                f"Font not found at:\n  {config.KHMER_FONT_PATH}\n"
                "Please run 'python setup.py' to download the required fonts."
            )

        # Load template
        self.template = Image.open(config.TEMPLATE_PATH).convert("RGBA")

        # Load fonts
        self.date_font = ImageFont.truetype(config.KHMER_FONT_PATH, config.DATE_FONT_SIZE)
        try:
            self.price_font = ImageFont.truetype(config.PRICE_FONT_PATH, config.PRICE_FONT_SIZE)
            self.dollar_font = ImageFont.truetype(config.PRICE_FONT_PATH, config.DOLLAR_FONT_SIZE)
        except Exception:
            # Fallback to default if Kaftus font is not yet added
            self.price_font = ImageFont.truetype(config.KHMER_FONT_PATH, config.PRICE_FONT_SIZE)
            self.dollar_font = ImageFont.truetype(config.KHMER_FONT_PATH, config.DOLLAR_FONT_SIZE)

    def generate(self, sell_price: int) -> Image.Image:
        """
        Generate a gold price image.

        Args:
            sell_price: The sell price (លក់ចេញ). Buy price = sell_price - PRICE_GAP.

        Returns:
            PIL Image with the prices overlaid on the template.
        """
        buy_price = sell_price - config.PRICE_GAP

        # Create a copy of the template
        img = self.template.copy()
        draw = ImageDraw.Draw(img)

        # ── Date/Time ──────────────────────────────────────────
        tz = pytz.timezone(config.TIMEZONE)
        now = datetime.now(tz)
        date_str = now.strftime('%d-%m-%Y %I:%M %p')

        self._draw_centered_text(
            draw, date_str,
            config.DATE_POSITION,
            self.date_font,
            config.DATE_COLOR
        )

        # ── Sell Price (លក់ចេញ) ────────────────────────────────
        self._draw_price(draw, sell_price, config.SELL_PRICE_POSITION)

        # ── Buy Price (ទិញចូល) ─────────────────────────────────
        self._draw_price(draw, buy_price, config.BUY_PRICE_POSITION)

        # Convert to RGB for saving as JPEG/PNG
        return img.convert("RGB")

    def generate_bytes(self, sell_price: int, fmt: str = "PNG") -> io.BytesIO:
        """
        Generate a gold price image and return as bytes buffer.

        Args:
            sell_price: The sell price.
            fmt: Image format ('PNG' or 'JPEG').

        Returns:
            BytesIO buffer containing the image.
        """
        img = self.generate(sell_price)
        buffer = io.BytesIO()
        img.save(buffer, format=fmt, quality=95)
        buffer.seek(0)
        return buffer

    def _draw_centered_text(self, draw, text, center_pos, font, color):
        """Draw text centered at the given position."""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = center_pos[0] - text_width // 2
        y = center_pos[1] - text_height // 2
        draw.text((x, y), text, fill=color, font=font)

    def _draw_price(self, draw, price, center_pos):
        """Draw a price number centered at the given position."""
        price_str = str(price)

        # Measure text dimensions
        price_bbox = draw.textbbox((0, 0), price_str, font=self.price_font)
        price_width = price_bbox[2] - price_bbox[0]
        price_height = price_bbox[3] - price_bbox[1]

        # Center horizontally and vertically
        x = center_pos[0] - price_width // 2
        y = center_pos[1] - price_height // 2

        # Draw the price number
        draw.text(
            (x, y),
            price_str,
            fill=config.PRICE_COLOR,
            font=self.price_font
        )
