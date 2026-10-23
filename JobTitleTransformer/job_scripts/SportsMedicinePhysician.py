import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Sports Medicine Physician related titles

sports_med_variants = [
    # Standard Titles & Variants
    r"\bSports Medicine Physician\b",  # General term
    r"\bSports Medicine Specialist\b",  # Specialist in sports medicine
    r"\bSports Doctor\b",  # General term for sports-focused doctor
    r"\bSports Physician\b",  # Alternate term for sports-focused doctor
    r"\bSports Medicine Doctor\b",  # Another variation for a sports-focused physician
    r"\bSports Medicine\b",  # General term

    # Misspellings & Typographical Errors
    r"\bSport Medicine Physician\b",  # Common misspelling
    r"\bSport Medicine Specialist\b",  # Misspelling of "Sports"
    r"\bSports Medecine Physician\b",  # Misspelling of "Medicine"
    r"\bSports Mediine Physician\b",  # Typo with double 'i'

    # Case Variations
    r"\bSPORTS MEDICINE PHYSICIAN\b",  # Uppercase variation
    r"\bsports medicine physician\b",  # Lowercase variation
    r"\bSpOrTs MeDiCiNe PhYsIcIaN\b",  # Mixed case variation

    # Spanish Variants
    r"\bMédico de Medicina Deportiva\b",  # General term for Sports Medicine Physician
    r"\bEspecialista en Medicina Deportiva\b",  # Specialist in Sports Medicine
    r"\bMédico Deportivo\b",  # Sports doctor in Spanish
    r"\bFisioterapeuta Deportivo\b",  # Sports physiotherapist (closely related)
    r"\bMédico de Deporte\b",  # Another variant for sports physician
    r"\bMedicina del Deporte\b",  # Sports Medicine as a field (generic)
    r"\bMedicina Deportiva\b",  # General term for Sports Medicine Physician

    # Hybrid Spanish-English Variants
    r"\bSports Médico\b",  # Mixed term
    r"\bSports Médico Deportivo\b",  # Mixed term

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bSports Medicine Specialist Physician\b",  # Specialist term
    r"\bSports Medicine Expert\b",  # Expert term for sports medicine
    r"\bSports Physician Specialist\b",  # Specialist form of physician
    r"\bSports Medicine Consultant\b",  # Consulting variant
    r"\bSports Rehabilitation Doctor\b",  # Related rehabilitation term
    r"\bSports Injury Specialist\b",  # Related to injury management in sports
    r"\bMedico Esportista\b",
    r"Esportista\b",
    r"\bGym Ecology\b",
]

# Exact matches that should be updated
sports_med_exact_matches = {
    "Sports Medicine Physician",
    "Sports Medicine Specialist",
    "Sports Doctor",
    "Sports Physician",
    "Sports Medicine Doctor",
    "Sport Medicine Physician",
    "Sport Medicine Specialist",
    "Sports Medecine Physician",
    "Sports Mediine Physician",
    "SPORTS MEDICINE PHYSICIAN",
    "sports medicine physician",
    "SpOrTs MeDiCiNe PhYsIcIaN",
    "Médico de Medicina Deportiva",
    "Especialista en Medicina Deportiva",
    "Médico Deportivo",
    "Fisioterapeuta Deportivo",
    "Médico de Deporte",
    "Medicina del Deporte",
    "Sports Médico",
    "Sports Médico Deportivo",
    "Sports Medicine Specialist Physician",
    "Sports Medicine Expert",
    "Sports Physician Specialist",
    "Sports Medicine Consultant",
    "Sports Rehabilitation Doctor",
    "Sports Injury Specialist",
    'Family Sports',
}

# # Define patterns (these should NOT be changed)
# sports_med_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

sports_med_exclusions = {
    'Resident', 'resident', 'student', 'Trainee', 'Resident Doctor', 'Resident ooPhysician',
    'Intern', 'intern', 'Medical Intern', 'Fellow', 'fellow', 'Clinical Fellow', 'Medical Student',
    'Clinical Trainee', 'Trainee Doctor', 'Trainee Physician', 'Junior Doctor', 'Postgraduate Trainee',
    'Aesthetic Fellow', 'Aesthetic Trainee', 'Aesthetic Medicine Fellow', 'Aesthetic Resident'
}

# Create a mask for Sports Medicine Physician
mask_sports_med = df['speciality'].str.contains('|'.join(sports_med_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(sports_med_exact_matches)

# mask_sports_med_exclusions = df['speciality'].str.contains(sports_med_exclusions, case=False, na=False, regex=True)
mask_sports_med_exclusions = df['speciality'].isin(sports_med_exclusions)

# Final mask: Select Sports Medicine Physician
mask_sports_med_final = mask_sports_med & ~mask_sports_med_exclusions

# Store the original values that will be replaced
original_sports_med_values = df.loc[mask_sports_med_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_sports_med_final, 'speciality'] = 'Sports Medicine Physician'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Sports Medicine Physician", 'green'))
print(df.loc[mask_sports_med_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_sports_med_values = df.loc[mask_sports_med_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Sports Medicine Physician", "cyan"))
for original_sports_med_value in original_sports_med_values:
    print(f"✅ {original_sports_med_value} → Sports Medicine Physician")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Sports Medicine Physician:", 'red'))
print(grouped_sports_med_values)

# Print summary
matched_count_sports_med = mask_sports_med_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Sports Medicine Physician: "
        f"{matched_count_sports_med}",
        'red'))