import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Dental Assistant related titles

dental_assistant_variants = [
    # Standard title variations
    r"\bDental\s?Assistant\b",
    r"\bDental\s?Tech\b",
    r"\bDental\s?Nurse\b",
    r"\bDental\s?Hygienist\b",
    r"\bOral\s?Health\s?Assistant\b",
    r"\bDental\s?Support\s?Staff\b",

    # Common misspellings and case mistakes
    r"\bDentel\s?Assistant\b",
    r"\bDantal\s?Assistant\b",
    r"\bDentel\s?Tech\b",
    r"\bDantal\s?Nurse\b",

    # Variants in Spanish and other languages
    r"\bAsistente\s?Dental\b",
    r"\bAyudante\s?Dental\b",
    r"\bAuxiliar\s?Dental\b",
    r"\bTécnico\s?Dental\b",
    r"\bHigienista\s?Dental\b",

    # Other possible variations
    r"\bCertified\s?Dental\s?Assistant\b",
    r"\bLicensed\s?Dental\s?Assistant\b",
    r"\bRegistered\s?Dental\s?Assistant\b",
    r"\bDental Assistant\b",
]

# Exact matches that should be updated
dental_assistant_exact_matches = {
    r"\bDentel\s?Assistant\b",
    r"\bDantal\s?Assistant\b",
    r"\bDentel\s?Tech\b",
    r"\bDantal\s?Nurse\b",
    r"\bAsistente\s?Dental\b",
    r"\bAyudante\s?Dental\b",
    r"\bAuxiliar\s?Dental\b",
    r"\bTécnico\s?Dental\b",
    r"\bHigienista\s?Dental\b",
    r"\bDental Clinic\b",
    r"\bDental Service Assistant Chief\b",   
}

# Define patterns (these should NOT be changed)
dental_assistant_exclusions = {
    'Resident',
    'resident',
    'student',
    'Trainee',
    'Resident Doctor',
    'Resident Physician',
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
    'Aesthetic Resident'
}

# Create a mask for Dental Assistant
mask_dental_assistant = df['speciality'].str.contains('|'.join(dental_assistant_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(dental_assistant_exact_matches)
mask_dental_assistant_exclusions = df['speciality'].isin(dental_assistant_exclusions)

# Final mask: Select Dental Assistant
mask_dental_assistant_final = mask_dental_assistant & ~mask_dental_assistant_exclusions

# Store the original values that will be replaced
original_dental_assistant_values = df.loc[mask_dental_assistant_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_dental_assistant_final, 'speciality'] = 'Dental Assistant'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Dental Assistant", 'green'))
print(df.loc[mask_dental_assistant_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_dental_assistant_values = df.loc[mask_dental_assistant_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Dental Assistant", "cyan"))
for original_dental_assistant_value in original_dental_assistant_values:
    print(f"✅ {original_dental_assistant_value} → Dental Assistant")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Dental Assistant:", 'red'))
print(grouped_dental_assistant_values)

# Print summary
matched_count_dental_assistant = mask_dental_assistant_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Dental Assistant: "
        f"{matched_count_dental_assistant}",
        'red'))