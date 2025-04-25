# lang_utils.py

import json

# Load the secret dictionary from the file
def load_mappings():
    with open("secret_dict.json", "r") as f:
        mapping = json.load(f)
    reverse_mapping = {v: k for k, v in mapping.items()}
    return mapping, reverse_mapping

# Encode function
def encode(text, mapping):
    words = text.split()  # Split text into words, keeping original case
    encoded_words = [mapping.get(word.lower(), word) for word in words]  # Map to secret words
    return ' '.join(encoded_words)

# Decode function
def decode(text, reverse_mapping):
    words = text.split()  # Split text into words, keeping original case
    decoded_words = [reverse_mapping.get(word.lower(), word) for word in words]  # Reverse map
    return ' '.join(decoded_words)

# Example usage
if __name__ == "__main__":
    mapping, reverse_mapping = load_mappings()
    original_text = "Sagar is very smart. Just kidding..LOL"
    encoded_text = encode(original_text, mapping)
    decoded_text = decode(encoded_text, reverse_mapping)

    print("Original Text:", original_text)
    print("Encoded Text:", encoded_text)
    print("Decoded Text:", decoded_text)
