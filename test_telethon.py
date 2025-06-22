import asyncio
from telethon import TelegramClient
import os

# --- Telegram API Credentials ---
API_ID = 28070806 # Replace with your actual API ID (e.g., 1234567)
API_HASH = '39b72cddcf9072e69c0ca572d4e43d5d' # Replace with your actual API Hash (e.g., 'abcdef123456...')
PHONE_NUMBER = '+251904444007' # Your Telegram phone number (e.g., '+2519xxxxxxxx')

async def simple_test():
    session_name = 'test_telethon_session'
    # Delete old test session if it exists
    if os.path.exists(f"{session_name}.session"):
        os.remove(f"{session_name}.session")
        print(f"Removed old {session_name}.session")

    print("Attempting to connect...")
    try:
        async with TelegramClient(session_name, API_ID, API_HASH, timeout=30) as client:
            print("Client connected successfully for test.")
            # You can add a small delay or a simple operation here if needed
            # e.g., await client.get_me()
            print(f"Connected as: {await client.get_me()}")
        print("Client disconnected successfully from test.")
    except Exception as e:
        print(f"Error during simple Telethon test: {e}")

if __name__ == '__main__':
    asyncio.run(simple_test())