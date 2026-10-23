import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Oculoplastic Surgeon related titles

oculoplastic_surgeon_variants = [
    # Standard Titles & Abbreviations
    r"\bOculoplastic\s?Surgeon\b",
    r"\bOculoplastics\s?Surgeon\b",
    r"\bOculo-Plastic\s?Surgeon\b",
    r"\bOphthalmic\s?Plastic\s?Surgeon\b",
    r"\bOrbital\s?Surgeon\b",
    r"\bOculofacial\s?Surgeon\b",
    r"\bEyelid\s?Surgeon\b",
    r"\bFacial\s?Oculoplastic\s?Surgeon\b",
    r"\bOculoplastic\s?Specialist\b",
    r"\bOculoplasty Surgeon\b",
    r"\bOphthalmologistOculoplastic Surgeon\b",
    r"\bOphthalmoplastic Surgery\b",
    r"\bOculoplastic\b",

    # Misspellings & Typographical Errors
    r"\bOcculoplastic\s?Surgeon\b",
    r"\bOculaplastic\s?Surgeon\b",
    r"\bOculoplastik\s?Surgeon\b",
    r"\bOculoplastic\s?Surgon\b",
    r"\bOculoplastic\s?Surgin\b",
    r"\bOculoplastic\s?Surjeon\b",
    r"\bOculoplastic\s?Surgan\b",
    r"\bOculoplastic\s?Surgion\b",
    r"\bOculoplastic\s?Suergeon\b",
    r"\bOculoplastic\s?Srurgeon\b",
    r"\bOculoplastic\s?Surrgeon\b",

    # Case Variations
    r"\boculoplastic surgeon\b",
    r"\bOculoplastic surgeon\b",
    r"\boculoplastic Surgeon\b",
    r"\bOCULOPLASTIC SURGEON\b",
    r"\bOculoPlastic Surgeon\b",

    # Spanish Variants
    r"\bCirujano\s?Oculoplástico\b",
    r"\bEspecialista\s?Oculoplástico\b",
    r"\bMédico\s?Cirujano\s?Oculoplástico\b",
    r"\bDoctor\s?en\s?Cirugía\s?Oculoplástica\b",
    r"\bCirujano\s?Plástico\s?Oftálmico\b",

    # Other Possible Variations (Including Doctor/Specialist Titles)
    r"\bEyelid\s?Plastic\s?Surgeon\b",
    r"\bOrbital\s?Facial\s?Plastic\s?Surgeon\b",
    r"\bOphthalmic\s?Cosmetic\s?Surgeon\b",
    r"\bPeriorbital\s?Surgeon\b",
    r"\bOculoplastics\b",
    r"\bAesthetic Medicine Oculoplasty  Ophtalmology\b",
    r"\bOculofacial Surgery\b",
]

# Exact matches that should be updated
oculoplastic_surgeon_exact_matches = {
    "Oculoplastic Surgeon",
    "Oculoplastics Surgeon",
    "Oculo-Plastic Surgeon",
    "Ophthalmic Plastic Surgeon",
    "Orbital Surgeon",
    "Oculofacial Surgeon",
    "Eyelid Surgeon",
    "Facial Oculoplastic Surgeon",
    "Oculoplastic Specialist",
    "Occuloplastic Surgeon",
    "Oculaplastic Surgeon",
    "Oculoplastik Surgeon",
    "Oculoplastic Surgon",
    "Oculoplastic Surgin",
    "Oculoplastic Surjeon",
    "Oculoplastic Surgan",
    "Oculoplastic Surgion",
    "Oculoplastic Suergeon",
    "Oculoplastic Srurgeon",
    "Oculoplastic Surrgeon",
    "Cirujano Oculoplástico",
    "Especialista Oculoplástico",
    "Médico Cirujano Oculoplástico",
    "Doctor en Cirugía Oculoplástica",
    "Cirujano Plástico Oftálmico",
    "Eyelid Plastic Surgeon",
    "Orbital Facial Plastic Surgeon",
    "Ophthalmic Cosmetic Surgeon",
    "Periorbital Surgeon",
}

# # Define patterns (these should NOT be changed)
# oculoplastic_surgeon_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

oculoplastic_surgeon_exclusions = {
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
}

# Create a mask for Oculoplastic Surgeon
mask_oculoplastic_surgeon = df['speciality'].str.contains('|'.join(oculoplastic_surgeon_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(oculoplastic_surgeon_exact_matches)

# mask_oculoplastic_surgeon_exclusions = df['speciality'].str.contains(oculoplastic_surgeon_exclusions, case=False, na=False, regex=True)
mask_oculoplastic_surgeon_exclusions = df['speciality'].isin(oculoplastic_surgeon_exclusions)

# Final mask: Select Oculoplastic Surgeon
mask_oculoplastic_surgeon_final = mask_oculoplastic_surgeon & ~mask_oculoplastic_surgeon_exclusions

# Store the original values that will be replaced
original_oculoplastic_surgeon_values = df.loc[mask_oculoplastic_surgeon_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_oculoplastic_surgeon_final, 'speciality'] = 'Oculoplastic Surgeon'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Oculoplastic Surgeon", 'green'))
print(df.loc[mask_oculoplastic_surgeon_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_oculoplastic_surgeon_values = df.loc[mask_oculoplastic_surgeon_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Oculoplastic Surgeon", "cyan"))
for original_oculoplastic_surgeon_value in original_oculoplastic_surgeon_values:
    print(f"✅ {original_oculoplastic_surgeon_value} → Oculoplastic Surgeon")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Oculoplastic Surgeon:", 'red'))
print(grouped_oculoplastic_surgeon_values)

# Print summary
matched_count_oculoplastic_surgeon = mask_oculoplastic_surgeon_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Oculoplastic Surgeon: "
        f"{matched_count_oculoplastic_surgeon}",
        'red'))