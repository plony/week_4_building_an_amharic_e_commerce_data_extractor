# scripts/config.py

import os

# --- Telegram API Credentials ---
API_ID = 28070806 # Replace with your actual API ID (e.g., 1234567)
API_HASH = '39b72cddcf9072e69c0ca572d4e43d5d' # Replace with your actual API Hash (e.g., 'abcdef123456...')
PHONE_NUMBER = '+251904444007' # Your Telegram phone number (e.g., '+2519xxxxxxxx')

# --- Telegram Channels to Scrape ---
# Provide public Telegram channel URLs or usernames.
# For debugging network/session issues, it's temporarily reduced to 1-2 channels.
# Expand this list once the scraping is stable.
TELEGRAM_CHANNELS = [
    # 'https://t.me/EthioMart_DMC', # Keep this commented out or corrected as per your last action
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
    'https://t.me/gebeyaadama', # This one resolved to 'አዳማ ገበያ - Adama gebeya'
    'https://t.me/MerttEka',
    'https://t.me/forfreemarket',
    'https://t.me/classybrands',
    'https://t.me/marakibrand',
    'https://t.me/aradabrand2',
    'https://t.me/marakisat2',
    'https://t.me/belaclassic',
    'https://t.me/AwasMart'# This one worked!
    # Add more channels here if needed, e.g., 'https://t.me/your_channel_name',
    # 'https://t.me/another_channel_url'
]

# --- Directory Paths ---
# Base directory for data storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Raw data directory for initial scraped messages
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
RAW_MESSAGES_JSONL = os.path.join(RAW_DATA_DIR, 'telegram_messages.jsonl')

# Interim data directory for temporary processing files
INTERIM_DATA_DIR = os.path.join(DATA_DIR, 'interim')

# Directories for downloaded media
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
DOCUMENTS_DIR = os.path.join(DATA_DIR, 'documents')

# Processed data directory
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
PROCESSED_MESSAGES_JSON = os.path.join(PROCESSED_DATA_DIR, 'processed_messages.json')

# Path for structured data output (after preprocessing)
STRUCTURED_DATA_JSONL = os.path.join(PROCESSED_DATA_DIR, 'structured_telegram_data.jsonl')

# --- Text Preprocessing Constants ---
# Characters to remove during text cleaning (using a raw string for regex pattern)
CHARS_TO_REMOVE = r"['\"”‘’“”!@#$%^&*()_+={}\[\]:;<>,.?/\\|`~-—–\n]"

# Amharic stopwords list
AMHARIC_STOPWORDS = [
    "እና", "ወይም", "ነው", "ናቸው", "ነበር", "ነበሩ", "አለ", "አሉ", "አይደለም", "ከ", "ለ", "በ",
    "ላይ", "ውስጥ", "ጋር", "የ", "ም", "ው", "ምንም", "ሁሉ", "ሌላ", "አንድ", "ሁለት", "ሶስት",
    "አራት", "አምስት", "ስድስት", "ሰባት", "ስምንት", "ዘጠኝ", "አስር", "እኔ", "አንተ", "አንቺ",
    "እሱ", "እሷ", "እኛ", "እናንተ", "እነሱ", "ይህ", "ያ", "እነዚህ", "እነዚያ", "እንዴት", "ለምን",
    "የት", "መቼ", "ማን", "ምን", "የትኛው", "እንዲሁም", "ብቻ", "ብቻውን", "እንደ", "እንደገና",
    "ሲሆን", "ግን", "ስለ", "አሁን", "ከዚህ", "በኋላ", "እስከ", "ባይሆን", "ወደ", "ምክንያቱም",
    "ካልሆነ", "አሁንም", "ወዲያውኑ", "በፊት", "በኋላ", "ዛሬ", "ትላንትና", "ነገ", "ብዙ", "ትንሽ",
    "ጥቂት", "ብዙዎች", "ሁሉም", "አንዳንዶቹ", "ምንም", "ያለ", "በጣም", "አብዛኛውን", "እጅግ",
    "አሁንም", "አይ", "አዎ", "በእርግጥ", "ደግሞ", "እንዲሁም", "እንኳን", "ልክ", "ምናልባት",
    "እስካሁን", "ወደ", "ከ", "ውስጥ", "ላይ", "ስር", "በፊት", "በኋላ", "ጎን", "መካከል", "ውስጥ",
    "ውጪ", "ላይ", "ታች", "ከ", "ውስጥ", "አጠገብ", "ቀጥሎ", "አቅራቢያ", "ርቀት", "ቅርብ", "ሩቅ",
    "ቀኝ", "ግራ", "ቀጥታ", "ወደ", "ከ", "የ", "ነው", "ናቸው", "ነበር", "ነበሩ", "አለ", "አሉ",
    "አይደለም", "አት", "አል", "እ", "ይ", "ት", "ን", "ሽ", "ች", "ክ", "ል", "ም", "ስ", "ር",
    "ጥ", "ቅ", "ዝ", "ጅ", "ጭ", "ግ", "ድ", "ህ", "ው", "ብ", "ተ", "ነ", "አ", "የ", "ው", "ኦ",
    "ሆ", "ሄ", "ሃ", "ሂ", "ሎ", "ላ", "ሊ", "ሉ", "ሌ", "ል", "መ", "ሙ", "ሚ", "ማ", "ሜ", "ም",
    "ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ረ", "ሩ", "ሪ", "ራ", "ሬ", "ር", "ቀ", "ቁ", "ቂ", "ቃ",
    "ቄ", "ቅ", "በ", "ቡ", "ቢ", "ባ", "ቤ", "ብ", "ተ", "ቱ", "ቲ", "ታ", "ቴ", "ት", "ቸ", "ቹ",
    "ቺ", "ቻ", "ቼ", "ች", "ነ", "ኑ", "ኒ", "ና", "ኔ", "ን", "ከ", "ኩ", "ኪ", "ካ", "ኬ", "ክ",
    "ወ", "ዉ", "ዊ", "ዋ", "ዌ", "ው", "ዐ", "ዑ", "ዒ", "ዓ", "ዔ", "ዕ", "ዘ", "ዙ", "ዚ", "ዛ",
    "ዜ", "ዝ", "የ", "ዩ", "ዪ", "ያ", "ዬ", "ይ", "ደ", "ዱ", "ዲ", "ዳ", "ዴ", "ድ", "ጀ", "ጁ",
    "ጂ", "ጃ", "ጄ", "ጅ", "ገ", "ጉ", "ጊ", "ጋ", "ጌ", "ግ", "ጠ", "ጡ", "ጢ", "ጣ", "ጤ", "ጥ",
    "ጏ", "ጟ", "ጧ", "ጷ", "ፀ", "ፁ", "ፂ", "ፃ", "ጼ", "ፅ", "ፈ", "ፉ", "ፊ", "ፋ", "ፌ", "ፍ",
    "ፐ", "ፑ", "ፒ", "ፓ", "ፔ", "ፕ"
]

# Regular expression patterns for extracting information
PRICE_PATTERN = r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:ETB|ብር)?"
PHONE_PATTERN = r"(?:\+251|0)?(?:9|7)\d{8}" # Common Ethiopian phone number patterns # <--- ADD THIS LINE


# Path for the SQLite database (used by Telethon for session)
# The session file will be created in the base directory by default
# telegram_scraper_session.session will be created in the root if not specified otherwise