import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Laboratory Medicine related titles

laboratory_medicine_variants = [
    r"\bLaboratory\s?Medicine\b",
    r"\bLab\s?Medicine\b",

    # Common misspellings and case errors
    r"\bLabratory\s?Medicine\b",
    r"\bLabortory\s?Medicine\b",
    r"\bLaborotory\s?Medicine\b",
    r"\bLaboratry\s?Medicine\b",
    r"\bLab Medicine\b",
    r"\bLabortary\s?Medicine\b",

    # Spanish variants
    r"\bMedicina\s?de\s?Laboratorio\b",
    r"\bMédico\s?de\s?Laboratorio\b",
    r"\bEspecialista\s?en\s?Medicina\s?de\s?Laboratorio\b",
    r"\bLaboratorio\s?Clínico\b",

    # Other possible variations
    r"\bLaboratory\s?Medicine\s?Specialist\b",
    r"\bLaboratory\s?Medicine\s?Physician\b",
    r"\bLaboratory\s?Medicine\s?Doctor\b",
    r"\bClinical\s?Laboratory\s?Specialist\b",
    r"\bBoard\s?Certified\s?Laboratory\s?Medicine\s?Doctor\b",
    r"\bMedico Laboral\b",
    r"Laboral",
    r"\bMagister En Analisis Y Diagnostico De Laboratorio\b",
    r"\bLaboratory Medicine\b",
    r"\bLaboratory Specialist\b",
    r"\bMedical Laboratory Technician\b",
    r"\bHead Of Laboratory\b",
    r"\bMagister En Analisis Y Diagnostico De Laboratorio\b",
    r"\bManager- Laboratory Services\b",
    r"\bLaboratory Manager\b",
    r"\bLaboratory Scientist\b",
    r"\bMedico Laboral\b",
    r"\bMedical Laboratory ScientistClinical Laboratory Technologist\b",
    r"\bMedical Laboratory Scientists\b",
    r"\bPrincipal Investigator & Head Of Laboratory\b",
    r"\bConstruction Forman Three Year Expriance & Constrction Material Laboratory 8 Years Expriance\b",
    r"\bLaboratory Technician\b",
    r"\bHead Of Laboratory Department\b",
    r"\bMedical Laboratory\b",
]

# Exact matches that should be updated
laboratory_medicine_exact_matches = {
    "Laboratory Medicine",
    "Lab Medicine",
    # Misspellings
    "Labratory Medicine",
    "Labortory Medicine",
    "Laborotory Medicine",
    "Laboratry Medicine",
    "Labortary Medicine",
    # Spanish variants
    "Medicina de Laboratorio",
    "Médico de Laboratorio",
    "Especialista en Medicina de Laboratorio",
    "Laboratorio Clínico",
    # Other possible variations
    "Laboratory Medicine Specialist",
    "Laboratory Medicine Physician",
    "Laboratory Medicine Doctor",
    "Clinical Laboratory Specialist",
    "Board Certified Laboratory Medicine Doctor",
    'Laboratory',
    'laboratory',
    'Lab',
    'lab',
}

# Define patterns (these should NOT be changed)
laboratory_medicine_exclusions = {
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

# Create a mask for Laboratory Medicine
mask_laboratory_medicine = df['speciality'].str.contains('|'.join(laboratory_medicine_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(laboratory_medicine_exact_matches)
mask_laboratory_medicine_exclusions = df['speciality'].isin(laboratory_medicine_exclusions)

# Final mask: Select Laboratory Medicine
mask_laboratory_medicine_final = mask_laboratory_medicine & ~mask_laboratory_medicine_exclusions

# Store the original values that will be replaced
original_laboratory_medicine_values = df.loc[mask_laboratory_medicine_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_laboratory_medicine_final, 'speciality'] = 'Laboratory Medicine'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Laboratory Medicine", 'green'))
print(df.loc[mask_laboratory_medicine_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_laboratory_medicine_values = df.loc[mask_laboratory_medicine_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Laboratory Medicine", "cyan"))
for original_laboratory_medicine_value in original_laboratory_medicine_values:
    print(f"✅ {original_laboratory_medicine_value} → Laboratory Medicine")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Laboratory Medicine:", 'red'))
print(grouped_laboratory_medicine_values)

# Print summary
matched_count_laboratory_medicine = mask_laboratory_medicine_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Laboratory Medicine: "
        f"{matched_count_laboratory_medicine}",
        'red'))