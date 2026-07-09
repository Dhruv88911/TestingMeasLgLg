"""
Setup script to download the required Noto Sans Khmer font from Google Fonts.
Run this once before starting the bot: python setup.py
"""

import os
import urllib.request
import sys

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# Noto Sans Khmer Bold from Google Fonts (direct download URL)
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/notosanskhmer/NotoSansKhmer%5Bwdth%2Cwght%5D.ttf"
FONT_BOLD_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskhmer/NotoSansKhmer-Bold.ttf"

# Alternative: static bold weight
FONT_STATIC_URL = "https://github.com/google/fonts/raw/main/ofl/notosanskhmer/static/NotoSansKhmer-Bold.ttf"


def create_directories():
    """Create required directories."""
    for dir_path in [FONT_DIR, TEMPLATE_DIR, OUTPUT_DIR]:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Directory ready: {dir_path}")


def download_font():
    """Download Noto Sans Khmer Bold font."""
    font_path = os.path.join(FONT_DIR, "NotoSansKhmer-Bold.ttf")

    if os.path.exists(font_path):
        print(f"✅ Font already exists: {font_path}")
        return True

    print("📥 Downloading Noto Sans Khmer Bold font...")

    # Try multiple URLs
    urls = [FONT_STATIC_URL, FONT_BOLD_URL, FONT_URL]

    for url in urls:
        try:
            print(f"   Trying: {url}")
            urllib.request.urlretrieve(url, font_path)
            file_size = os.path.getsize(font_path)

            if file_size > 1000:  # Valid font should be > 1KB
                print(f"✅ Font downloaded successfully ({file_size:,} bytes)")
                return True
            else:
                os.remove(font_path)
                print(f"   ⚠️  File too small ({file_size} bytes), trying next URL...")

        except Exception as e:
            print(f"   ❌ Failed: {e}")
            if os.path.exists(font_path):
                os.remove(font_path)

    print("\n❌ Could not download font automatically.")
    print("   Please download Noto Sans Khmer Bold manually:")
    print("   1. Go to: https://fonts.google.com/noto/specimen/Noto+Sans+Khmer")
    print("   2. Download the font family")
    print("   3. Extract NotoSansKhmer-Bold.ttf")
    print(f"   4. Place it in: {FONT_DIR}")
    return False


def check_template():
    """Check if template image exists."""
    template_path = os.path.join(TEMPLATE_DIR, "template.png")

    if os.path.exists(template_path):
        print(f"✅ Template found: {template_path}")
        return True
    else:
        print(f"\n⚠️  Template not found!")
        print(f"   Please place your template image at:")
        print(f"   {template_path}")
        print(f"   (The template should be your blank gold price image without dynamic text)")
        return False


def check_env():
    """Check if .env file exists."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    env_example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.example")

    if os.path.exists(env_path):
        print(f"✅ .env file found")
        return True
    elif os.path.exists(env_example_path):
        print(f"\n⚠️  .env file not found!")
        print(f"   Copy .env.example to .env and add your bot token:")
        print(f"   copy .env.example .env")
        return False
    else:
        print(f"\n⚠️  No .env file found. Create one with your BOT_TOKEN.")
        return False


def main():
    print("=" * 55)
    print("  🪙 LYHENG JEWELRY - Gold Price Bot Setup")
    print("=" * 55)
    print()

    # Step 1: Create directories
    print("📁 Creating directories...")
    create_directories()
    print()

    # Step 2: Download font
    print("🔤 Checking fonts...")
    font_ok = download_font()
    print()

    # Step 3: Check template
    print("🖼️  Checking template...")
    template_ok = check_template()
    print()

    # Step 4: Check .env
    print("🔑 Checking configuration...")
    env_ok = check_env()
    print()

    # Summary
    print("=" * 55)
    if font_ok and template_ok and env_ok:
        print("✅ All checks passed! Run the bot with:")
        print("   python bot.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
    print("=" * 55)


if __name__ == "__main__":
    main()
