import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Internal Medicine related titles

internal_medicine_variants = [
    r"\bInternal\s?Medicine\b",
    r"\bInternal\s?Med\b",

    # Common misspellings and case errors
    r"\bInteral\s?Medicine\b",
    r"\bInternel\s?Medicine\b",
    r"\bInternl\s?Medicine\b",
    r"\bInternall\s?Medicine\b",
    r"\bIntarnal\s?Medicine\b",
    r"\bInteranl\s?Medicine\b",
    r"\bInternist\b",

    # Spanish variants
    r"\bMedicina\s?Interna\b",
    r"\bMédico\s?Internista\b",
    r"\bEspecialista\s?en\s?Medicina\s?Interna\b",

    # Other possible variations
    r"\bInternal\s?Medicine\s?Specialist\b",
    r"\bInternal\s?Medicine\s?Physician\b",
    r"\bInternal\s?Medicine\s?Doctor\b",
    r"\bBoard\s?Certified\s?Internist\b",
    r"\bInterne En Medecine\b",
    r"\bInfectious Diseases\b",
    r"\bInternal Medicine\b",
    r"\bConsultant U Internal Medicine\b",
    r"\bConsultant Internal Medicine\b",
    r"\bInfectious Diseases Specialist\b",
    r"\bInfection Control Specialist\b",
    r"\bMedico Estetico  Specialista In Medicina Interna\b",
    r"\bInterne En Medecine\b",
    r"\bInternist\b",
    r"\bCardiology Internal Medicine\b",
    r"\bMedical Doctor Internal Medicine\b",
    r"\bGeneral Internal Medicine\b",
    r"\bToxopherese  Environmental Medicine  Internal Medicine  Anti-Aging Medicine\b",
    r"\bInternist- Aesthetic Medicine Master\b",
    r"\bMedicina Interna\b",
    r"\bInternal Medicine Dermatology\b",
    r"\bInternal Med\b",
    r"\bMedicina Interna Estetica\b",
    r"\bInternal Medicine & Lifestyle Medicine\b",
]

# Exact matches that should be updated
internal_medicine_exact_matches = {
    "Internal Medicine",
    "Internal Med",
    # Misspellings
    "Interal Medicine",
    "Internel Medicine",
    "Internl Medicine",
    "Internall Medicine",
    "Intarnal Medicine",
    "Interanl Medicine",
    "Internist",
    # Spanish variants
    "Medicina Interna",
    "Médico Internista",
    "Especialista en Medicina Interna",
    # Other possible variations
    "Internal Medicine Specialist",
    "Internal Medicine Physician",
    "Internal Medicine Doctor",
    "Board Certified Internist",
    'Infection Control',
    'infection control',
    'Int Medicine',
    'Osteopathic Physician Specializing In Functional Internal & Regenerative Medicine',
}

# Define patterns (these should NOT be changed)
internal_medicine_exclusions = {
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
    'Physician Recruiter - Otolaryngology Ent & Internal Medicine Consultant',
    'Physician Assistant In Internal Medicine',
    'Physician Recruiter - Anesthesiology Family & Internal Medicine Consultant',
}

# Create a mask for Internal Medicine
mask_internal_medicine = df['speciality'].str.contains('|'.join(internal_medicine_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(internal_medicine_exact_matches)
mask_internal_medicine_exclusions = df['speciality'].isin(internal_medicine_exclusions)

# Final mask: Select Internal Medicine
mask_internal_medicine_final = mask_internal_medicine & ~mask_internal_medicine_exclusions

# Store the original values that will be replaced
original_internal_medicine_values = df.loc[mask_internal_medicine_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_internal_medicine_final, 'speciality'] = 'Internal Medicine'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Internal Medicine", 'green'))
print(df.loc[mask_internal_medicine_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_internal_medicine_values = df.loc[mask_internal_medicine_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Internal Medicine", "cyan"))
for original_internal_medicine_value in original_internal_medicine_values:
    print(f"✅ {original_internal_medicine_value} → Internal Medicine")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Internal Medicine:", 'red'))
print(grouped_internal_medicine_values)

# Print summary
matched_count_internal_medicine = mask_internal_medicine_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Internal Medicine: "
        f"{matched_count_internal_medicine}",
        'red'))