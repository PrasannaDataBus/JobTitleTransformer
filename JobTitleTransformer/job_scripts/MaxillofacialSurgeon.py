import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Maxillofacial Surgeon related titles

maxillofacial_variants = [
    # Standard Titles & Abbreviations
    r"\bMaxillofacial\s?Surgeon\b",
    r"\bMaxillofacial\s?Surg\b",
    r"\bMaxFac\s?Surgeon\b",
    r"\bBucomaxillofacial Surgery\b",
    r"\bBuco Maxilo Facial\b",
    r"\bMaxillo Facial Surgeon\b",
    r"\bMaxillo-Facial Surgeon\b",
    r"\bMaxilo Facial\b",
    r"\bMaxilofacial Surgery\b",
    r"\bMaxillary Facial Surgery\b",
    r"\bChirurgie Maxillo-Faciale\b",
    r"\bChirurgie Maxillo Faciale\b",
    r"\bOrl Et Chirurgie Cervico Faciale\b",

    # Misspellings & Typographical Errors
    r"\bMaxilofacial\s?Surgeon\b",
    r"\bMaxillofascial\s?Surgeon\b",
    r"\bMaxillofacil\s?Surgeon\b",
    r"\bMaxillofascial\s?Surgon\b",
    r"\bMaxillofascial\s?Surgin\b",
    r"\bMaxillofacial\s?Surjeon\b",
    r"\bMaxillofacial\s?Surgan\b",
    r"\bMaxillofacial\s?Surgion\b",
    r"\bMaxillofacial\s?Suergeon\b",
    r"\bMaxillofacial\s?Srurgeon\b",
    r"\bMaxillofacial\s?Surrgeon\b",
    # Case Variations
    r"\bmaxillofacial surgeon\b",
    r"\bMaxillofacial surgeon\b",
    r"\bmaxillofacial Surgeon\b",
    r"\bMAXILLOFACIAL SURGEON\b",
    r"\bMaxillofaCial Surgeon\b",

    # Spanish Variants
    r"\bCirujano\s?Maxilofacial\b",
    r"\bEspecialista\s?Maxilofacial\b",
    r"\bMédico\s?Cirujano\s?Maxilofacial\b",
    r"\bDoctor\s?en\s?Cirugía\s?Maxilofacial\b",

    # Other Possible Variations (Including Doctor/Specialist Titles)
    r"\bCraniofacial\s?Surgeon\b",
    r"\bMaxillofacial Surgery\b",
]

# Exact matches that should be updated
maxillofacial_exact_matches = {
    "Maxillofacial Surgeon",
    "Maxillofacial Surg",
    "MaxFac Surgeon",
    "Maxilofacial Surgeon",
    "Maxillofascial Surgeon",
    "Maxillofacil Surgeon",
    "Maxillofascial Surgon",
    "Maxillofascial Surgin",
    "Maxillofacial Surjeon",
    "Maxillofacial Surgan",
    "Maxillofacial Surgion",
    "Maxillofacial Suergeon",
    "Maxillofacial Srurgeon",
    "Maxillofacial Surrgeon",
    "Cirujano Maxilofacial",
    "Especialista Maxilofacial",
    "Médico Cirujano Maxilofacial",
    "Doctor en Cirugía Maxilofacial",
    "Craniofacial Surgeon",
    'Maxillofacial',
    'Max Fax',
}

# Define patterns (these should NOT be changed)
maxillofacial_exclusions = r'\b(?:Oral)\b'

# Create a mask for Maxillofacial Surgeon
mask_maxillofacial = df['speciality'].str.contains('|'.join(maxillofacial_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(maxillofacial_exact_matches)
mask_maxillofacial_exclusions = df['speciality'].str.contains(maxillofacial_exclusions, case=False, na=False, regex=True)

# Final mask: Select Maxillofacial Surgeon
mask_maxillofacial_final = mask_maxillofacial & ~mask_maxillofacial_exclusions

# Store the original values that will be replaced
original_maxillofacial_values = df.loc[mask_maxillofacial_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_maxillofacial_final, 'speciality'] = 'Maxillofacial Surgeon'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Maxillofacial Surgeon", 'green'))
print(df.loc[mask_maxillofacial_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_maxillofacial_values = df.loc[mask_maxillofacial_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Maxillofacial Surgeon", "cyan"))
for original_maxillofacial_value in original_maxillofacial_values:
    print(f"✅ {original_maxillofacial_value} → Maxillofacial Surgeon")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Maxillofacial Surgeon:", 'red'))
print(grouped_maxillofacial_values)

# Print summary
matched_count_maxillofacial = mask_maxillofacial_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Maxillofacial Surgeon: "
        f"{matched_count_maxillofacial}",
        'red'))