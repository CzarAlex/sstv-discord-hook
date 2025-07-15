# 📡 MMSSTV Discord Image Uploader

This Python script watches a folder (e.g. `C:\Ham\MMSSTV\History`) for new `.bmp` images, and automatically uploads them to a Discord channel via webhook **only if the image is larger than 900 KB**. It's great for automatically sharing high-quality Slow Scan TV (SSTV) images!

---

## ✨ Features

- ✅ Monitors a folder in real-time
- 🖼️ Filters `.bmp` files by size (> 900KB)
- 🔄 Converts `.bmp` to `.jpg` before uploading
- 📤 Uploads image to a Discord webhook with a custom message

The size filter is to hopefully weed out static-only decodes.

---

## 📦 Requirements

This script requires Python 3.6 or newer and a few third-party libraries.

Install dependencies using:

```bash
pip install watchdog discord-webhook Pillow
