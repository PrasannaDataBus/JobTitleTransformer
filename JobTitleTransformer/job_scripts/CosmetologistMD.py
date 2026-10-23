import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Cosmetologist MD related titles

cosmetologist_md_variants = [
    # Standard title variations
    r"\bCosmetologist\s?MD\b",
    r"\bMD\s?Cosmetologist\b",
    r"\bDoctor\s?of\s?Cosmetology\b",
    r"\bCosmetic\s?Doctor\b",
    r"\bMedical\s?Cosmetologist\b",
    r"\bCosmetologist\b",
    r"\bCosmiatry\b",
    r"\bVrach-Kosmetolog\b",
    r"\bCosmeologist\b",

    # Common misspellings and case mistakes
    r"\bCosmotologist\s?MD\b",
    r"\bCosmetoligist\s?MD\b",
    r"\bCosmetologist\s?M\.?D\.?\b",
    r"\bCosmatologist\s?MD\b",
    r"\bMD\s?Cosmotologist\b",

    # Variants in Spanish and other languages
    r"\bCosmetólogo\s?MD\b",
    r"\bMédico\s?Cosmetólogo\b",
    r"\bDoctor\s?en\s?Cosmetología\b",

    # Other possible variations
    r"\bBoard\s?-?\s?Certified\s?Cosmetologist\s?MD\b",
    r"\bAesthetic\s?Physician\s?\(Cosmetology\)\b",

    # Standard title variations
    r"\bCosmetologist\b",
    r"\bCosmetic\s?Specialist\b",

    # Common misspellings and case mistakes
    r"\bCosmotologist\b",
    r"\bCosmetoligist\b",
    r"\bCosmatologist\b",

    # Variants in Spanish and other languages
    r"\bCosmetólogo\b",
    r"\bEspecialista\s?en\s?Cosmetología\b",

    # Other possible variations
    r"\bProfessional\s?Cosmetologist\b",
    r"\bLicensed\s?Cosmetologist\b",
    r"\bCosmetology\b",
    r"\bCosmetic Medicine\b",
    r"\bSosmetologist\b",
    r"\bCosmetologie\b",
    r"\bArsthetician Cosemtologist\b",
    r"\bKosmetolog Feldsher\b",
]

# Exact matches that should be updated
cosmetologist_md_exact_matches = {
    r"\bCosmotologist\s?MD\b",
    r"\bCosmetoligist\s?MD\b",
    r"\bCosmetologist\s?M\.?D\.?\b",
    r"\bCosmatologist\s?MD\b",
    r"\bMD\s?Cosmotologist\b",
    r"\bCosmetólogo\s?MD\b",
    r"\bMédico\s?Cosmetólogo\b",
    r"\bDoctor\s?en\s?Cosmetología\b",
    r"\bCosmotologist\b",
    r"\bCosmetoligist\b",
    r"\bCosmatologist\b",
    r"\bCosmetólogo\b",
    r"\bEspecialista\s?en\s?Cosmetología\b",
    r"\bCosmetology\b",
    r"\bCosmetic Medicine\b",
    'Kosmetolog',
    'Medical Micropigmentologist',
}

# Define patterns (these should NOT be changed)
cosmetologist_md_exclusions = {
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
    'Aesthetic Resident',
    'Cosmetology Nurse',
    'Cosmetologist Student Of Medical Faculty',
    'Cosmetologist & Studing Nurse',
    'Cosmetologist & Esthetician',
    'Beautician Cosmetologist',
    'Cosmetologist Esthetician',
    'Cosmetology Instructor',
    'Cosmetology Teacher',
    'Instructor Of Cosmetology',
    'Supervisor Theatrical Cosmetology',
    'Vocational Instructor Of Cosmetology',
    'Cosmetology Educator',
    'Teacher Cosmetology',
    'Hairdressing & Cosmetology Teacher',
    'Ems& Cosmetology Licensing Aide Professional',
    'High School Cosmetology Instructor',
    'Cosmetology Career Technology Instructor',
    'Division Manager Licensing For The Mn Board Of Cosmetology',
}

# Create a mask for cosmetologist_md
mask_cosmetologist_md = df['speciality'].str.contains('|'.join(cosmetologist_md_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(cosmetologist_md_exact_matches)
mask_cosmetologist_md_exclusions = df['speciality'].isin(cosmetologist_md_exclusions)

# Final mask: Select cosmetologist_md
mask_cosmetologist_md_final = mask_cosmetologist_md & ~mask_cosmetologist_md_exclusions

# Store the original values that will be replaced
original_cosmetologist_md_values = df.loc[mask_cosmetologist_md_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_cosmetologist_md_final, 'speciality'] = 'Cosmetologist MD'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Cosmetologist MD", 'green'))
print(df.loc[mask_cosmetologist_md_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_cosmetologist_md_values = df.loc[mask_cosmetologist_md_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Cosmetologist MD", "cyan"))
for original_cosmetologist_md_value in original_cosmetologist_md_values:
    print(f"✅ {original_cosmetologist_md_value} → Cosmetologist MD")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Cosmetologist MD:", 'red'))
print(grouped_cosmetologist_md_values)

# Print summary
matched_count_cosmetologist_md = mask_cosmetologist_md_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Cosmetologist MD: "
        f"{matched_count_cosmetologist_md}",
        'red'))