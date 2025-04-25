import streamlit as st
import json
import re

def preserve_case(original, mapped):
    if original.isupper():
        return mapped.upper()
    elif original.istitle():
        return mapped.title()
    return mapped.lower()

# Load mappings
with open('secret_mapping.json', 'r') as f:
    mappings = json.load(f)
    encode_map = mappings['encode']
    decode_map = mappings['decode']

st.title("Secret Language Translator")

# Add mode selector
mode = st.radio("Choose mode:", ("Encode", "Decode"))

input_text = st.text_area(f"Enter text to {mode.lower()}:", height=150)

if input_text:
    current_map = encode_map if mode == "Encode" else decode_map
    tokens = re.findall(r"[a-zA-Z']+|[^a-zA-Z']+", input_text)
    
    translated = []
    for token in tokens:
        if re.fullmatch(r'^[a-zA-Z]+$', token):
            lower_token = token.lower()
            if lower_token in current_map:
                translated_word = preserve_case(token, current_map[lower_token])
                translated.append(translated_word)
            else:
                translated.append(token)
        else:
            translated.append(token)
    
    st.subheader("Result:")
    st.write(''.join(translated))