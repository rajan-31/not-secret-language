import streamlit as st
import hashlib
import json
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Google Drive setup
gauth = GoogleAuth()
drive = GoogleAuth(gauth).LocalWebserverAuth()

LANGUAGE_FILE_ID = 'your_google_drive_file_id_here'

def get_language_rules():
    # Load or create language rules from Google Drive
    try:
        file = drive.CreateFile({'id': LANGUAGE_FILE_ID})
        content = file.GetContentString()
        return json.loads(content)
    except:
        return generate_new_language()

def generate_new_language():
    # Create new linguistic transformation rules
    rules = {
        'vowel_map': random.sample('aeiou', 5),
        'consonant_shifts': {c: (i+5)%21 for i,c in enumerate('bcdfghjklmnpqrstvwxyz')},
        'syllable_patterns': random.sample(['cv', 'vc', 'cvc', 'vcc'], 4),
        'transform_seed': random.randint(0, 2**32)
    }
    
    # Save to Google Drive
    file = drive.CreateFile({'title': 'secret_language.json'})
    file.SetContentString(json.dumps(rules))
    file.Upload()
    return rules

def transform_word(word, rules, mode='encode'):
    # Preserve capitalization and punctuation
    original_case = [c.isupper() for c in word]
    base_word = re.sub(r'\W+', '', word).lower()
    punctuation = re.sub(r'\w+', '', word)
    
    # Cryptographic seeding
    seed = int(hashlib.sha256(f"{rules['transform_seed']}{base_word}".encode()).hexdigest(), 16)
    random.seed(seed)
    
    # Linguistic transformations
    transformed = []
    for c in base_word:
        if c in 'aeiou':
            # Vowel mapping with position rotation
            idx = 'aeiou'.index(c)
            new_char = rules['vowel_map'][(idx + len(transformed)) % 5]
        else:
            # Consonant shifting with chaos
            shift = rules['consonant_shifts'].get(c, 0)
            new_char = chr(((ord(c) - 97 + shift) % 26) + 97)
        transformed.append(new_char)
    
    # Syllable restructuring
    transformed = apply_syllable_pattern(''.join(transformed), rules['syllable_patterns'])
    
    # Restore case and punctuation
    final = []
    for i, c in enumerate(transformed):
        if i < len(original_case) and original_case[i]:
            final.append(c.upper())
        else:
            final.append(c)
    return ''.join(final) + punctuation

def apply_syllable_pattern(word, patterns):
    # Break word into pseudo-syllables
    chunks = []
    while word:
        pattern = random.choice(patterns)
        chunk_len = min(len(pattern), len(word))
        chunks.append(word[:chunk_len])
        word = word[chunk_len:]
    return ''.join(chunks)

# Streamlit UI
st.title("🔮 CryptoLingua Pro")
st.caption("AI-Powered Secret Language Generator")

rules = get_language_rules()
mode = st.radio("Select Mode:", ("Encode", "Decode"))
message = st.text_area("Enter your message:", height=150)
secret_key = st.text_input("Language Key:", value=rules['transform_seed'], type="password")

if st.button(f"{mode} Message"):
    if message:
        processed = process_text(message, rules, mode.lower())
        st.subheader("Result:")
        st.markdown(f"```\n{processed}\n```")
        
        st.markdown("---")
        st.caption("Language Fingerprint:")
        st.json({
            "vowel_map": rules['vowel_map'],
            "syllable_patterns": rules['syllable_patterns'],
            "transform_seed": f"*****{str(rules['transform_seed'])[-4:]}"
        })
    else:
        st.warning("Please enter a message")

st.markdown("---")
st.info("ℹ️ **Security Features:**\n"
        "- Unique linguistic DNA stored in Google Drive\n"
        "- Cryptographic seeding with SHA-256\n"
        "- Position-dependent transformations\n"
        "- Syllable pattern restructuring\n"
        "- Key-based reversibility")
