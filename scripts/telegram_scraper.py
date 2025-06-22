# scripts/telegram_scraper.py
import os
import json
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, DocumentAttributeFilename, DocumentAttributeVideo
from tqdm.asyncio import tqdm
from datetime import datetime

# Assuming config.py is in the same 'scripts' directory or accessible via system path
from scripts.config import API_ID, API_HASH, PHONE_NUMBER, TELEGRAM_CHANNELS, \
                           RAW_DATA_DIR, PHOTOS_DIR, DOCUMENTS_DIR, RAW_MESSAGES_JSONL

async def setup_telegram_client():
    """Sets up and connects the Telegram client."""
    client = TelegramClient('telegram_scraper_session', API_ID, API_HASH, timeout=60) # Or 30, try different values
    print("Telegram client connecting...")
    await client.start(phone=PHONE_NUMBER)
    print("Telegram client connected.")
    return client

async def get_channel_entities(client, channel_urls):
    """Resolves channel entities from URLs."""
    channel_entities = []
    print("\nResolving channel entities...")
    with tqdm(total=len(channel_urls), desc="Resolving channels") as pbar:
        for url in channel_urls:
            try:
                entity = await client.get_entity(url)
                channel_entities.append(entity)
                # print(f"  -> Found: {entity.title} (ID: {entity.id})") # Uncomment for verbose output
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
        'photo_path': None,
        'has_document': False,
        'document_path': None,
    }

    # Handle Photo (message.photo)
    if message.photo:
        data['has_photo'] = True
        photo_filename = f"photo_{message.id}_{message.date.timestamp()}.jpg"
        photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        try:
            await message.download_media(file=photo_path)
            data['photo_path'] = photo_path
            # print(f"  -> Downloaded photo: {photo_path}") # Uncomment for verbose output
        except Exception as e:
            print(f"  -> ERROR downloading photo for message {message.id}: {e}")
            data['photo_path'] = None # Mark as failed if download fails

    # Handle Document (message.document - this also includes videos, GIFs, files)
    if message.document:
        data['has_document'] = True
        document_filename = None

        # --- Attempt 1: Get filename directly from message.file.name (most reliable for many cases) ---
        if hasattr(message.file, 'name') and message.file.name:
            document_filename = message.file.name
        else:
            # --- Attempt 2: Iterate through attributes for DocumentAttributeFilename ---
            for attr in message.document.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    document_filename = attr.file_name
                    break # Found it, exit loop

            # --- Attempt 3: If still no filename, and it's a video document, create a generic video name ---
            if not document_filename:
                for attr in message.document.attributes:
                    if isinstance(attr, DocumentAttributeVideo):
                        ext = 'mp4' # Default video extension, can be more specific if needed
                        document_filename = f"video_{message.id}_{message.date.timestamp()}.{ext}"
                        break

            # --- Attempt 4: Final fallback using MIME type if no specific filename or video name found ---
            if not document_filename:
                ext = message.document.mime_type.split('/')[-1] if message.document.mime_type else 'bin'
                document_filename = f"doc_{message.id}_{message.date.timestamp()}.{ext}"

        document_path = os.path.join(DOCUMENTS_DIR, document_filename)
        try:
            await message.download_media(file=document_path)
            data['document_path'] = document_path
            # print(f"  -> Downloaded document: {document_path}") # Uncomment for verbose output
        except Exception as e:
            print(f"  -> ERROR downloading document for message {message.id} ({document_filename}): {e}")
            data['document_path'] = None # Mark as failed if download fails

    return data

async def scrape_channel_messages(client, channel_entity):
    """Fetches all messages from a single channel."""
    all_messages = []
    print(f"\nFetching historical messages from '{channel_entity.title}' (ID: {channel_entity.id})...")

    # Get the total message count for the progress bar
    total_messages = await client.get_messages(channel_entity, limit=0)
    pbar_description = f"Scraping '{channel_entity.title}'"

    async for message in client.iter_messages(channel_entity, reverse=True): # reverse=True to get oldest first
        processed_data = await process_message(message)
        all_messages.append(processed_data)
        # No tqdm update here, as iter_messages doesn't provide total easily.
        # tqdm can be implemented with a separate counter or by estimating.
        # For simplicity, we'll just show the message processing.
        # You can add a counter and update tqdm if performance allows.

    print(f"  -> Fetched {len(all_messages)} messages from '{channel_entity.title}'.")
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

    client = await setup_telegram_client()

    try:
        channel_entities = await get_channel_entities(client, TELEGRAM_CHANNELS)

        all_scraped_messages = []
        for entity in channel_entities:
            # Skip if entity resolution failed for some reason (though error message is printed)
            if entity:
                messages = await scrape_channel_messages(client, entity)
                all_scraped_messages.extend(messages)
            else:
                print(f"Skipping a channel that could not be resolved.")

        # Save all scraped messages to a JSONL file
        with open(RAW_MESSAGES_JSONL, 'a', encoding='utf-8') as f: # Use 'a' to append if multiple runs (not typical here)
            for msg_data in all_scraped_messages:
                f.write(json.dumps(msg_data, ensure_ascii=False) + '\n')
        print(f"\nSuccessfully saved {len(all_scraped_messages)} raw messages to {RAW_MESSAGES_JSONL}")

    finally:
        if client.is_connected():
            await client.disconnect()
            print("Telegram client disconnected.")

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Run the main ingestion function
    asyncio.run(ingest_telegram_data())