# scripts/text_preprocessor.py

import re
import unicodedata
from scripts.config import REMOVE_STOPWORDS # Import config for stopword setting

class AmharicPreprocessor:
    """
    A class for preprocessing Amharic text data.
    Handles cleaning, normalization, and tokenization.
    """
    def __init__(self):
        # Define homophone mapping for normalization. This is a complex area.
        # For NER, sometimes preserving original form is better, but for general text tasks, normalization helps.
        # A more robust solution would involve a lookup table or more complex linguistic rules.
        # For now, a conservative approach is taken for NER, primarily cleaning and standardizing.
        # If true homophone normalization is needed, this mapping should be extensively researched.
        # Example of a few common variations, focus on visual consistency for now:
        self.homophone_map = {
            'ሀ': 'ሀ', 'ሃ': 'ሀ', 'ሐ': 'ሀ', 'ሓ': 'ሀ', 'ኀ': 'ሀ', 'ኃ': 'ሀ', 'ኻ': 'ሀ',
            'ሰ': 'ሰ', 'ሠ': 'ሰ',
            'ጸ': 'ጸ', 'ፀ': 'ጸ',
            'ው': 'ው', 'ዉ': 'ው', # More of a spelling variant
            'አ': 'አ', 'ኣ': 'አ', 'ዐ': 'አ', 'ዓ': 'አ',
            # Add other known variations if critical for NER, else LLM might handle.
        }

        # Common Amharic punctuation and symbols to remove or replace.
        # Includes Ethiopic punctuation marks.
        self.amharic_punctuation = r'[\!\@\#\$\%\^\«\»\&\*\(\)\…\[\]\{\}\;“‟”›‘’\"\'\:\,\.\‹\/\<\>\?\—\\\`\´\~\|\=\+\፡\።\፤\፥\፧\፨\፠]'

        # Regex for common emojis and symbols
        self.emojis_and_symbols = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U00002600-\U000026FF"  # Miscellaneous Symbols
            "\U0000FE00-\U0000FE0F"  # Variation Selectors
            "\U0001FAD0-\U0001FADF"  # Added in Unicode 13.0 for food/drink
            "\U0001F6F0-\U0001F6FF"  # Symbols and Pictographs Extended-A
            "]+", flags=re.UNICODE
        )

        # Amharic stop words - this list needs to be comprehensive.
        # This is a sample; for production, source a larger list or create one.
        self.amharic_stopwords = set([
            "እና", "ነበር", "ነው", "ግን", "ከ", "በ", "ላይ", "ወደ", "ሲል", "ለ", "የ", "አዎ", "አይደለም", "ያለ",
            "አሉት", "አላቸው", "አሉ", "ሲሆን", "የሆነ", "ሆኖ", "በፊት", "ከዛ", "በኋላ", "ዛሬ", "ትናንት",
            "ነገ", "አንዳንድ", "ብዙ", "ሁሉንም", "ሁሉም", "ማን", "ምን", "የት", "እንዴት", "ለምን", "መቼ",
            "የትኛዉ", "እሱ", "እሷ", "እነሱ", "እኛ", "አንተ", "አንቺ", "እናንተ", "እኔ", "እርሱ", "እርሷ", "እርሳቸው",
            "ያ", "ይህ", "እነዚህ", "እነዚያ", "እንዲሁም", "ወይም", "ምናልባት", "ብቻ", "ግዴታ", "አንዴ", "ሁለት",
            "ሶስት", "አራት", "አምስት", "ስድስት", "ሰባት", "ስምንት", "ዘጠኝ", "አስር"
            # Add more as you refine your stopwords list
        ])

    def clean_text(self, text):
        """Removes URLs, mentions, hashtags, non-Amharic characters, emojis, and extra whitespace."""
        if not isinstance(text, str): # Handle non-string inputs (e.g., None)
            return ""
        # 1. Decode potential HTML entities (if any are left from source)
        text = unicodedata.normalize('NFKC', text)
        # 2. Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # 3. Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        # 4. Remove emojis
        text = self.emojis_and_symbols.sub(r'', text)
        # 5. Remove non-Amharic script (Ethiopic Unicode blocks), except numbers and some common symbols
        # Unicode ranges for Ethiopic: U+1200–U+137F, U+2D80–U+2DDF (Ethiopic Extended), U+AB00–U+AB2F (Ethiopic Extended-A)
        # Keeping basic Latin letters for potential loanwords/brands, and common numbers.
        # A more strict approach would remove all non-Ethiopic script except numbers.
        text = re.sub(r'[^\u1200-\u137F\u2D80-\u2DDF\uAB00-\uAB2F0-9a-zA-Z\s' + re.escape(self.amharic_punctuation) + ']', '', text)
        # 6. Remove excess spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def normalize_amharic_characters(self, text):
        """Applies homophone normalization if defined. Cautious approach for NER."""
        normalized_text = ""
        for char in text:
            # Only apply if a mapping exists. Otherwise, keep original.
            normalized_text += self.homophone_map.get(char, char)
        return normalized_text

    def normalize_numbers(self, text):
        """Converts Ge'ez numbers to Arabic numerals."""
        geez_to_arabic_map = {
            '፩': '1', '፪': '2', '፫': '3', '፬': '4', '፭': '5',
            '፮': '6', '፯': '7', '፰': '8', '፱': '9', '፲': '10',
            '፳': '20', '፴': '30', '፵': '40', '፶': '50', '፷': '60',
            '፸': '70', '፹': '80', '፺': '90', '፻': '100', '፼': '10000'
        }
        for geez, arabic in geez_to_arabic_map.items():
            text = text.replace(geez, arabic)
        return text

    def tokenize(self, text):
        """Basic tokenization by spaces and common punctuation.
           For production, consider dedicated Amharic tokenizers if available and performing better.
        """
        # Split by spaces and by standard Amharic punctuation, keeping punctuation as tokens
        # Example: "ቃል::" -> ["ቃል", "::"] or "ቃል", ".", "."
        # For now, just split by whitespace and remove empty strings.
        tokens = text.split()
        return [token for token in tokens if token]

    def remove_stopwords(self, tokens):
        """Removes defined Amharic stopwords from a list of tokens."""
        return [token for token in tokens if token not in self.amharic_stopwords]

    def preprocess(self, text):
        """
        Main preprocessing pipeline for Amharic text.
        Applies cleaning, normalization, tokenization, and optional stopword removal.
        """
        # 1. Clean the raw text (remove noise)
        text = self.clean_text(text)
        # 2. Normalize Amharic characters (homophones etc.)
        text = self.normalize_amharic_characters(text)
        # 3. Normalize numbers (Ge'ez to Arabic)
        text = self.normalize_numbers(text)
        # 4. Tokenize the text
        tokens = self.tokenize(text)

        # 5. Optional: Remove stopwords. For NER, it's often better to keep them for context.
        if REMOVE_STOPWORDS:
            tokens = self.remove_stopwords(tokens)

        # Join tokens back into a string. For NER, sequence is important.
        return " ".join(tokens)

