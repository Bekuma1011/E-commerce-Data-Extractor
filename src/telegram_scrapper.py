from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Define Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# Function to scrape one channel
async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title
    async for message in client.iter_messages(entity, limit=500):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            await client.download_media(message.media, media_path)
        
        writer.writerow([
            channel_title,
            channel_username,
            message.id,
            message.message,
            message.date,
            media_path
        ])

# Main async logic
async def run_scraper():
    # Authenticate with phone directly (no prompt)
    await client.start(phone=phone)

    # Prepare media directory
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # Prepare CSV
    with open('../data/telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

        # Channels to scrape
        channels = [
            '@ZemenExpress', '@meneshayeofficial',
            '@classybrands', '@nevacomputer', '@belaclassic'
        ]

        # Scrape each channel
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"✅ Scraped: {channel}")

# Run
asyncio.run(run_scraper())
