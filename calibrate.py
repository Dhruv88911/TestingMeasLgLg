"""
Calibration Script for LYHENG JEWELRY Gold Price Bot.
Draws a grid over your template image to help you find the exact (X, Y) coordinates
for the Date, Sell Price, and Buy Price.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import config

def generate_grid_image():
    if not os.path.exists(config.TEMPLATE_PATH):
        print(f"❌ Template not found at: {config.TEMPLATE_PATH}")
        print("Please add your template first.")
        return

    # Load template
    img = Image.open(config.TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    print(f"📏 Template size: {width}x{height} pixels")

    # Try to load font for coordinates, otherwise use default
    try:
        font = ImageFont.truetype(config.KHMER_FONT_PATH, 16)
    except:
        font = ImageFont.load_default()

    # Draw 50px grid (light)
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 100), width=1)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 100), width=1)

    # Draw 100px grid (solid) with coordinates
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=(0, 255, 255), width=2)
        draw.text((x + 2, 2), str(x), fill=(0, 255, 255), font=font)
        
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=(0, 255, 255), width=2)
        if y > 0:  # Avoid drawing 0 twice
            draw.text((2, y + 2), str(y), fill=(0, 255, 255), font=font)
            
    # Draw crosshairs at current config positions
    def draw_crosshair(pos, color, label):
        x, y = pos
        s = 20
        draw.line([(x-s, y), (x+s, y)], fill=color, width=3)
        draw.line([(x, y-s), (x, y+s)], fill=color, width=3)
        draw.text((x+5, y+5), f"{label} {pos}", fill=color, font=font)

    draw_crosshair(config.DATE_POSITION, (255, 0, 0), "DATE")
    draw_crosshair(config.SELL_PRICE_POSITION, (0, 255, 0), "SELL")
    draw_crosshair(config.BUY_PRICE_POSITION, (0, 0, 255), "BUY")

    # Save
    output_path = os.path.join(config.OUTPUT_DIR, "calibration_grid.png")
    img.save(output_path)
    print(f"✅ Calibration image saved to: {output_path}")
    print("Open this image to find the exact X,Y coordinates for your text!")

if __name__ == "__main__":
    generate_grid_image()
