import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Neonatologist related titles

neonatologist_variants = [
   # Standard Titles & Abbreviations
    r"\bNeonatologist\b",
    r"\bNeonatal\s?Doctor\b",
    r"\bNeonatal\s?Specialist\b",
    r"\bNeonatology\s?Doctor\b",
    r"\bNeonatology\s?Specialist\b",
    r"\bConsultant\s?Neonatologist\b",
    r"\bSenior\s?Neonatologist\b",
    r"\bNeonatal\s?Physician\b",
    r"\bNeonatologist\s?Specialist\b",
    r"\bNeonatology\b",

    # Misspellings & Typographical Errors
    r"\bNeonotologist\b",
    r"\bNeonatoligist\b",
    r"\bNeonatoligist\b",
    r"\bNeonatoligist\b",
    r"\bNeonatogist\b",
    r"\bNeonoligist\b",
    r"\bNeonatoligist\b",
    r"\bNeonotoligist\b",
    r"\bNenoatologist\b",
    r"\bNeonologist\b",
    r"\bNeonlogist\b",
    r"\bNeonologist\b",

    # Case Variations
    r"\bneonatologist\b",
    r"\bNeonatologist\b",
    r"\bNEONATOLOGIST\b",
    r"\bNeonaToLogist\b",
    r"\bNeonAtologist\b",

    # Spanish Variants
    r"\bNeonatólogo\b",
    r"\bMédico\s?Neonatólogo\b",
    r"\bEspecialista\s?en\s?Neonatología\b",
    r"\bDoctor\s?en\s?Neonatología\b",
    r"\bConsultor\s?Neonatólogo\b",
    r"\bNeonatología\b",

    # Other Possible Variations (Including Doctor/Specialist Titles)
    r"\bNeonatal\s?Physician\b",
    r"\bNeonatal\s?Expert\b",
    r"\bPediatric\s?Neonatologist\b",
    r"\bNewborn\s?Specialist\b",
    r"\bPremature\s?Care\s?Specialist\b",
    r"\bNeonatal\s?Intensive\s?Care\s?Doctor\b",
    r"\bNeonatology\s?Expert\b",
]

# Exact matches that should be updated
neonatologist_exact_matches = {
    "Neonatologist",
    "Neonatal Doctor",
    "Neonatal Specialist",
    "Neonatology Doctor",
    "Neonatology Specialist",
    "Consultant Neonatologist",
    "Senior Neonatologist",
    "Neonatal Physician",
    "Neonatologist Specialist",
    "Neonatology",
    "Neonotologist",
    "Neonatoligist",
    "Neonatoligist",
    "Neonatogist",
    "Neonoligist",
    "Neonotoligist",
    "Nenoatologist",
    "Neonologist",
    "Neonlogist",
    "Neonatólogo",
    "Médico Neonatólogo",
    "Especialista en Neonatología",
    "Doctor en Neonatología",
    "Consultor Neonatólogo",
    "Neonatología",
    "Neonatal Physician",
    "Neonatal Expert",
    "Pediatric Neonatologist",
    "Newborn Specialist",
    "Premature Care Specialist",
    "Neonatal Intensive Care Doctor",
    "Neonatology Expert",
}

# # Define patterns (these should NOT be changed)
# neonatologist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

