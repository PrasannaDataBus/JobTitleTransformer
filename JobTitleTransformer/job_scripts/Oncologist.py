import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Oncologist related titles

oncologist_variants = [
    # Standard Titles & Abbreviations
    r"\bOncologist\b",
    r"\bMedical\s?Oncologist\b",
    r"\bClinical\s?Oncologist\b",
    r"\bRadiation\s?Oncologist\b",
    r"\bSurgical\s?Oncologist\b",
    r"\bPediatric\s?Oncologist\b",
    r"\bGynecologic\s?Oncologist\b",
    r"\bNeuro\s?Oncologist\b",
    r"\bBreast\s?Oncologist\b",
    r"\bThoracic\s?Oncologist\b",
    r"\bGenitourinary\s?Oncologist\b",
    r"\bGastrointestinal\s?Oncologist\b",

    # Misspellings & Typographical Errors
    r"\bOncolgist\b",
    r"\bOncolojist\b",
    r"\bOnclogist\b",
    r"\bOncologest\b",
    r"\bOncologis\b",
    r"\bOncologits\b",
    r"\bOnckologist\b",
    r"\bOnkologist\b",

    # Case Variations
    r"\boncologist\b",
    r"\bOncologist\b",
    r"\bONCOLOGIST\b",
    r"\bOncoLogist\b",

    # Spanish Variants
    r"\bOncólogo\b",
    r"\bMédico\s?Oncólogo\b",
    r"\bEspecialista\s?en\s?Oncología\b",
    r"\bOncólogo\s?Médico\b",
    r"\bOncólogo\s?Clínico\b",
    r"\bOncólogo\s?Radioterápico\b",
    r"\bOncólogo\s?Pediátrico\b",
    r"\bCirujano\s?Oncólogo\b",

    # Other Possible Variations (Including Doctor/Specialist Titles)
    r"\bOncology\s?Specialist\b",
    r"\bCancer\s?Specialist\b",
    r"\bTumor\s?Specialist\b",
    r"\bOncological\s?Surgeon\b",
    r"\bOncological\s?Physician\b",
    r"\bOnco\b",
    r"\bChief Pediatric Oncology\b",
]

# Exact matches that should be updated
oncologist_exact_matches = {
    "Oncologist",
    "Medical Oncologist",
    "Clinical Oncologist",
    "Radiation Oncologist",
    "Surgical Oncologist",
    "Pediatric Oncologist",
    "Gynecologic Oncologist",
    "Neuro Oncologist",
    "Breast Oncologist",
    "Thoracic Oncologist",
    "Genitourinary Oncologist",
    "Gastrointestinal Oncologist",
    "Oncolgist",
    "Oncolojist",
    "Onclogist",
    "Oncologest",
    "Oncologis",
    "Oncologits",
    "Onckologist",
    "Onkologist",
    "Oncólogo",
    "Médico Oncólogo",
    "Especialista en Oncología",
    "Oncólogo Médico",
    "Oncólogo Clínico",
    "Oncólogo Radioterápico",
    "Oncólogo Pediátrico",
    "Cirujano Oncólogo",
    "Oncology Specialist",
    "Cancer Specialist",
    "Tumor Specialist",
    "Oncological Surgeon",
    "Oncological Physician",
}

# # Define patterns (these should NOT be changed)
# oncologist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

oncologist_exclusions = {
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
    'Resident Physician - Radiation Oncologist',
}

# Create a mask for Oncologist
mask_oncologist = df['speciality'].str.contains('|'.join(oncologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(oncologist_exact_matches)

# mask_oncologist_exclusions = df['speciality'].str.contains(oncologist_exclusions, case=False, na=False, regex=True)
mask_oncologist_exclusions = df['speciality'].isin(oncologist_exclusions)

# Final mask: Select Oncologist
mask_oncologist_final = mask_oncologist & ~mask_oncologist_exclusions

# Store the original values that will be replaced
original_oncologist_values = df.loc[mask_oncologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_oncologist_final, 'speciality'] = 'Oncologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Oncologist", 'green'))
print(df.loc[mask_oncologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_oncologist_values = df.loc[mask_oncologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Oncologist", "cyan"))
for original_oncologist_value in original_oncologist_values:
    print(f"✅ {original_oncologist_value} → Oncologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Oncologist:", 'red'))
print(grouped_oncologist_values)

# Print summary
matched_count_oncologist = mask_oncologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Oncologist: "
        f"{matched_count_oncologist}",
        'red'))