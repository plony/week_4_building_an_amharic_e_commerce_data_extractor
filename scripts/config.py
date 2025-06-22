# scripts/config.py
import os

# --- Project Paths ---
# Get the directory where the config.py script is located
# This assumes config.py is in the 'scripts' folder, and PROJECT_ROOT is its parent
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data Directories
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
LABELED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'labeled') # For Task 2: Labeling

# Media Directories (within RAW_DATA_DIR)
PHOTOS_DIR = os.path.join(RAW_DATA_DIR, 'photos')
DOCUMENTS_DIR = os.path.join(RAW_DATA_DIR, 'documents')

# File Paths
RAW_MESSAGES_JSONL = os.path.join(RAW_DATA_DIR, 'telegram_messages.jsonl')
STRUCTURED_DATA_JSONL = os.path.join(PROCESSED_DATA_DIR, 'structured_telegram_data.jsonl')

# --- Telegram API Credentials ---
API_ID = 28070806 # Replace with your actual API ID (e.g., 1234567)
API_HASH = '39b72cddcf9072e69c0ca572d4e43d5d' # Replace with your actual API Hash (e.g., 'abcdef123456...')
PHONE_NUMBER = '+251904444007' # Your Telegram phone number (e.g., '+2519xxxxxxxx')

# --- Telegram Channels to Scrape ---
TELEGRAM_CHANNELS = [
  'https://t.me/ZemenExpress',
    'https://t.me/nevacomputer',
    'https://t.me/meneshayeofficial',
    'https://t.me/ethio_brand_collection',
    'https://t.me/Leyueqa',
    'https://t.me/sinayelj',
    'https://t.me/Shewabrand',
    'https://t.me/helloomarketethiopia',
    'https://t.me/modernshoppingcenter',
    'https://t.me/qnashcom',
    'https://t.me/Fashiontera',
    'https://t.me/kuruwear',
    'https://t.me/gebeyaadama',
    'https://t.me/MerttEka',
    'https://t.me/forfreemarket',
    'https://t.me/classybrands',
    'https://t.me/marakibrand',
    'https://t.me/aradabrand2',
    'https://t.me/marakisat2',
    'https://t.me/belaclassic',
    'https://t.me/AwasMart'
       # Note: @qnashcom was
]

# --- Preprocessing Configuration ---
# Characters to remove during preprocessing
CHARS_TO_REMOVE = "•●★☆▪︎¤°`´„“«»‘’›‹„“‘’”„“‘’"
