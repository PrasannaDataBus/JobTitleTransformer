import sys
import os
import re
import pandas as pd
from termcolor import colored
from tabulate import tabulate as tab

# Test dataframe
df_test = df.copy()

# _encode_decode.py

ENCODE_DECODE_MAP = {
    "&Aacute;": "Á",
    "&aacute;": "á",
    "&Eacute;": "É",
    "&eacute;": "é",
    "&Iacute;": "Í",
    "&iacute;": "í",
    "&Oacute;": "Ó",
    "&oacute;": "ó",
    "&Uacute;": "Ú",
    "&uacute;": "ú",
    "&Ntilde;": "Ñ",
    "&ntilde;": "ñ",
    "&Ccedil;": "Ç",
    "&ccedil;": "ç",
    "&quot;": "\"",
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&uuml;": "ü",
    "&Uuml;": "Ü",
    "&szlig;": "ß",
}


# Function to replace encoded values
def decode_html_entities(value):
    if isinstance(value, str):  # Only process strings
        for encoded, decoded in ENCODE_DECODE_MAP.items():
            value = value.replace(encoded, decoded)
    return value  # Return the modified or original value


# Apply the function to all string columns in the DataFrame
df['speciality'] = df['speciality'].apply(decode_html_entities)

from unidecode import unidecode
import unicodedata
import html

# encode and decode
df['speciality'] = df['speciality'].apply(lambda x: unidecode(html.unescape(str(x))))

# Trim whitespace
df['speciality'] = df['speciality'].str.strip()

# Remove extra spaces, underscores, and incorrect separators
df['speciality'] = df['speciality'].replace({
    r'\s{2,}': ' ',  # Replace multiple spaces with a single space
    r'[_\.]': ' ',   # Replace underscores and dots with space
    r',\s*': ' ',    # Remove commas followed by space
    r'\s*/\s*': '/', # Trim spaces around slashes
    r'[¡’]': '',     # Remove unwanted characters
    r'\b(?:And|and|&Amp;|&amp;)\b': '&'  # Normalize 'And' variations
}, regex=True)

# Normalize accented characters
df['speciality'] = df['speciality'].apply(
    lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8')
    if isinstance(x, str) else x
)

# # Convert to title case
# df['speciality'] = df['speciality'].str.title()

# Tip: Use either one logical condition for the below normalize_text

# def normalize_text(text):
#     if isinstance(text, str):
#         # Normalize unicode characters (like accented characters)
#         text = unicodedata.normalize('NFKD', text)
#         # Remove special characters excluding '&' and '-'
#         text = text.encode('ascii', 'ignore').decode('utf-8')
#         # Remove unwanted special chars except for '&' and '-'
#         text = re.sub(r'[^\w\s&-]', '', text)
#         return text
#     return text


def normalize_text(text):
    if isinstance(text, str):
        # Normalize unicode characters (like accented characters)
        text = unicodedata.normalize('NFKD', text)
        # Remove unwanted special characters but add spaces where they were
        # First, replace unwanted characters with a space, then clean up the spaces
        text = re.sub(r'[^\w\s&-]', ' ', text)  # Replace non-alphanumeric with space
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Trim leading/trailing spaces
        text = text.strip()
        return text
    return text


df['speciality'] = df['speciality'].apply(normalize_text)  # Apply normalization

# Assuming your DataFrame is named df
# df['speciality'] = df['speciality'].str.strip()  # Trim leading and trailing spaces

# To handle Prime Data
# Apply transformation only where speciality starts with numbers
df['speciality'] = df['speciality'].apply(lambda x: re.sub(r'^\d+\s*', '', x) if isinstance(x, str) and re.match(r'^\d+', x) else x)

# Create clean working columns
df['speciality'] = df['speciality'].fillna('Other').astype(str).str.strip()
df['speciality'] = df['speciality'].astype(str).str.strip().replace(['-', 'nan', '', 'Unknown', 'Unspecified Specialty'], 'Other')

# Filtering logic: Keep only non valid records in df_other dataframe
df_other = df[
    df['speciality'].astype(str).str.strip().isin([
        'Other',
        'Unknown',
        'None',
        'Medical Aesthetics Industry',
        'Other Industry',
        'Other Please specify',
        'Other please specify',
        'Dp',
        '-'
    ]) |  # Remove specified values
    df['speciality'].astype(str).str.match(r'^\d+$') |  # numbers only
    df['speciality'].astype(str).str.match(r'^[A-Za-z]$')  # single letters
].reset_index(drop=True)

# Print low-confidence sample
print(colored("\nRecords where Job Title is Other, Unknown, None or non relevant", "red", attrs=["bold"]))
print(tab(df_other.head(10), headers='keys', tablefmt='psql'))
print(colored(f"\nRecords where Job Title is Other, Unknown, None or non relevant: {len(df_other)}", "red"))

# Filtering logic: Keep only valid records in df
df = df[
    ~df['speciality'].astype(str).str.strip().isin([
        'Other',
        'Unknown',
        'None',
        'Medical Aesthetics Industry',
        'Other Industry',
        'Other Please specify',
        'Other please specify',
        'Dp',
        '-'
    ]) &  # Remove specified values
    ~df['speciality'].astype(str).str.match(r'^\d+$') &  # Remove numbers only
    ~df['speciality'].astype(str).str.match(r'^[A-Za-z]$')  # Remove single letters
].reset_index(drop=True)

# Print count of valid non-matching job titles that will be sent for machine learning process
print(colored(f"\nCount of records that will be sent for transformation stages: {df.shape[0]}", 'red'))

# Creating a copy column original_specialty to apply Machine Learning
df['original_speciality'] = df['speciality'].copy()


