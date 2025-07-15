import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import Image

# Folder path to monitor for new images
FOLDER_PATH = 'C:\\Ham\\MMSSTV\\History'

# Discord webhook URL
WEBHOOK_URL = 'full HTTPS:// address of your webhook goes here'

# Your custom note to be included in the message
CUSTOM_NOTE = "Maybe your call sign or the band you're using"

# Set to store uploaded image filenames
uploaded_images = set()

# Maximum file size (500KB)
MAX_FILE_SIZE = 1024 * 1024

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.lower().endswith('.bmp'):
            image_filename = os.path.basename(event.src_path)
            
            # Check if the image has not been uploaded before and is smaller than 500KB
            if image_filename not in uploaded_images and os.path.getsize(event.src_path) <= MAX_FILE_SIZE:
                uploaded_images.add(image_filename)
                print(f'New image detected: {event.src_path}')
                time.sleep(1)  # Add a 1-second delay
                upload_image(event.src_path)

def convert_to_jpg(image_path):
    img = Image.open(image_path)
    image_without_extension = os.path.splitext(image_path)[0]
    jpg_path = f'{image_without_extension}.jpg'
    img.convert('RGB').save(jpg_path)
    return jpg_path

def upload_image(image_path):
    # Convert the image to JPG if it's a BMP file
    if image_path.lower().endswith('.bmp'):
        image_path = convert_to_jpg(image_path)

    webhook = DiscordWebhook(url=WEBHOOK_URL, content=CUSTOM_NOTE)

    with open(image_path, 'rb') as f:
        image_data = f.read()

    embed = DiscordEmbed()
    embed.set_image(url=f'attachment://{os.path.basename(image_path)}')
    webhook.add_embed(embed)
    webhook.add_file(file=image_data, filename=os.path.basename(image_path))

    response = webhook.execute()
    print(f'Image {os.path.basename(image_path)} uploaded to Discord. Response: {response}')

    # Delete the converted JPG file if it was originally a BMP
    if image_path.lower().endswith('.bmp'):
        os.remove(image_path)

if __name__ == "__main__":
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