if __name__ == '__main__':
    # Simple test cases for the preprocessor
    preprocessor = AmharicPreprocessor()

    print("--- Testing AmharicPreprocessor ---")

    test_texts = [
        "ጤና ይስጥልኝ! ይህ ምርጥ የሞባይል ስልክ በ1500 ብር ብቻ ይገኛል። አድራሻ: አዲስ አበባ። @exampleuser #ለሽያጭ",
        "የተለያዩ እቃዎች አሉን። ዛሬ በ5000 ብር እጅግ በጣም ጥሩ ላፕቶፕ። አድራሻችን ጎተራ።",
        "ይህ ጫማ በ፻ ብር ይገኛል። አድራሻ - ስድስት ኪሎ። www.example.com",
        "ጥሩ ዋጋ: 250 ብር + 50 ብር Delivery Fee 🚚📦",
        "የለም! መረጃ የለም።"
    ]

    for i, text in enumerate(test_texts):
        print(f"\nOriginal {i+1}: {text}")
        preprocessed_text = preprocessor.preprocess(text)
        print(f"Preprocessed {i+1}: {preprocessed_text}")

    # Test with REMOVE_STOPWORDS = True (temporarily override for demonstration)
    # Ensure to reset it if needed for main pipeline
    from scripts.config import REMOVE_STOPWORDS as initial_remove_stopwords
    temp_preprocessor = AmharicPreprocessor()
    temp_preprocessor.remove_stopwords = True # Directly set for testing
    print("\n--- Testing with Stopwords Removed (Temporary Override) ---")
    preprocessed_with_stopwords_removed = temp_preprocessor.preprocess(test_texts[0])
    print(f"Original: {test_texts[0]}")
    print(f"Preprocessed (Stopwords Removed): {preprocessed_with_stopwords_removed}")
    # Reset to original config value
    from scripts.config import REMOVE_STOPWORDS
    REMOVE_STOPWORDS = initial_remove_stopwords