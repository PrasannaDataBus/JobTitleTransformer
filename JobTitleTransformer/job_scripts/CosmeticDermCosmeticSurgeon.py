import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Cosmetic Dermatologist related titles

cosmetic_dermatologist_variants = [
    # Standard title variations
    r"\bCosmetic\s?Dermatologist\b",
    r"\bDermatologist\s?Cosmetic\b",
    r"\bCosmetic\s?Skin\s?Specialist\b",
    r"\bDoctor\s?of\s?Cosmetic\s?Dermatology\b",
    r"\bCosmetic\s?Skin\s?Doctor\b",
    r"\bAesthetic\s?Dermatologist\b",
    r"\bSkin\s?Care\s?Specialist\b",

    # Common misspellings and case mistakes
    r"\bCosmetic\s?Dermotologist\b",
    r"\bCosmetick\s?Dermatologist\b",
    r"\bCosmotik\s?Dermatologist\b",
    r"\bKosmetic\s?Dermatologist\b",
    r"\bCosmetic\s?Dermetologist\b",

    # Variants in Spanish and other languages
    r"\bDermatólogo\s?Cosmético\b",
    r"\bMédico\s?Estético\b",
    r"\bEspecialista\s?en\s?Dermatología\s?Cosmética\b",

    # Other possible variations
    r"\bBoard\s?-?\s?Certified\s?Cosmetic\s?Dermatologist\b",
    r"\bGeneral\s?Cosmetic\s?Dermatologist\b",
    r"\bCosmeti Dermatology\b",
    r"\bLikar Dermatolog\b",
    r"\bCosmetic Dermatplpgy\b",
    r"\bConsultant DermatologistCosmetologist\b",
    r"\bCosmetic Dermatology\b",
    r"\bCosmetic Injecting\b",
    r"\bMedical Cosmetic\b",
    r"\bDermal Filler\b",
    r"\bKosmetische Medizin\b",
    r"\bCosmetic Injectables\b",
    r"\bMedica Procedimento Estetico\b",
    r"\bEstetica Facial\b",
    r"\bVrach Dermatokosmetolog\b",
    r"\bDermatology - Medical Devices\b",
    r"\bFacial Rejuvenation & Improvement Of Skin Quality With A Combination Of Injectable Treatments Of Hyaluronic Acid Calcium Hydroxyapatite & Botulinum Toxin Type A A Case Report\b",
    r"\bAnti Wrinkle Tx\b",
    r"\bDermocosmetics\b",
    r"\bDermatologistCosmetologist\b",
    r"\bDermato Cosmetolog\b",
    r"\bEstetica E Cosmetica\b",
    r"\bCosmiatra\b",
    r"\bCosmetic Efficacy\b",
    r"\bAnti-Wrinkle\b",
]

# Exact matches that should be updated
cosmetic_dermatologist_exact_matches = {
    "Cosmetic Dermatologist",
    "cosmetic dermatologist",
    "COSMETIC DERMATOLOGIST",
    "Cosmetic Dermotologist",
    "Cosmetick Dermatologist",
    "Cosmotik Dermatologist",
    "Kosmetic Dermatologist",
    "Cosmetic Dermetologist",
    "Cosmeti Dermatology",
    'Dermal Fillers',
    'dermal fillers',
    'dermal filler',
    'Dermal Filler',

    # Variants in Spanish
    "Dermatólogo Cosmético",
    "Médico Estético",
    "Especialista en Dermatología Cosmética",

    # Hybrid terms (English-Spanish combinations)
    "Cosmetic Dermatólogo",
    "Cosmetico Dermatologist",

    # Values from data sources
    "Cosmetic Dermatology",
    "cosmetic dermatology",
    "Aesthetic Dermatologist",
    'Cosmetic MedicineAesthetics',
    'Cosmetisch Arts',
    'DirectorSenior Dermal',
    'Dermal',
    'Vrach Kosmetolog Dermatolog',
    'Cosmetic Department',
    'Prp',
    'PRP',
    'prp',
    'Dermatology Therapeutic Specialist',
    'Senior Dermatology Therapeutic Specialist',
}

# Define patterns (these should NOT be changed)
cosmetic_dermatologist_exclusions = {
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
    'Registered Nurse Cosmetic Injectables',
}

