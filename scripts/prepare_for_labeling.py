import json
import os

# Define paths (adjust if your data/processed directory is different)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
STRUCTURED_DATA_JSONL = os.path.join(PROCESSED_DATA_DIR, 'structured_telegram_data.jsonl')
MESSAGES_FOR_LABELING_TXT = os.path.join(PROCESSED_DATA_DIR, 'messages_for_labeling.txt')

def extract_messages_for_labeling(num_messages=50):
    """
    Extracts a specified number of message texts from the structured JSONL file
    and saves them to a plain text file for manual labeling.
    """
    extracted_count = 0
    with open(STRUCTURED_DATA_JSONL, 'r', encoding='utf-8') as infile, \
         open(MESSAGES_FOR_LABELING_TXT, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if extracted_count >= num_messages:
                break
            try:
                data = json.loads(line.strip())
                message_text = data.get('cleaned_text')
                if message_text:
                    # Write message_id for easy reference
                    outfile.write(f"--- Message ID: {data.get('message_id')} ---\n")
                    outfile.write(f"{message_text}\n\n") # Two newlines to separate messages visually
                    extracted_count += 1
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")
    print(f"Extracted {extracted_count} messages to '{MESSAGES_FOR_LABELING_TXT}' for labeling.")
    print("Please open this file, copy messages, and manually label them.")

if __name__ == "__main__":
    extract_messages_for_labeling(num_messages=50) # You can change this number