import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Pathologist related titles

pathologist_variants = [
    # Standard Titles & Variants
    r"\bPathologist\b",
    r"\bClinical Pathologist\b",
    r"\bMedical Pathologist\b",
    r"\bAnatomic Pathologist\b",
    r"\bForensic Pathologist\b",
    r"\bPathology Consultant\b",
    r"\bConsultant Pathologist\b",
    r"\bLaboratory Pathologist\b",
    r"\bHistopathologist\b",
    r"\bHematopathologist\b",
    r"\bMolecular Pathologist\b",
    r"\bGeneral Pathologist\b",
    r"\bPediatric Pathologist\b",
    r"\bPathology\b",

    # Misspellings & Typographical Errors
    r"\bPathologiest\b",
    r"\bPatholigist\b",
    r"\bPatologist\b",
    r"\bPatholigist\b",
    r"\bPthologist\b",
    r"\bPatholigist\b",

    # Case Variations
    r"\bpathologist\b",
    r"\bPaThOlOgIsT\b",
    r"\bPATHOLOGIST\b",
    r"\bPaThOlOgIsT\b",

    # Spanish Variants
    r"\bPatólogo\b",
    r"\bPatóloga\b",
    r"\bPatólogo\s?Clínico\b",
    r"\bPatólogo\s?Médico\b",
    r"\bPatólogo\s?Anatómico\b",
    r"\bPatólogo\s?Forense\b",
    r"\bConsultor\s?Patólogo\b",
    r"\bPatólogo\s?Consultor\b",
    r"\bLaboratorio\s?Patólogo\b",
    r"\bHematopatólogo\b",
    r"\bPatólogo\s?Molecular\b",
    r"\bPatólogo\s?General\b",
    r"\bPatólogo\s?Pediátrico\b",

    # Other Possible Variations
    r"\bPathology\s?Consultant\b",
    r"\bLaboratory\s?Pathologist\b",
    r"\bPathologist\s?Specialist\b",
    r"\bCertified\s?Pathologist\b",
    r"\bSenior\s?Pathologist\b",
    r"\bJunior\s?Pathologist\b",
    r"\bExpert\s?Pathologist\b",
    r"\bMedical\s?Pathology\s?Consultant\b",
]

# Exact matches that should be updated
pathologist_exact_matches = {
    "Pathologist",
    "Clinical Pathologist",
    "Medical Pathologist",
    "Anatomic Pathologist",
    "Forensic Pathologist",
    "Pathology Consultant",
    "Consultant Pathologist",
    "Laboratory Pathologist",
    "Histopathologist",
    "Hematopathologist",
    "Molecular Pathologist",
    "General Pathologist",
    "Pediatric Pathologist",
    "Pathologiest",
    "Patholigist",
    "Patologist",
    "Pthologist",
    "Patólogo",
    "Patóloga",
    "Patólogo Clínico",
    "Patólogo Médico",
    "Patólogo Anatómico",
    "Patólogo Forense",
    "Consultor Patólogo",
    "Patólogo Consultor",
    "Laboratorio Patólogo",
    "Hematopatólogo",
    "Patólogo Molecular",
    "Patólogo General",
    "Patólogo Pediátrico",
    "Pathologist Specialist",
    "Certified Pathologist",
    "Senior Pathologist",
    "Junior Pathologist",
    "Expert Pathologist",
    "Medical Pathology Consultant",
    'Biopathologist Antiaging Medicine',
    'Medica Patologista',
}

# # Define patterns (these should NOT be changed)
# pathologist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

pathologist_exclusions = {
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
    'Client Developer - Pathology & Dermatology',
}

# Create a mask for Pathologist
mask_pathologist = df['speciality'].str.contains('|'.join(pathologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(pathologist_exact_matches)

# mask_pathologist_exclusions = df['speciality'].str.contains(pathologist_exclusions, case=False, na=False, regex=True)
mask_pathologist_exclusions = df['speciality'].isin(pathologist_exclusions)

# Final mask: Select Pathologist
mask_pathologist_final = mask_pathologist & ~mask_pathologist_exclusions

# Store the original values that will be replaced
original_pathologist_values = df.loc[mask_pathologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_pathologist_final, 'speciality'] = 'Pathologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Pathologist", 'green'))
print(df.loc[mask_pathologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_pathologist_values = df.loc[mask_pathologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Pathologist", "cyan"))
for original_pathologist_value in original_pathologist_values:
    print(f"✅ {original_pathologist_value} → Pathologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Pathologist:", 'red'))
print(grouped_pathologist_values)

# Print summary
matched_count_pathologist = mask_pathologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Pathologist: "
        f"{matched_count_pathologist}",
        'red'))