import streamlit as st
import hashlib
import json
import random
import os
import re

LANGUAGE_FILE = "secret_language_rules.json"

def get_language_rules():
    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, 'r') as f:
                return json.load(f)
        except:
            return generate_new_language()
    return generate_new_language()

def generate_new_language():
    rules = {
        'vowel_map': random.sample('aeiou', 5),
        'consonant_shifts': {c: (i+5)%21 for i,c in enumerate('bcdfghjklmnpqrstvwxyz')},
        'reverse_shifts': {(i+5)%21: c for i,c in enumerate('bcdfghjklmnpqrstvwxyz')},
        'syllable_patterns': random.sample(['cv', 'vc', 'cvc', 'vcc'], 4),
        'transform_seed': random.randint(0, 2**32)
    }
    with open(LANGUAGE_FILE, 'w') as f:
        json.dump(rules, f)
    return rules

def transform_word(word, rules, mode='encode'):
    original_case = [c.isupper() for c in word]
    base_word = re.sub(r'\W+', '', word).lower()
    punctuation = re.sub(r'\w+', '', word)
    
    seed = int(hashlib.sha256(f"{rules['transform_seed']}{base_word}".encode()).hexdigest(), 16)
    random.seed(seed)
    
    transformed = []
    for c in base_word:
        if c in 'aeiou':
            idx = 'aeiou'.index(c)
            if mode == 'encode':
                new_char = rules['vowel_map'][(idx + len(transformed)) % 5]
            else:
                original_idx = rules['vowel_map'].index(c)
                new_char = 'aeiou'[(original_idx - len(transformed)) % 5]
        else:
            if mode == 'encode':
                shift = rules['consonant_shifts'].get(c, 0)
                new_char = chr(((ord(c) - 97 + shift) % 26) + 97)
            else:
                original_ord = (ord(c) - 97) % 26
                new_char = rules['reverse_shifts'].get(original_ord, c)
        transformed.append(new_char)
    
    transformed = apply_reversible_syllables(''.join(transformed), rules['syllable_patterns'], mode)
    
    final = []
    for i, c in enumerate(transformed):
        if i < len(original_case) and original_case[i]:
            final.append(c.upper())
        else:
            final.append(c.lower())
    return ''.join(final) + punctuation

def apply_reversible_syllables(word, patterns, mode):
    chunks = []
    remaining = word
    pattern_index = 0
    
    while remaining:
        pattern = patterns[pattern_index % len(patterns)]
        chunk_len = min(len(pattern), len(remaining))
        chunks.append(remaining[:chunk_len])
        remaining = remaining[chunk_len:]
        pattern_index += 1
    
    return ''.join(chunks) if mode == 'encode' else ''.join(chunks[::-1])

def process_text(text, rules, mode):
    words = re.findall(r'\w+\W*|\W+', text)
    return ''.join([transform_word(word, rules, mode) for word in words])

# Streamlit UI
st.title("🔮 Secret Language Translator")
st.markdown("---")

rules = get_language_rules()

mode = st.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
message = st.text_area("Enter your message:", height=150)
secret_key = st.text_input("Language Key:", value=str(rules['transform_seed']), type="password")

if st.button(f"{mode} Message"):
    if message:
        processed = process_text(message, rules, mode.lower())
        st.subheader("Result:")
        st.markdown(f"```\n{processed}\n```")
        
        st.markdown("---")
        with st.expander("Language Settings"):
            st.json({
                "vowel_map": rules['vowel_map'],
                "syllable_patterns": rules['syllable_patterns'],
                "transform_seed": f"*****{str(rules['transform_seed'])[-4:]}"
            })
    else:
        st.warning("Please enter a message")

st.markdown("---")
st.info("💡 **Tip:** Save your Language Key to decode messages later!")