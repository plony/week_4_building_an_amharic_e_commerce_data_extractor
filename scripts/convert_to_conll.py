import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_LABELED_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, 'my_labeled_data_raw.txt') # Your manually created file
FINAL_CONLL_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, 'labeled_data_conll.txt') # The final CoNLL output file

def convert_to_conll_format(input_path, output_path):
    """
    Reads a raw labeled text file and converts it to a strict CoNLL format.
    Ensures each line has one token and one label, separated by a space,
    and messages are separated by a single blank line.
    """
    print(f"Reading raw labeled data from: {input_path}")
    cleaned_lines = []
    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip() # Remove leading/trailing whitespace
            if line:
                # Basic check for token and label presence
                parts = line.split(' ')
                if len(parts) >= 2:
                    token = parts[0]
                    label = parts[-1] # Take the last part as the label
                    cleaned_lines.append(f"{token} {label}")
                else:
                    print(f"Warning: Skipping malformed line (no token-label pair): '{line}'")
            else:
                cleaned_lines.append("") # Keep blank lines for message separation

    # Ensure consistent single blank lines between messages
    final_output_lines = []
    prev_blank = False
    for line in cleaned_lines:
        if line == "":
            if not prev_blank:
                final_output_lines.append(line)
            prev_blank = True
        else:
            final_output_lines.append(line)
            prev_blank = False

    # Ensure no leading/trailing blank lines
    while final_output_lines and final_output_lines[0] == "":
        final_output_lines.pop(0)
    while final_output_lines and final_output_lines[-1] == "":
        final_output_lines.pop()

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in final_output_lines:
            outfile.write(line + '\n')

    print(f"Successfully converted to CoNLL format and saved to: {output_path}")
    print("Please review the generated file for correctness.")

if __name__ == "__main__":
    convert_to_conll_format(RAW_LABELED_DATA_PATH, FINAL_CONLL_DATA_PATH)