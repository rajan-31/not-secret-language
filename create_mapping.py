import nltk
from nltk.corpus import words
import json
import random

nltk.download('words')

# Load and prepare English words
english_words = [word.lower() for word in words.words() if word.isalpha()]
unique_words = list(set(english_words))
unique_words.sort()

# Create shuffled mapping
shuffled_words = unique_words.copy()
random.shuffle(shuffled_words)

# Create bidirectional mapping
secret_mapping = {orig: shuffled_words[i] for i, orig in enumerate(unique_words)}
reverse_mapping = {v: k for k, v in secret_mapping.items()}

# Save both mappings
with open('secret_mapping.json', 'w') as f:
    json.dump({'encode': secret_mapping, 'decode': reverse_mapping}, f)

print("Bidirectional mapping dictionary created!")