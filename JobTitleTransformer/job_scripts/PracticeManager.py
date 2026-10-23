import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Practice Manager related titles

practice_manager_variants = [
    # Standard Titles & Variants
    r"\bPractice Manager\b",
    r"\bMedical Practice Manager\b",
    r"\bHealthcare Practice Manager\b",
    r"\bPractice Operations Manager\b",
    r"\bMedical Office Manager\b",
    r"\bPm\b",
    r"\bPractice Admin\b",
    r"\bPractice Administrator\b",
    r"\bPractice Head\b",
    r"\bPractice Growth & Profitability\b",
    r"\bPractice Development Manager\b",
    r"\bSenior Service Specialist\b",
    r"\bPractice Development\b",
    r"\bPractice Coordinator\b",

    # Misspellings & Typographical Errors
    r"\bPractise Manager\b",
    r"\bPractice Manger\b",
    r"\bPractic Manager\b",
    r"\bPractise Manger\b",
    r"\bPractioner Manager\b",
    r"\bPractice Maneger\b",

    # Case Variations
    r"\bpractice manager\b",
    r"\bPRACTICE MANAGER\b",
    r"\bPrAcTiCe MaNaGeR\b",

    # Spanish Variants
    r"\bGerente de Práctica\b",
    r"\bGerente de Oficina Médica\b",
    r"\bGerente de Consultorio Médico\b",
    r"\bAdministrador de Consultorio Médico\b",

    # Other Possible Variations
    r"\bHealthcare Administrator\b",
    r"\bMedical Office Administrator\b",
    r"\bPractice Operations Coordinator\b",
    r"\bPractice Operations Director\b",
    r"\bHealthcare Facility Manager\b",
    r"\bHealthcare Facility Manager\b",
    r"\bPratiche\b",
    r"\bOffice Manager Medical Affairs Administration\b",
    r"\bPractice Management\b",
]

# Exact matches that should be updated
practice_manager_exact_matches = {
    "Practice Manager",
    "Medical Practice Manager",
    "Healthcare Practice Manager",
    "Practice Operations Manager",
    "Medical Office Manager",
    "Practise Manager",
    "Practice Manger",
    "Practic Manager",
    "Practise Manger",
    "Practioner Manager",
    "Practice Maneger",
    "Gerente de Práctica",
    "Gerente de Oficina Médica",
    "Gerente de Consultorio Médico",
    "Administrador de Consultorio Médico",
    "Healthcare Administrator",
    "Medical Office Administrator",
    "Practice Operations Coordinator",
    "Practice Operations Director",
    "Healthcare Facility Manager",
    'Management',
    'CeoPractice Manager',
    'Aesthetics Program Manager - Physician Advocate',
    'Training Manager',
    'Clinical Training Director',
    'Practice Director',
    'Director Of Aesthetic Training',
    'Foundation Training',
    'OwnerPractice Manager',
    'Pracitce Manager',
    'Practice Makkar',
    'Prcactice Manager',
    'RNPractice Manager',
    'RN Administrator',
    'Practice admin',
    'Practice Administrator',
    'Director Training & Development',
    'Director of Training & Technical Support',
    'Director Of Physician Network Development & Practice Acquisitions',
    'Director Of Physician Practices',
    'Director Physician Practices',
    'Physician Practice Liaison',
    'Program Manager & Senior Acquisitions Physician',
    'Program Manager & Tpmg Health & Wellness Physician',
    'Program Manager Community Relations & Outreach Physician',
    'Program Manager General Surgery Residency Program',
    'Director of Aesthetics & Customer Service',
}

# # Define patterns (these should NOT be changed)
# practice_manager_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

practice_manager_exclusions = {
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

# Create a mask for Practice Manager
mask_practice_manager = df['speciality'].str.contains('|'.join(practice_manager_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(practice_manager_exact_matches)

# mask_practice_manager_exclusions = df['speciality'].str.contains(practice_manager_exclusions, case=False, na=False, regex=True)
mask_practice_manager_exclusions = df['speciality'].isin(practice_manager_exclusions)

# Final mask: Select Practice Manager
mask_practice_manager_final = mask_practice_manager & ~mask_practice_manager_exclusions

# Store the original values that will be replaced
original_practice_manager_values = df.loc[mask_practice_manager_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_practice_manager_final, 'speciality'] = 'Practice Manager'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Practice Manager", 'green'))
print(df.loc[mask_practice_manager_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_practice_manager_values = df.loc[mask_practice_manager_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Practice Manager", "cyan"))
for original_practice_manager_value in original_practice_manager_values:
    print(f"✅ {original_practice_manager_value} → Practice Manager")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Practice Manager:", 'red'))
print(grouped_practice_manager_values)

# Print summary
matched_count_practice_manager = mask_practice_manager_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Practice Manager: "
        f"{matched_count_practice_manager}",
        'red'))