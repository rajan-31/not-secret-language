# lang_generator.py

import nltk
import random
import json

# Download NLTK words list
nltk.download('words')
from nltk.corpus import words

def generate_language_mapping():
    # Generate the word list and shuffle for mapping
    english_words = list(set(words.words()))
    random.seed(42)  # for reproducibility
    secret_words = english_words.copy()
    random.shuffle(secret_words)

    # Create the secret mapping
    mapping = dict(zip(english_words, secret_words))
    reverse_mapping = {v: k for k, v in mapping.items()}

    # Save the dictionary to a JSON file
    with open("secret_dict.json", "w") as f:
        json.dump(mapping, f)

    return mapping, reverse_mapping

# Call the function to generate mappings and save them
if __name__ == "__main__":
    generate_language_mapping()
