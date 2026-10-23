import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Psychologist related titles

psychologist_variants = [
    # Standard Titles & Variants
    r"\bPsychologist\b",
    r"\bClinical Psychologist\b",
    r"\bLicensed Psychologist\b",
    r"\bPsychology Specialist\b",
    r"\bBehavioral Psychologist\b",
    r"\bMental Health Psychologist\b",

    # Misspellings & Typographical Errors
    r"\bPshychologist\b",
    r"\bPsychologst\b",
    r"\bPsycholigist\b",
    r"\bPsycholgist\b",
    r"\bPsycologist\b",
    r"\bPsychollogist\b",
    r"\bPsychologgist\b",
    r"\bPsychologisst\b",
    r"\bPsichologist\b",

    # Case Variations
    r"\bPSYCHOLOGIST\b",
    r"\bpsychologist\b",
    r"\bPsYcHoLoGiSt\b",

    # Spanish Variants
    r"\bPsicólogo\b",
    r"\bPsicóloga\b",
    r"\bDoctor en Psicología\b",
    r"\bEspecialista en Psicología\b",
    r"\bMédico Psicólogo\b",
    r"\bPsicólogo Clínico\b",
    r"\bPsicólogo de la Salud\b",

    # Hybrid Spanish-English Variants
    r"\bPsicologyst\b",
    r"\bPsychologa\b",

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bConsultant Psychologist\b",
    r"\bSenior Psychologist\b",
    r"\bLead Psychologist\b",
    r"\bForensic Psychologist\b",
    r"\bChild Psychologist\b",
    r"\bGeriatric Psychologist\b",
    r"\bNeuropsychologist\b",
    r"\bPsychology\b",
    r"\bChild & Adolescent Neuropsichiatry\b",
]

# Exact matches that should be updated
psychologist_exact_matches = {
    "Psychologist",
    "Clinical Psychologist",
    "Licensed Psychologist",
    "Psychology Specialist",
    "Behavioral Psychologist",
    "Mental Health Psychologist",
    "Pshychologist",
    "Psychologst",
    "Psycholigist",
    "Psycholgist",
    "Psycologist",
    "Psychollogist",
    "Psychologgist",
    "Psychologisst",
    "Psichologist",
    "Psicólogo",
    "Psicóloga",
    "Doctor en Psicología",
    "Especialista en Psicología",
    "Médico Psicólogo",
    "Psicólogo Clínico",
    "Psicólogo de la Salud",
    "Psicologyst",
    "Psychologa",
    "Consultant Psychologist",
    "Senior Psychologist",
    "Lead Psychologist",
    "Forensic Psychologist",
    "Child Psychologist",
    "Geriatric Psychologist",
    "Neuropsychologist",
}

# # Define patterns (these should NOT be changed)
# psychologist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

psychologist_exclusions = {
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

# Create a mask for Psychologist
mask_psychologist = df['speciality'].str.contains('|'.join(psychologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(psychologist_exact_matches)

# mask_psychologist_exclusions = df['speciality'].str.contains(psychologist_exclusions, case=False, na=False, regex=True)
mask_psychologist_exclusions = df['speciality'].isin(psychologist_exclusions)

# Final mask: Select Psychologist
mask_psychologist_final = mask_psychologist & ~mask_psychologist_exclusions

# Store the original values that will be replaced
original_psychologist_values = df.loc[mask_psychologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_psychologist_final, 'speciality'] = 'Psychologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Psychologist", 'green'))
print(df.loc[mask_psychologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_psychologist_values = df.loc[mask_psychologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Psychologist", "cyan"))
for original_psychologist_value in original_psychologist_values:
    print(f"✅ {original_psychologist_value} → Psychologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Psychologist:", 'red'))
print(grouped_psychologist_values)

# Print summary
matched_count_psychologist = mask_psychologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Psychologist: "
        f"{matched_count_psychologist}",
        'red'))