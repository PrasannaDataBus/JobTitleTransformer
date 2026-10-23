import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Dental Surgeon related titles

dental_surgeon_variants = [
    # Standard title variations
    r"\bDental\s?Surgeon\b",
    r"\bCosmetic\s?Dental\s?Surgeon\b",
    r"\bGeneral\s?Dental\s?Surgeon\b",
    r"\bDDS\b",
    r"\bD D S\b",
    r"\bCosmetic Dentition\b",
    r"\bDental Surgron\b",
    r"\bDentistDental Surgeon\b",
    r"\bCirurgia Dentista\b",
    r"\bDentist Surgeon\b",
    r"\bCirurgiao Dentista\b",
    r"\bFarmacist & Dentist Surgery\b",
    r"\bChirurgien Dentiste\b",
    r"\bCirujana Dentista\b",
    r"\bCirugia Dentista\b",
    r"\bCirurgia-Dentista\b",
    r"\bDental Surgery\b",
    r"\bCirugia Dentista Hof\b",
    r"\bDental Surgey\b",

    # Common misspellings and case mistakes
    r"\bDentel\s?Surgeon\b",

    # Variants in Spanish and other languages
    r"\bCirujano\s?Dental\b",
    r"\bCirujano\s?Dentista\b",

    # Other possible variations (including specialist forms)
    r"\bCertified\s?Dental\s?Surgeon\b",
    r"\bLicensed\s?Dental\s?Surgeon\b",
    r"\bSpecialist\s?Dental\s?Surgeon\b",
    r"\bRegistered\s?Dental\s?Surgeon\b",
]

# Exact matches that should be updated
dental_surgeon_exact_matches = {
    r"\bDentel\s?Surgeon\b",
    r"\bCirujano\s?Dental\b",
    r"\bCirujano\s?Dentista\b",
}

# Define patterns (these should NOT be changed)
dental_surgeon_exclusions = [
    r"\bMaxillo\s?Facial\b",
    r"\bMaxillo-Facial\b"
] # maxillo variants

# Create a mask for Dental Surgeon
mask_dental_surgeon = df['speciality'].str.contains('|'.join(dental_surgeon_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(dental_surgeon_exact_matches)
mask_dental_surgeon_exclusions = df['speciality'].isin(dental_surgeon_exclusions)

# Final mask: Select Dental Surgeon
mask_dental_surgeon_final = mask_dental_surgeon & ~mask_dental_surgeon_exclusions

# Store the original values that will be replaced
original_dental_surgeon_values = df.loc[mask_dental_surgeon_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_dental_surgeon_final, 'speciality'] = 'Dental Surgeon'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Dental Surgeon", 'green'))
print(df.loc[mask_dental_surgeon_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_dental_surgeon_values = df.loc[mask_dental_surgeon_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Dental Surgeon", "cyan"))
for original_dental_surgeon_value in original_dental_surgeon_values:
    print(f"✅ {original_dental_surgeon_value} → Dental Surgeon")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Dental Surgeon:", 'red'))
print(grouped_dental_surgeon_values)

# Print summary
matched_count_dental_surgeon = mask_dental_surgeon_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Dental Surgeon: "
        f"{matched_count_dental_surgeon}",
        'red'))