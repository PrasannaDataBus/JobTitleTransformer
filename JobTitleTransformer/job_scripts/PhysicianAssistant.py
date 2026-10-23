import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Physician Assistant related titles

PA_variants = [
    # Standard Titles & Variants
    r"\bPhysician Assistant\b",
    r"\bPhysician's Assistant\b",
    r"\bPhysician Assistant Specialist\b",
    r"\bPA\b",
    r"\bPhysician's Associate\b",
    r"\bMedical Assistant\b",  # Depending on context, could refer to the same
    r"\bPhysician Assistant Professional\b",
    r"\bP A/P A -C\b",
    r"\bP AP A -C\b",
    r"\bAsistente Medico Estetico\b",
    r"\bAssistante Medecine Esthetique\b",
    r"\bAuxiliar Medicina Estetica\b",
    r"\bGeneral Koordinator\b",
    r"\bMd Assistant\b",
    r"\bAssiant\b",
    r"\bAsistent\b",
    r"\bAssistante Medicale\b",
    r"\bAsistente\b",
    r"\bAssistante\b",
    r"\bPhysician Associate\b",
    r"\bOperation Associate\b",
    r"\bPersonal Assistant To Dr\b",

    # Misspellings & Typographical Errors
    r"\bPhyscian Assistant\b",
    r"\bPhysician Assitant\b",
    r"\bPhysician Asistant\b",
    r"\bPhysican Assistant\b",

    # Case Variations
    r"\bphysician assistant\b",
    r"\bPHYSICIAN ASSISTANT\b",
    r"\bPhYsIcIaN AsSiStAnT\b",
    r"\bPhysician AssistanT\b",

    # Spanish Variants
    r"\bAsistente Médico\b",
    r"\bAsistente de Médico\b",
    r"\bAsistente de Medicina\b",
    r"\bAsociado Médico\b",
    r"\bAsistente de Médico Profesional\b",

    # Other Possible Variations
    r"\bMedical Physician Assistant\b",
    r"\bHealth Practitioner Assistant\b",
    r"\bClinical Physician Assistant\b",
    r"\bPhysician's Healthcare Assistant\b",
    r"\bCoordinator Tsfp\b",
    r"\bPlastic Surgery Medical Assistant\b",
    r"\bPlastic Surgery Pa\b",
    r"\bAssistante Medecine Esthetique\b",
    r"\bPhysician Assistant\b",
    r"\bP AP A -C\b",
    r"\bPhysician Associate\b",
    r"\bAssistant Camera Operator\b",
    r"\bPersonal Assistant\b",
    r"\bPa\b",
    r"\bAssiant\b",
    r"\bPa-C\b",
    r"\bMd Assistant\b",
    r"\bAsistent\b",
    r"\bPlastic Surgery Medical Assistant\b",
    r"\bCertified Medical Assistant\b",
    r"\bAssistante Medecine Esthetique\b",
    r"\bAssistante Medicale\b",
    r"\bDoctor Asistent\b",
    r"\bMedical Assistant\b",
    r"\bMedical Care Assistant\b",
    r"\bMedicalScientific Assistant\b",
    r"\bMpas Pa-C\b",
    r"\bExeccutive Assistant\b",
    r"\bOperation Associate\b",
    r"\bPa C\b",
    r"\bGeneral Koordinator\b",
    r"\bSurgical Assistant\b",
    r"\bPlastic Surgery Pa\b",
    r"\bAsistente Medico Estetico\b",
    r"\bRn Pa\b",
    r"\bAesthetic Pa\b",
    r"\bAesthetic Dermatology Pa\b",
    r"\bCoordinator Tsfp\b",
    r"\bImd-Pa\b",
    r"\bAssistant Planner\b",
    r"\bAsistente De Gerencia\b",
    r"\bPersonal Assistant To Dr\b",
    r"\bAssistant Bu\b",
    r"\bNpd Assistant\b",
    r"\bAssistant To The Management\b",
    r"\bPolar & Care Assistant\b",
    r"\bPhysician Assistant Injector\b",
    r"\bSpecial Assistant\b",
    r"\bResearch Assistant\b",
    r"\bAssistant Practitioner\b",
]

# Exact matches that should be updated
PA_exact_matches = {
    "Physician Assistant",
    "Physician's Assistant",
    "Physician Assistant Specialist",
    "PA",
    "Physician's Associate",
    "Medical Assistant",
    "Physician Assistant Professional",
    "Physcian Assistant",
    "Physician Assitant",
    "Physician Asistant",
    "Physican Assistant",
    "Asistente Médico",
    "Asistente de Médico",
    "Asistente de Medicina",
    "Asociado Médico",
    "Asistente de Médico Profesional",
    "Medical Physician Assistant",
    "Health Practitioner Assistant",
    "Clinical Physician Assistant",
    "Physician's Healthcare Assistant",
    "P AP A -C",
    'Assistant',
    'assistant',
    'Physician AssistantFounder',
    'Physician AssistantOwner',
    'Physicians Assitant',
    'Physician Coordinator',
    'Orthopedic Physician S Assistant',
    'DMS PAC CAC',
}

# # Define patterns (these should NOT be changed)
# PA_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

PA_exclusions = {
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

# Create a mask for Physician Assistant
mask_PA = df['speciality'].str.contains('|'.join(PA_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(PA_exact_matches)

# mask_PA_exclusions = df['speciality'].str.contains(PA_exclusions, case=False, na=False, regex=True)
mask_PA_exclusions = df['speciality'].isin(PA_exclusions)

# Final mask: Select Physician Assistant
mask_PA_final = mask_PA & ~mask_PA_exclusions

# Store the original values that will be replaced
original_PA_values = df.loc[mask_PA_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_PA_final, 'speciality'] = 'Physician Assistant'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Physician Assistant", 'green'))
print(df.loc[mask_PA_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_PA_values = df.loc[mask_PA_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Physician Assistant", "cyan"))
for original_PA_value in original_PA_values:
    print(f"✅ {original_PA_value} → Physician Assistant")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Physician Assistant:", 'red'))
print(grouped_PA_values)

# Print summary
matched_count_PA = mask_PA_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Physician Assistant: "
        f"{matched_count_PA}",
        'red'))