# scripts/text_preprocessor.py
import re
import string
from scripts.config import CHARS_TO_REMOVE, AMHARIC_STOPWORDS, PRICE_PATTERN, PHONE_PATTERN

class AmharicPreprocessor:
    def __init__(self, chars_to_remove=CHARS_TO_REMOVE, stopwords=AMHARIC_STOPWORDS):
        self.chars_to_remove_pattern = re.compile(f"[{re.escape(chars_to_remove)}]")
        self.stopwords = set(stopwords)

    def clean_text(self, text):
        """Removes unwanted characters and extra spaces."""
        if not isinstance(text, str):
            return ""
        text = self.chars_to_remove_pattern.sub('', text)
        text = re.sub(r'\s+', ' ', text).strip() # Replace multiple spaces with single space
        return text

    def remove_emojis_and_symbols(self, text):
        """Removes emojis and other non-Amharic/non-alphanumeric symbols."""
        if not isinstance(text, str):
            return ""
        # Keep Amharic (Ethiopic script), basic Latin (for numbers/English words), numbers, and some punctuation
        # Ethiopic Unicode range: \u1200-\u137F (and other ranges if needed)
        # For simplicity, a broad removal of non-standard chars
        # This regex keeps Amharic characters, English letters, numbers, and basic punctuation.
        cleaned_text = re.sub(r'[^\u1200-\u137F\u1369-\u1371\s\w.,!?-]', '', text)
        return cleaned_text

    def normalize_amharic_text(self, text):
        """Normalizes Amharic characters (e.g., merging similar-looking characters)."""
        if not isinstance(text, str):
            return ""
        # Example normalizations (expand as needed based on common variations)
        text = text.replace("ሀ", "ሃ") # ha
        text = text.replace("ሑ", "ሁ") # hu
        text = text.replace("ሒ", "ሂ") # hi
        text = text.replace("ኅ", "ህ") # he
        text = text.replace("ኈ", "ሆ") # ho
        text = text.replace("ሠ", "ሰ") # se
        text = text.replace("ሸ", "ሰ") # se (if sh is considered same as s)
        text = text.replace("ዐ", "አ") # a'in
        text = text.replace("ዒ", "ኢ") # i'in
        text = text.replace("ዑ", "ኡ") # u'in
        text = text.replace("ዓ", "አ") # a'in
        text = text.replace("ፅ", "ጽ") # ts'i
        text = text.replace("ጾ", "ፆ") # tso
        # More complex normalizations might involve character mapping tables
        return text

    def remove_stopwords(self, text):
        """Removes common Amharic stopwords."""
        if not isinstance(text, str):
            return ""
        words = text.split()
        filtered_words = [word for word in words if word not in self.stopwords]
        return " ".join(filtered_words)

    def preprocess_text(self, text):
        """Applies all preprocessing steps in order."""
        text = self.clean_text(text)
        text = self.remove_emojis_and_symbols(text)
        text = self.normalize_amharic_text(text)
        text = self.remove_stopwords(text)
        text = text.lower() # Convert to lowercase (Amharic doesn't have case, but good for consistency)
        return text

    def extract_price(self, text):
        """Extracts potential price information from text."""
        if not isinstance(text, str):
            return None
        matches = re.findall(PRICE_PATTERN, text)
        if matches:
            # Return the first found price, removing commas for numeric conversion
            return matches[0].replace(',', '')
        return None

    def extract_phone_number(self, text):
        """Extracts potential phone numbers from text."""
        if not isinstance(text, str):
            return None
        matches = re.findall(PHONE_PATTERN, text)
        if matches:
            # For simplicity, return the first found number and clean it
            phone = re.sub(r'[^\d]', '', matches[0])
            return phone
        return None

# Example usage (for testing within the module)
if __name__ == '__main__':
    preprocessor = AmharicPreprocessor()
    sample_text = "ጤና ይስጥልኝ! ይህ በጣም ቆንጆ ስልክ ነው። ዋጋው 5,000 ብር ብቻ። 📞 ለበለጠ መረጃ ይደውሉልን። 0912345678"
    print(f"Original: {sample_text}")
    
    cleaned = preprocessor.clean_text(sample_text)
    print(f"Cleaned: {cleaned}")
    
    no_emojis = preprocessor.remove_emojis_and_symbols(sample_text)
    print(f"No Emojis: {no_emojis}")

    normalized = preprocessor.normalize_amharic_text("ሠላም ዐለም!")
    print(f"Normalized: {normalized}")
    
    processed = preprocessor.preprocess_text(sample_text)
    print(f"Processed: {processed}")

    price = preprocessor.extract_price(sample_text)
    print(f"Extracted Price: {price}")

    phone = preprocessor.extract_phone_number(sample_text)
    print(f"Extracted Phone: {phone}")