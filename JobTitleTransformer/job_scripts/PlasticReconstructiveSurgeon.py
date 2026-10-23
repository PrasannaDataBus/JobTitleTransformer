import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Plastic and Reconstructive Surgeon related titles

reconstructive_variants = [
    # Standard Titles & Variants
    r"\bPlastic and Reconstructive Surgeon\b",
    r"\bReconstructive Surgeon\b",
    r"\bAesthetic and Reconstructive Surgeon\b",
    r"\bCosmetic and Reconstructive Surgeon\b",
    r"\bReconstructive and Aesthetic Surgeon\b",
    r"Plastic & Reconstructive Surgery",
    r"\bOncoplastic Surgeon\b",
    r"\bPlastic Rekonstructive & Aesthetic Surgery\b",
    r"\bPlastic Reconstructive Aesthetic Surgery\b",
    r"\bChirurgie Plastique Et Reparatrice\b",

    # Misspellings & Typographical Errors
    r"\bPlasic and Reconstructive Surgeon\b",
    r"\bPlastic and Reconstuctive Surgeon\b",
    r"\bPlastic and Reconstructive Surgeoon\b",
    r"\bPlstic and Reconstructive Surgeon\b",
    r"\bPlstic and Reconstructive Surgon\b",
    r"\bPlastic and Reconstructuve Surgeon\b",

    # Case Variations
    r"\bplastic and reconstructive surgeon\b",
    r"\bPLASTIC AND RECONSTRUCTIVE SURGEON\b",
    r"\bPlAsTiC aND ReCoNsTrUcTiVe SuRgEoN\b",

    # Spanish Variants
    r"\bCirujano Plástico y Reconstructivo\b",
    r"\bCirujano Estético y Reconstructivo\b",
    r"\bCirujano Reconstructivo\b",

    # Other Possible Variations
    r"\bCosmetic Reconstructive Surgeon\b",
    r"\bReconstructive Surgery Specialist\b",
    r"\bReconstructive and Cosmetic Surgeon\b",
    r"\bPlastic & Reconstractive Surgeon\b",
    r"\bArmonizacion Orofacial\b",
    r"\bPlastic Aesthetic & Reconstructive Surgery\b",
    r"\bPlastic Reconstructive & Aesthetic Surgeon\b",
    r"\bPlastic Rekonstructive & Aesthetic Surgery\b",
    r"\bPlastic Reconstructive & Aesthetic Surgery\b",
    r"\bPlastic Reconstructive Aesthetic Surgery\b",
    r"\bSpecialist In Facial Harmonization\b",
]

# Exact matches that should be updated
reconstructive_exact_matches = {
    "Plastic and Reconstructive Surgeon",
    "Reconstructive Surgeon",
    "Aesthetic and Reconstructive Surgeon",
    "Cosmetic and Reconstructive Surgeon",
    "Reconstructive and Aesthetic Surgeon",
    "Plasic and Reconstructive Surgeon",
    "Plastic and Reconstuctive Surgeon",
    "Plastic and Reconstructive Surgeoon",
    "Plstic and Reconstructive Surgeon",
    "Plstic and Reconstructive Surgon",
    "Plastic and Reconstructuve Surgeon",
    "Cirujano Plástico y Reconstructivo",
    "Cirujano Estético y Reconstructivo",
    "Cirujano Reconstructivo",
    "Cosmetic Reconstructive Surgeon",
    "Reconstructive Surgery Specialist",
    "Reconstructive and Cosmetic Surgeon",
    'Plastic & Reconstrucitve Surgery',
    'Cirujana Plastica Y Reconstructiva'
}

# # Define patterns (these should NOT be changed)
# reconstructive_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

reconstructive_exclusions = {
    'Resident',
    'resident',
    'student',
    'Trainee',
    'Resident Doctor',
    'Resident ooPhysician',
    'Intern',
    'intern',
    'Medical Intern',
    'Fellow',
    'fellow',
    'Clinical Fellow',
    'Medical Student',
    'Clinical Trainee',
    'Trainee Doctor',
    'Trainee Physician',
    'Junior Doctor',
    'Postgraduate Trainee',
    'Aesthetic Fellow',
    'Aesthetic Trainee',
    'Aesthetic Medicine Fellow',
    'Aesthetic Resident',
    'A Professor Plastic & Reconstructive Surgery',
}

# Create a mask for Plastic and Reconstructive Surgeon
mask_reconstructive = df['speciality'].str.contains('|'.join(reconstructive_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(reconstructive_exact_matches)

# mask_reconstructive_exclusions = df['speciality'].str.contains(reconstructive_exclusions, case=False, na=False, regex=True)
mask_reconstructive_exclusions = df['speciality'].isin(reconstructive_exclusions)

# Final mask: Select Plastic and Reconstructive Surgeon
mask_reconstructive_final = mask_reconstructive & ~mask_reconstructive_exclusions

# Store the original values that will be replaced
original_reconstructive_values = df.loc[mask_reconstructive_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_reconstructive_final, 'speciality'] = 'Plastic and Reconstructive Surgeon'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Plastic and Reconstructive Surgeon", 'green'))
print(df.loc[mask_reconstructive_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_reconstructive_values = df.loc[mask_reconstructive_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Plastic and Reconstructive Surgeon", "cyan"))
for original_reconstructive_value in original_reconstructive_values:
    print(f"✅ {original_reconstructive_value} → Plastic and Reconstructive Surgeon")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Plastic and Reconstructive Surgeon:", 'red'))
print(grouped_reconstructive_values)

# Print summary
matched_count_reconstructive = mask_reconstructive_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Plastic and Reconstructive Surgeon: "
        f"{matched_count_reconstructive}",
        'red'))