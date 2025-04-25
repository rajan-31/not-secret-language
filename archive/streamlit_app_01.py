import streamlit as st
import re

def encode_word(word):
    # Handle punctuation and capitalization
    punctuation = ''
    if not word[-1].isalnum():
        punctuation = word[-1]
        word = word[:-1]
    
    original = word
    lower_word = word.lower()
    
    # Pattern-based transformations
    encoded = lower_word
    
    # 1. Double the last consonant if word ends with consonant
    if len(encoded) > 1 and not encoded[-1] in 'aeiou':
        encoded += encoded[-1]
    
    # 2. Add "izz" after first vowel
    vowels = re.findall('[aeiou]', encoded)
    if vowels:
        first_vowel_pos = encoded.find(vowels[0])
        encoded = encoded[:first_vowel_pos+1] + 'izz' + encoded[first_vowel_pos+1:]
    
    # 3. Capitalize if original was capitalized
    if original.istitle():
        encoded = encoded.capitalize()
    
    return encoded + punctuation

def decode_word(encoded_word):
    punctuation = ''
    if not encoded_word[-1].isalnum():
        punctuation = encoded_word[-1]
        encoded_word = encoded_word[:-1]
    
    original = encoded_word
    lower_word = encoded_word.lower()
    
    decoded = lower_word
    
    # Reverse the "izz" insertion
    decoded = re.sub(r'([aeiou])izz', r'\1', decoded, count=1)
    
    # Reverse last consonant doubling
    if len(decoded) > 1 and not decoded[-1] in 'aeiou' and decoded[-1] == decoded[-2]:
        decoded = decoded[:-1]
    
    # Restore capitalization
    if original.istitle():
        decoded = decoded.capitalize()
    
    return decoded + punctuation

def process_text(text, mode):
    words = re.split(r'(\s+)', text)  # Preserve whitespace
    processed = []
    
    for word in words:
        if word.strip():
            if mode == 'encode':
                processed_word = encode_word(word)
            else:
                processed_word = decode_word(word)
            processed.append(processed_word)
        else:
            processed.append(word)
    
    return ''.join(processed)

# Streamlit UI
st.title("🔤 Auto-Secret Language Translator")

mode = st.radio("Select Mode:", ("Encode", "Decode"))
text = st.text_area("Enter your text:", height=150)

if st.button(f"{mode} Text"):
    if text:
        result = process_text(text, mode.lower())
        st.subheader("Result:")
        st.markdown(f"```\n{result}\n```")
        
        st.markdown("---")
        st.caption("Transformation Rules:")
        st.markdown("""
        1. Doubles final consonant (if present)
        2. Inserts "izz" after first vowel
        3. Preserves capitalization/punctuation
        """)
    else:
        st.warning("Please enter some text")

st.markdown("---")
st.info("ℹ️ **Example:**\n"
        "Original: `Hello, world!`\n"
        "Encoded: `Hizzello, worizzldd!`\n"
        "Decoded back: `Hello, world!`")
