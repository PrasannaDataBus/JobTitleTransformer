import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Nurse Practitioner (NP) related titles

NP_variants = [
    # Standard Titles & Abbreviations
    r"\bNurse\s?Practitioner\b",
    r"\bNurse\s?Practitioner\s?\(NP\)\b",
    r"\bNP\b",
    r"\bNurse Practitioner NP\b",
    r"\bN P\b",
    r"\bn p\b",
    r"\bANP\b",
    r"\bFamily\s?Nurse\s?Practitioner\b",
    r"\bFNP\b",
    r"\bAdult\s?Nurse\s?Practitioner\b",
    r"\bPediatric\s?Nurse\s?Practitioner\b",
    r"\bPsychiatric\s?Nurse\s?Practitioner\b",
    r"\bGeriatric\s?Nurse\s?Practitioner\b",
    r"\bNurse Injector\b",
    r"\bCosmetic Nurse\b",
    r"\bStaff Nurse\b",
    r"\bNurse Prescriber\b",
    r"\bNursing\b",
    r"\bAesthetic Nurse PractitionerPrescriber\b",
    r"\bAesthetic Nurse SpecialistOwnee\b",
    r"\bAesthetic PracticionerNurse\b",
    r"\bCertified Nurse Midwifery\b",
    r"\bNuse\b",
    r"\bEsthetic Nurse\b",
    r"\bSpec  Nurse\b",
    r"\bStaffnurse\b",
    r"\bIndependent Nurse Presceriber\b",
    r"\bNursingGluta Infusions\b",

    # Misspellings & Typographical Errors
    r"\bNurs\s?Practitioner\b",
    r"\bNurse\s?Practioner\b",
    r"\bNurse\s?Pracktitioner\b",
    r"\bNurse\s?Practitonner\b",
    r"\bNurse\s?Practitoner\b",
    r"\bNurse\s?Pracktitioner\s?\(NP\)\b",
    r"\bNurse\s?Prakittioner\b",
    r"\bNurse\s?Practitionar\b",
    r"\bNurce\s?Practitioner\b",
    r"\bNurse\s?Prakitoner\b",

    # Case Variations
    r"\bnurse practitioner\b",
    r"\bNurse practitioner\b",
    r"\bnurse Practitioner\b",
    r"\bNURSE PRACTITIONER\b",
    r"\bNurse PRACTITIONER\b",
    r"\bnurse PRACTITIONER\b",

    # Spanish Variants
    r"\bEnfermero\s?Practicante\b",
    r"\bEnfermera\s?Practicante\b",
    r"\bPracticante\s?de\s?Enfermería\b",
    r"\bEspecialista\s?en\s?Enfermería\b",
    r"\bEnfermero\s?de\s?Atención\s?Primaria\b",

    # Other Possible Variations (Including Doctor/Specialist Forms)
    r"\bNurse\s?Clinician\b",
    r"\bSenior\s?Nurse\s?Practitioner\b",
    r"\bBoard\s?Certified\s?Nurse\s?Practitioner\b",
    r"\bCertified\s?Nurse\s?Practitioner\b",
    r"\bOwnerNurse Practitioner\b",
]

# Exact matches that should be updated
NP_exact_matches = {
    "Nurse Practitioner",
    "Nurse Practitioner (NP)",
    "NP",
    "Family Nurse Practitioner",
    "FNP",
    "Adult Nurse Practitioner",
    "Pediatric Nurse Practitioner",
    "Psychiatric Nurse Practitioner",
    "Geriatric Nurse Practitioner",
    "Nurs Practitioner",
    "Nurse Practioner",
    "Nurse Pracktitioner",
    "Nurse Practitonner",
    "Nurse Practitoner",
    "Nurse Pracktitioner (NP)",
    "Nurse Prakittioner",
    "Nurse Practitionar",
    "Nurce Practitioner",
    "Nurse Prakitoner",
    "Enfermero Practicante",
    "Enfermera Practicante",
    "Practicante de Enfermería",
    "Especialista en Enfermería",
    "Enfermero de Atención Primaria",
    "Nurse Clinician",
    "Senior Nurse Practitioner",
    "Board Certified Nurse Practitioner",
    "Certified Nurse Practitioner",
    "Injector",
    "Aesthetic PracticionerNurse",
    'Nurse Pracitioner',
    'Nurse Practicioner',
    'Nurs Practitionar',
    'Nrs Practitioner',
    'Cosmetologist & Studing Nurse',
    'Cosmetology Nurse',
    'Specialist Nurse',
    'Nurse Antiaging',
    'Nurse PractitionerMedical Director',
    'Lic  Enfermeria',
    'Wound Care Nurse',
    'DNM',
}

# # Define patterns (these should NOT be changed)
NP_exclusions = r'\b(?:ARNP)|(?:Advanced)|(?:Registered)|(?:Rn)|(?:RN)\b'

# NP_exclusions = {
#     'Resident', 'resident', 'student', 'Trainee', 'Resident Doctor', 'Resident ooPhysician',
#     'Intern', 'intern', 'Medical Intern', 'Fellow', 'fellow', 'Clinical Fellow', 'Medical Student',
#     'Clinical Trainee', 'Trainee Doctor', 'Trainee Physician', 'Junior Doctor', 'Postgraduate Trainee',
#     'Aesthetic Fellow', 'Aesthetic Trainee', 'Aesthetic Medicine Fellow', 'Aesthetic Resident'
# }

# Create a mask for Nurse Practitioner (NP)
mask_NP = df['speciality'].str.contains('|'.join(NP_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(NP_exact_matches)

mask_NP_exclusions = df['speciality'].str.contains(NP_exclusions, case=False, na=False, regex=True)
# mask_NP_exclusions = df['speciality'].isin(NP_exclusions)

# Final mask: Select Nurse Practitioner (NP)
mask_NP_final = mask_NP & ~mask_NP_exclusions

# Store the original values that will be replaced
original_NP_values = df.loc[mask_NP_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_NP_final, 'speciality'] = 'Nurse Practitioner (NP)'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Nurse Practitioner (NP)", 'green'))
print(df.loc[mask_NP_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_NP_values = df.loc[mask_NP_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Nurse Practitioner (NP)", "cyan"))
for original_NP_value in original_NP_values:
    print(f"✅ {original_NP_value} → Nurse Practitioner (NP)")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Nurse Practitioner (NP):", 'red'))
print(grouped_NP_values)

# Print summary
matched_count_NP = mask_NP_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Nurse Practitioner (NP): "
        f"{matched_count_NP}",
        'red'))