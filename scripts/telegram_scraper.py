# scripts/telegram_scraper.py
import os
import json
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, DocumentAttributeFilename, DocumentAttributeVideo
from tqdm.asyncio import tqdm
from datetime import datetime

# Import paths and credentials from config.py
from scripts.config import API_ID, API_HASH, PHONE_NUMBER, TELEGRAM_CHANNELS, \
                           RAW_DATA_DIR, IMAGES_DIR, DOCUMENTS_DIR, RAW_MESSAGES_JSONL

# --- NOTE: The setup_telegram_client function has been removed. ---
# The connection is now handled directly by 'async with TelegramClient' in ingest_telegram_data.

async def get_channel_entities(client, channel_urls):
    """Resolves channel entities from URLs."""
    # The client is guaranteed to be connected here because ingest_telegram_data
    # uses 'async with TelegramClient' which ensures connection.
    channel_entities = []
    print("\nResolving channel entities...")
    with tqdm(total=len(channel_urls), desc="Resolving channels") as pbar:
        for url in channel_urls:
            try:
                entity = await client.get_entity(url)
                channel_entities.append(entity)
            except Exception as e:
                print(f"  -> ERROR: Could not resolve {url}: {e}")
            pbar.update(1)
    return channel_entities

async def process_message(message):
    """
    Processes a single Telegram message, extracts relevant data,
    and handles media downloads.
    """
    data = {
        'channel_id': message.peer_id.channel_id if hasattr(message.peer_id, 'channel_id') else None,
        'message_id': message.id,
        'date': message.date.isoformat(),
        'text': message.message,
        'views': message.views,
        'forwards': message.forwards,
        'replies_count': message.replies.replies if message.replies else 0,
        'has_photo': False,
        'image_path': None,
        'has_document': False,
        'document_path': None,
        'media_download_error': False
    }

    if message.photo:
        data['has_photo'] = True
        image_filename = f"image_{message.id}_{message.date.timestamp()}.jpg"
        image_path = os.path.join(IMAGES_DIR, image_filename)
        try:
            if not os.path.exists(image_path):
                await message.download_media(file=image_path)
            data['image_path'] = image_path
        except Exception as e:
            print(f"  -> ERROR downloading image for message {message.id}: {e}")
            data['image_path'] = None
            data['media_download_error'] = True

    if message.document:
        data['has_document'] = True
        document_filename = None

        if hasattr(message.file, 'name') and message.file.name:
            document_filename = message.file.name
        else:
            for attr in message.document.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    document_filename = attr.file_name
                    break
            if not document_filename:
                for attr in message.document.attributes:
                    if isinstance(attr, DocumentAttributeVideo):
                        ext = 'mp4'
                        document_filename = f"video_{message.id}_{message.date.timestamp()}.{ext}"
                        break
            if not document_filename:
                ext = message.document.mime_type.split('/')[-1] if message.document.mime_type else 'bin'
                document_filename = f"doc_{message.id}_{message.date.timestamp()}.{ext}"

        document_path = os.path.join(DOCUMENTS_DIR, document_filename)
        try:
            if not os.path.exists(document_path):
                await message.download_media(file=document_path)
            data['document_path'] = document_path
        except Exception as e:
            print(f"  -> ERROR downloading document for message {message.id} ({document_filename}): {e}")
            data['document_path'] = None
            data['media_download_error'] = True

    return data

async def scrape_channel_messages(client, channel_entity):
    """Fetches all messages from a single channel."""
    all_messages = []
    print(f"\nFetching historical messages from '{channel_entity.title}' (ID: {channel_entity.id})...")

    # --- ADD THIS LINE FOR TESTING ---
    # Limits the number of messages fetched per channel.
    # Set a small number (e.g., 500) for quick testing.
    # You can increase this later or remove it for full scraping if confident.
    MESSAGE_LIMIT_PER_CHANNEL = 100 # You can set this to 100, 500, or 1000 for testing.

    try:
        # --- MODIFY THIS LINE TO INCLUDE THE LIMIT ---
        async for message in client.iter_messages(channel_entity, reverse=True, limit=MESSAGE_LIMIT_PER_CHANNEL):
            processed_data = await process_message(message)
            all_messages.append(processed_data)
    except Exception as e:
        print(f"  -> An error occurred while scraping '{channel_entity.title}': {e}")
    finally:
        print(f"\n  -> Fetched {len(all_messages)} messages from '{channel_entity.title}'.")
    return all_messages

async def ingest_telegram_data():
    """
    Main function to orchestrate Telegram data ingestion.
    Connects to Telegram, resolves channels, scrapes messages,
    and saves them to a JSONL file.
    """
    # Remove existing raw data file for a clean ingestion
    if os.path.exists(RAW_MESSAGES_JSONL):
        os.remove(RAW_MESSAGES_JSONL)
        print(f"Removed existing {RAW_MESSAGES_JSONL} for a clean ingestion.")

    # Use async with for robust client management
    # The client will automatically connect on 'async with' entry
    # and disconnect on 'async with' exit (even if errors occur)
    print("Telegram client connecting...")
    try:
        async with TelegramClient('telegram_scraper_session', API_ID, API_HASH, timeout=60) as client:
            print("Telegram client connected.")

            channel_entities = await get_channel_entities(client, TELEGRAM_CHANNELS)

            all_scraped_messages = []
            for entity in channel_entities:
                if entity:
                    messages = await scrape_channel_messages(client, entity)
                    all_scraped_messages.extend(messages)
                else:
                    print(f"Skipping a channel that could not be resolved.")

            # Save all scraped messages to a JSONL file
            with open(RAW_MESSAGES_JSONL, 'a', encoding='utf-8') as f:
                for msg_data in all_scraped_messages:
                    f.write(json.dumps(msg_data, ensure_ascii=False) + '\n')
            print(f"\nSuccessfully saved {len(all_scraped_messages)} raw messages to {RAW_MESSAGES_JSONL}")

    except Exception as e:
        # This catches errors during connection, scraping, or saving
        print(f"An error occurred during data ingestion: {e}")
    # --- NOTE: The manual 'finally' block for client disconnection has been removed. ---
    # Because 'async with' handles it automatically and robustly, even if errors occur.


if __name__ == '__main__':
    # Ensure directories exist before running independently too.
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    asyncio.run(ingest_telegram_data())