neonatologist_exclusions = {
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

# Create a mask for Neonatologist
mask_neonatologist = df['speciality'].str.contains('|'.join(neonatologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(neonatologist_exact_matches)

# mask_neonatologist_exclusions = df['speciality'].str.contains(neonatologist_exclusions, case=False, na=False, regex=True)
mask_neonatologist_exclusions = df['speciality'].isin(neonatologist_exclusions)

# Final mask: Select Neonatologist
mask_neonatologist_final = mask_neonatologist & ~mask_neonatologist_exclusions

# Store the original values that will be replaced
original_neonatologist_values = df.loc[mask_neonatologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_neonatologist_final, 'speciality'] = 'Neonatologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Neonatologist", 'green'))
print(df.loc[mask_neonatologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_neonatologist_values = df.loc[mask_neonatologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Neonatologist", "cyan"))
for original_neonatologist_value in original_neonatologist_values:
    print(f"✅ {original_neonatologist_value} → Neonatologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Neonatologist:", 'red'))
print(grouped_neonatologist_values)

# Print summary
matched_count_neonatologist = mask_neonatologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Neonatologist: "
        f"{matched_count_neonatologist}",
        'red'))

# Define regex patterns for Neurologist related titles

neurologist_variants = [
    # Standard Titles & Abbreviations
    r"\bNeurologist\b",
    r"\bNeuro\s?Doctor\b",
    r"\bNeuro\s?Specialist\b",
    r"\bNeurology\s?Doctor\b",
    r"\bNeurology\s?Specialist\b",
    r"\bConsultant\s?Neurologist\b",
    r"\bSenior\s?Neurologist\b",
    r"\bNeurological\s?Physician\b",
    r"\bNeuroscience\b",

    # Misspellings & Typographical Errors
    r"\bNurologist\b",
    r"\bNeorologist\b",
    r"\bNeuroligist\b",
    r"\bNeurlogist\b",
    r"\bNeoroligist\b",
    r"\bNeurollogist\b",
    r"\bNeurogist\b",
    r"\bNeuorlogist\b",
    r"\bNuerologist\b",
    r"\bNeurologits\b",
    r"\bNeurlgist\b",
    r"\bNeurologst\b",
    r"\bNeroligist\b",
    r"\bNeurlolgist\b",

    # Case Variations
    r"\bneurologist\b",
    r"\bNeurologist\b",
    r"\bNEUROLOGIST\b",
    r"\bNeuroLogist\b",
    r"\bNeurolOgist\b",

    # Spanish Variants
    r"\bNeurólogo\b",
    r"\bMédico\s?Neurólogo\b",
    r"\bEspecialista\s?en\s?Neurología\b",
    r"\bDoctor\s?en\s?Neurología\b",
    r"\bConsultor\s?Neurólogo\b",
    r"\bNeurocientífico\b",

    # Other Possible Variations (Including Doctor/Specialist Titles)
    r"\bNeuroscientist\b",
    r"\bNeuro\s?Physician\b",
    r"\bNeurosurgery\s?Specialist\b",
    r"\bBrain\s?Specialist\b",
    r"\bNeuromedicine\s?Expert\b",
    r"\bNeurology\b",
]

# Exact matches that should be updated
neurologist_exact_matches = {
    "Neurologist",
    "Neuro Doctor",
    "Neuro Specialist",
    "Neurology Doctor",
    "Neurology Specialist",
    "Consultant Neurologist",
    "Senior Neurologist",
    "Neurological Physician",
    "Nurologist",
    "Neorologist",
    "Neuroligist",
    "Neurlogist",
    "Neoroligist",
    "Neurollogist",
    "Neurogist",
    "Neuorlogist",
    "Nuerologist",
    "Neurologits",
    "Neurlgist",
    "Neurologst",
    "Neroligist",
    "Neurlolgist",
    "Neurólogo",
    "Médico Neurólogo",
    "Especialista en Neurología",
    "Doctor en Neurología",
    "Consultor Neurólogo",
    "Neurocientífico",
    "Neuroscientist",
    "Neuro Physician",
    "Neurosurgery Specialist",
    "Brain Specialist",
    "Neuromedicine Expert",
    'Neurosurgeon',
    'Neuro Rehab',
}

# # Define patterns (these should NOT be changed)
# neurologist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

neurologist_exclusions = {
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
    'Physician Assistant Neurology & Pain Management',
}

# Create a mask for Neurologist
mask_neurologist = df['speciality'].str.contains('|'.join(neurologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(neurologist_exact_matches)

# mask_neurologist_exclusions = df['speciality'].str.contains(neurologist_exclusions, case=False, na=False, regex=True)
mask_neurologist_exclusions = df['speciality'].isin(neurologist_exclusions)

# Final mask: Select Neurologist
mask_neurologist_final = mask_neurologist & ~mask_neurologist_exclusions

# Store the original values that will be replaced
original_neurologist_values = df.loc[mask_neurologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_neurologist_final, 'speciality'] = 'Neurologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Neurologist", 'green'))
print(df.loc[mask_neurologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_neurologist_values = df.loc[mask_neurologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Neurologist", "cyan"))
for original_neurologist_value in original_neurologist_values:
    print(f"✅ {original_neurologist_value} → Neurologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Neurologist:", 'red'))
print(grouped_neurologist_values)

# Print summary
matched_count_neurologist = mask_neurologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Neurologist: "
        f"{matched_count_neurologist}",
        'red'))