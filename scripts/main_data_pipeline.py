# scripts/main_data_pipeline.py
import os
import asyncio
import json
import pandas as pd # Import pandas if you plan to use it for data structuring/analysis later
from tqdm import tqdm # Import tqdm for progress bars

# Import constants from config.py
from scripts.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR, \
                           RAW_MESSAGES_JSONL, STRUCTURED_DATA_JSONL, \
                           IMAGES_DIR, DOCUMENTS_DIR, CHARS_TO_REMOVE

# Import functions from telegram_scraper.py
from scripts.telegram_scraper import ingest_telegram_data

# Import the AmharicPreprocessor class from text_preprocessor.py
from scripts.text_preprocessor import AmharicPreprocessor


def setup_directories():
    """Ensures that the necessary directories exist."""
    print("Setting up directories...")
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(INTERIM_DATA_DIR, exist_ok=True) # Ensure interim dir exists
    os.makedirs(IMAGES_DIR, exist_ok=True) # Changed from PHOTOS_DIR
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print("Directories are ready.")

async def main_pipeline_execution():
    """
    Orchestrates the entire data pipeline:
    1. Ingests raw data from Telegram.
    2. Preprocesses the text data and extracts entities.
    3. Saves structured data.
    """
    setup_directories()

    # --- Step 1: Data Ingestion from Telegram Channels ---
    print("\n--- Step 1: Data Ingestion from Telegram Channels ---")
    await ingest_telegram_data()

    # --- Step 2: Data Preprocessing and Structuring ---
    print("\n--- Step 2: Data Preprocessing and Structuring ---")
    if os.path.exists(RAW_MESSAGES_JSONL):
        preprocessor = AmharicPreprocessor() # Initialize the preprocessor

        processed_messages = []
        with open(RAW_MESSAGES_JSONL, 'r', encoding='utf-8') as f_in:
            for line in tqdm(f_in, desc="Preprocessing messages"):
                message_data = json.loads(line)

                # Initialize new fields
                message_data['cleaned_text'] = None
                message_data['extracted_price'] = None
                message_data['extracted_phone'] = None

                if 'text' in message_data and message_data['text']:
                    original_text = message_data['text']

                    # Apply preprocessing steps
                    message_data['cleaned_text'] = preprocessor.preprocess_text(original_text)

                    # Extract entities
                    message_data['extracted_price'] = preprocessor.extract_price(original_text)
                    message_data['extracted_phone'] = preprocessor.extract_phone_number(original_text)

                processed_messages.append(message_data)

        # Save the processed data to the structured JSONL file
        print(f"Saving processed data to {STRUCTURED_DATA_JSONL}...")
        with open(STRUCTURED_DATA_JSONL, 'w', encoding='utf-8') as f_out:
            for msg_data in processed_messages:
                f_out.write(json.dumps(msg_data, ensure_ascii=False) + '\n')
        print(f"Successfully processed and structured {len(processed_messages)} messages to {STRUCTURED_DATA_JSONL}")
    else:
        print(f"No raw messages found at {RAW_MESSAGES_JSONL}. Skipping preprocessing.")

    print("\nData pipeline execution completed.")


if __name__ == '__main__':
    try:
        asyncio.run(main_pipeline_execution())
    except Exception as e:
        print(f"An error occurred during the pipeline execution: {e}")