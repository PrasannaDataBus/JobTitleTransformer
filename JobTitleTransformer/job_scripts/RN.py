import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Registered Nurse (RN) related titles

RN_variants = [
    # Standard Titles & Variants
    r"\bRegistered Nurse\b",
    r"\bRegistered Nurse (RN)\b",
    r"\bRN\b",
    r"\bNurse (Registered)\b",
    r"\bRegistered Nurse Practitioner\b",
    r"\bRegistered Professional Nurse\b",
    r"\bNursing Specialist\b",
    r"\bRegistered Nurse RN\b",
    r"\bR N\b",
    r"\bRm\b",
    r"\bRegister Nurse\b",
    r"\bRegistered Cosmetic Nurse\b",
    r"\bRegistered Nursing\b",
    r"\bRegistered Staff Nurse\b",
    r"\bInjection\b",
    r"\bChargenurse\b",
    r"\bAdvanced Practice Registered Nurse\b",
    r"\bInfirmiere Auxiliaire\b",
    r"\bRegisterednurse\b",
    r"\bPrescribing Nurse\b",
    r"\bRegistered General Nurse\b",
    r"\bOperatsionnaia Medsestra\b",
    r"\bInfirmiere\b",
    r"\bMidwife\b",
    r"\bEnfermeira\b",
    r"\bEnfermagem Estetica\b",
    r"\bEmergencyroomnurse\b",
    r"\bRnPmhnp\b",

    # Misspellings & Typographical Errors
    r"\bRegistred Nurse\b",
    r"\bRegisted Nurse\b",
    r"\bRegitered Nurse\b",
    r"\bResgistered Nurse\b",
    r"\bRegistred Nurce\b",
    r"\bRergistered Nurse\b",
    r"\bRegistered Nure\b",
    r"\bRegistered Nuerse\b",

    # Case Variations
    r"\bREGISTERED NURSE\b",
    r"\bREGISTERED NURSE (RN)\b",
    r"\bregistered nurse\b",
    r"\bREGISTERED nurse\b",

    # Spanish Variants
    r"\bEnfermera Registrada\b",
    r"\bEnfermera Profesional Registrada\b",
    r"\bEnfermera (RN)\b",
    r"\bEnfermera Especialista\b",
    r"\bEnfermera Registrada (RN)\b",
    r"\bEnfermera de Cuidados Críticos\b",

    # Hybrid Spanish-English Variants
    r"\bRegistered Enfermera\b",
    r"\bNurse Registrada (RN)\b",

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bNurse Practitioner (Registered)\b",
    r"\bNurse Consultant\b",
    r"\bCertified Registered Nurse (CRN)\b",
    r"\bRegistered Nursing Assistant\b",
    r"\bNurse Educator\b",
    r"\bNursing Supervisor\b",
    r"\bCommunity Nurse\b",
    r"\bCritical Care Nurse (RN)\b",
    r"\bEmergency Nurse (RN)\b",
    r"\bCosmetic NurseRegistered Nurse\b",
]

# Exact matches that should be updated
RN_exact_matches = {
    "Registered Nurse",
    "Registered Nurse (RN)",
    "RN",
    "Nurse (Registered)",
    "Registered Nurse Practitioner",
    "Registered Professional Nurse",
    "Nursing Specialist",
    "Registred Nurse",
    "Registed Nurse",
    "Regitered Nurse",
    "Resgistered Nurse",
    "Registred Nurce",
    "Rergistered Nurse",
    "Registered Nure",
    "Registered Nuerse",
    "Enfermera Registrada",
    "Enfermera Profesional Registrada",
    "Enfermera (RN)",
    "Enfermera Especialista",
    "Enfermera Registrada (RN)",
    "Enfermera de Cuidados Críticos",
    "Registered Enfermera",
    "Nurse Registrada (RN)",
    "Nurse Practitioner (Registered)",
    "Nurse Consultant",
    "Certified Registered Nurse (CRN)",
    "Registered Nursing Assistant",
    "Nurse Educator",
    "Nursing Supervisor",
    "Community Nurse",
    "Critical Care Nurse (RN)",
    "Emergency Nurse (RN)",
    "Aesthetic Nurse",
    "Registered Nurse RN",
    'Registered NurseClinical Director',
    'Rgn',
    'Aesthetic RNOwner',
    'Advanced Practice Aesthetic RN',
    'Certified Aesthetic Nurse Specialist Independent Contractor',
    'Emt',
    'Aesthetic Nurse & Clinic CEO',
    'Aesthetic nurse',
    'Enfermera',
}

# # Define patterns (these should NOT be changed)
RN_exclusions = r'\b(?:ARNP)|(?:Arpn)|(?:Advanced)|(?:Licensed)\b'

# RN_exclusions = {
#     'Resident', 'resident', 'student', 'Trainee', 'Resident Doctor', 'Resident ooPhysician',
#     'Intern', 'intern', 'Medical Intern', 'Fellow', 'fellow', 'Clinical Fellow', 'Medical Student',
#     'Clinical Trainee', 'Trainee Doctor', 'Trainee Physician', 'Junior Doctor', 'Postgraduate Trainee',
#     'Aesthetic Fellow', 'Aesthetic Trainee', 'Aesthetic Medicine Fellow', 'Aesthetic Resident'
# }

# Create a mask for Registered Nurse (RN)
mask_RN = df['speciality'].str.contains('|'.join(RN_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(RN_exact_matches)

mask_RN_exclusions = df['speciality'].str.contains(RN_exclusions, case=False, na=False, regex=True)
# mask_RN_exclusions = df['speciality'].isin(RN_exclusions)

# Final mask: Select Registered Nurse (RN)
mask_RN_final = mask_RN & ~mask_RN_exclusions

# Store the original values that will be replaced
original_RN_values = df.loc[mask_RN_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_RN_final, 'speciality'] = 'Registered Nurse (RN)'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Registered Nurse (RN)", 'green'))
print(df.loc[mask_RN_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_RN_values = df.loc[mask_RN_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Registered Nurse (RN)", "cyan"))
for original_RN_value in original_RN_values:
    print(f"✅ {original_RN_value} → Registered Nurse (RN)")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Registered Nurse (RN):", 'red'))
print(grouped_RN_values)

# Print summary
matched_count_RN = mask_RN_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Registered Nurse (RN): "
        f"{matched_count_RN}",
        'red'))