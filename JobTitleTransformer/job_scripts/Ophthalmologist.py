import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Ophthalmologist related titles

ophthalmologist_variants = [
    # Standard Titles & Abbreviations
    r"\bOphthalmologist\b",
    r"\bOphthalmology\s?Specialist\b",
    r"\bEye\s?Specialist\b",
    r"\bEye\s?Doctor\b",
    r"\bOphthalmic\s?Surgeon\b",
    r"\bOphthalmology\b",

    # Misspellings & Typographical Errors
    r"\bOpthalmologist\b",
    r"\bOphtalmologist\b",
    r"\bOphthomologist\b",
    r"\bOphthalmologis\b",
    r"\bOpthomoligist\b",
    r"\bOphthalmalogist\b",
    r"\bOphthalmoloist\b",

    # Case Variations
    r"\bophthalmologist\b",
    r"\bOphthalmologist\b",
    r"\bOPHTHALMOLOGIST\b",
    r"\bOphthaLmologist\b",

    # Spanish Variants
    r"\bOftalmólogo\b",
    r"\bMédico\s?Oftalmólogo\b",
    r"\bEspecialista\s?en\s?Oftalmología\b",
    r"\bOftalmólogo\s?Médico\b",
    r"\bOftalmólogo\s?Quirúrgico\b",
    r"\bOftalmólogo\s?Pediátrico\b",
    r"\bOftalmólogo\s?Clínico\b",

    # Other Possible Variations (Including Doctor forms, Specialist forms)
    r"\bEye\s?Doctor\b",
    r"\bOphthalmic\s?Physician\b",
    r"\bOphthalmic\s?Specialist\b",
    r"\bOptometrist\b",  # Can be confused with Ophthalmologists in some regions
    r"\bVision\s?Specialist\b",
    r"\bOfthalmology\b",
    r"\bOphthalmogist\b",
    r"\bOphthalmolohist\b",
    r"\bOftalmologia\b",
]

# Exact matches that should be updated
ophthalmologist_exact_matches = {
    "Ophthalmologist",
    "Ophthalmology Specialist",
    "Eye Specialist",
    "Eye Doctor",
    "Ophthalmic Surgeon",
    "Opthalmologist",
    "Ophtalmologist",
    "Ophthomologist",
    "Ophthalmologis",
    "Opthomoligist",
    "Ophthalmalogist",
    "Ophthalmoloist",
    "Oftalmólogo",
    "Médico Oftalmólogo",
    "Especialista en Oftalmología",
    "Oftalmólogo Médico",
    "Oftalmólogo Quirúrgico",
    "Oftalmólogo Pediátrico",
    "Oftalmólogo Clínico",
    "Ophthalmic Physician",
    "Ophthalmic Specialist",
    "Optometrist",
    "Vision Specialist",
    'Ophtalmo',
}

# # Define patterns (these should NOT be changed)
# ophthalmologist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

ophthalmologist_exclusions = {
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
    'Ophthalmology Resident',
    'Doctor Resident Of Ophthalmology',
}

# Create a mask for Ophthalmologist
mask_ophthalmologist = df['speciality'].str.contains('|'.join(ophthalmologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(ophthalmologist_exact_matches)

# mask_ophthalmologist_exclusions = df['speciality'].str.contains(ophthalmologist_exclusions, case=False, na=False, regex=True)
mask_ophthalmologist_exclusions = df['speciality'].isin(ophthalmologist_exclusions)

# Final mask: Select Ophthalmologist
mask_ophthalmologist_final = mask_ophthalmologist & ~mask_ophthalmologist_exclusions

# Store the original values that will be replaced
original_ophthalmologist_values = df.loc[mask_ophthalmologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_ophthalmologist_final, 'speciality'] = 'Ophthalmologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Ophthalmologist", 'green'))
print(df.loc[mask_ophthalmologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_ophthalmologist_values = df.loc[mask_ophthalmologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Ophthalmologist", "cyan"))
for original_ophthalmologist_value in original_ophthalmologist_values:
    print(f"✅ {original_ophthalmologist_value} → Ophthalmologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Ophthalmologist:", 'red'))
print(grouped_ophthalmologist_values)

# Print summary
matched_count_ophthalmologist = mask_ophthalmologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Ophthalmologist: "
        f"{matched_count_ophthalmologist}",
        'red'))