# Create a mask for cosmetic_surgeon
mask_cosmetic_dermatologist = df['speciality'].str.contains('|'.join(cosmetic_dermatologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(cosmetic_dermatologist_exact_matches)
mask_cosmetic_dermatologist_exclusions = df['speciality'].isin(cosmetic_dermatologist_exclusions)

# Final mask: Select cosmetic_surgeon
mask_cosmetic_dermatologist_final = mask_cosmetic_dermatologist & ~mask_cosmetic_dermatologist_exclusions

# Store the original values that will be replaced
original_cosmetic_dermatologist_values = df.loc[mask_cosmetic_dermatologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_cosmetic_dermatologist_final, 'speciality'] = 'Cosmetic Dermatologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Cosmetic Dermatologist", 'green'))
print(df.loc[mask_cosmetic_dermatologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_cosmetic_dermatologist_values = df.loc[mask_cosmetic_dermatologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Cosmetic Dermatologist", "cyan"))
for original_cosmetic_dermatologist_value in original_cosmetic_dermatologist_values:
    print(f"✅ {original_cosmetic_dermatologist_value} → Cosmetic Dermatologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Cosmetic Dermatologist:", 'red'))
print(grouped_cosmetic_dermatologist_values)

# Print summary
matched_count_cosmetic_dermatologist = mask_cosmetic_dermatologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Cosmetic Dermatologist: "
        f"{matched_count_cosmetic_dermatologist}",
        'red'))


# Consmetic Surgeon

# Define regex patterns for Cosmetic Surgeon related titles

cosmetic_surgeon_variants = [
    # Standard title variations
    r"\bCosmetic\s?Surgeon\b",
    r"\bSurgeon\s?Cosmetic\b",
    r"\bCosmetic\s?Surgery\s?Specialist\b",
    r"\bSurgeon\s?for\s?Cosmetic\s?Procedures\b",
    r"\bDoctor\s?of\s?Cosmetic\s?Surgery\b",
    r"\bCosmetic Physician\b",
    r"\bCosmetic Surgery\b",
    r"\bCosmetic & Reconstruction Surgeon\b",
    r"\bCosmetic Physicians\b",

    # Common misspellings and case mistakes
    r"\bCosmetic\s?Surgion\b",
    r"\bCosmetick\s?Surgeon\b",
    r"\bCosmotik\s?Surgeon\b",
    r"\bKosmetic\s?Surgeon\b",
    r"\bCosmetic\s?Surjen\b",

    # Variants in Spanish and other languages
    r"\bCirujano\s?Cosmético\b",
    r"\bCirujano\s?Estético\b",
    r"\bMédico\s?Estético\b",

    # Other possible variations
    r"\bAesthetic Surgeon\b",
    r"\bBoard\s?-?\s?Certified\s?Cosmetic\s?Surgeon\b",
    r"\bCosmeti Surgery\b",
    r"\bGeneralCosmetic Surgeon\b",
    r"\bLikar Kosmetolog\b",
    r"\bCosmetic Physicion\b",
    r"\bDr  Kosmetolog\b",
    r"\bCoametic Surgeon\b",
]

# Exact matches that should be updated
cosmetic_surgeon_exact_matches = {
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",
    "Cosmetic Surgeon",

    # Common misspellings for Cosmetic Surgeon titles
    "Cosmetic Surgion",
    "Cosmetick Surgeon",
    "Cosmotik Surgeon",
    "Kosmetic Surgeon",
    "Cosmetic Surjen",
    "Cosmetik Surjen",
    "Kosmetic Surjen",
    "Cosmetic Surgeoon",

    # Case-related errors for Cosmetic Surgeon
    "cosmetic surgeon",
    "COSMETIC SURGEON",
    "Cosmetic Surgeon",
    "cosmetik surgeon",
    "kosmetic surgeon",
    "cosmetic surjen",
    "cosmetic surgeoon",

    # Variants of Cosmetic Surgeon in Spanish
    "Cirujano Cosmético",
    "Cirujano Estético",
    "Médico Estético",

    # Hybrid terms (Including English-Spanish combinations)
    "Cosmetic Cirujano",
    "Cosmetico Surgeon",

    # values from data sources
    'Cosmetic Doctor',
    'CIRUGIA COSMETICA',
}

# Define patterns (these should NOT be changed)
cosmetic_surgeon_exclusions = {
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
    'Plastic Reconstructive & Aesthetic Surgeon',
    'Cosmetic Surgery Fellow In Training',
}

# Create a mask for cosmetic_surgeon
mask_cosmetic_surgeon = df['speciality'].str.contains('|'.join(cosmetic_surgeon_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(cosmetic_surgeon_exact_matches)
mask_cosmetic_surgeon_exclusions = df['speciality'].isin(cosmetic_surgeon_exclusions)

# Final mask: Select cosmetic_surgeon
mask_cosmetic_surgeon_final = mask_cosmetic_surgeon & ~mask_cosmetic_surgeon_exclusions

# Store the original values that will be replaced
original_cosmetic_surgeon_values = df.loc[mask_cosmetic_surgeon_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_cosmetic_surgeon_final, 'speciality'] = 'Cosmetic Surgeon'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Cosmetic Surgeon", 'green'))
print(df.loc[mask_cosmetic_surgeon_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_cosmetic_surgeon_values = df.loc[mask_cosmetic_surgeon_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Cosmetic Surgeon", "cyan"))
for original_cosmetic_surgeon_value in original_cosmetic_surgeon_values:
    print(f"✅ {original_cosmetic_surgeon_value} → Cosmetic Surgeon")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Cosmetic Surgeon:", 'red'))
print(grouped_cosmetic_surgeon_values)

# Print summary
matched_count_cosmetic_surgeon = mask_cosmetic_surgeon_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Cosmetic Surgeon: "
        f"{matched_count_cosmetic_surgeon}",
        'red'))