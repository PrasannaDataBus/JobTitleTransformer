import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Pediatrician related titles

pediatrician_variants = [
    # Standard Titles & Variants
    r"\bPediatrician\b",
    r"\bPediatrist\b",
    r"\bPediatrics Specialist\b",
    r"\bPediatric Doctor\b",
    r"\bChild Specialist\b",
    r"\bPediatrics Physician\b",
    r"\bPediatric Consultant\b",
    r"\bPediatric Specialist\b",
    r"\bPediatric Practitioner\b",
    r"\bPediatric Surgeon\b",
    r"\bGeneral Pediatrician\b",
    r"\bPediatrician Consultant\b",
    r"\bConsultant Pediatrician\b",
    r"Paediatrics",
    r"\bPaediatric Surgery\b",
    r"\bPaediatrician\b",

    # Misspellings & Typographical Errors
    r"\bPediatrition\b",
    r"\bPediatrition\b",
    r"\bPedriatrician\b",
    r"\bPeditrician\b",
    r"\bPedatrician\b",
    r"\bPediatrion\b",
    r"\bPediatrian\b",

    # Case Variations
    r"\bpediatrician\b",
    r"\bPEDIATRICIAN\b",
    r"\bPeDiAtRiCiAn\b",
    r"\bPediatriCian\b",

    # Spanish Variants
    r"\bPediatra\b",
    r"\bPediatra\s?General\b",
    r"\bPediatra\s?Especialista\b",
    r"\bMédico\s?Pediatra\b",
    r"\bPediatra\s?Consultor\b",
    r"\bPediatra\s?Infantil\b",
    r"\bPediatra\s?Pediátrico\b",
    r"\bPediatra\s?Cirujano\b",
    r"\bPediatra\s?Generalista\b",

    # Other Possible Variations
    r"\bPediatric Physician\b",
    r"\bPediatric Consultant\b",
    r"\bPediatric Specialist\b",
    r"\bPediatric Doctor\b",
    r"\bChild Healthcare Professional\b",
    r"\bPediatric Surgeon\b",
]

# Exact matches that should be updated
pediatrician_exact_matches = {
    "Pediatrician",
    "Pediatrist",
    "Pediatrics Specialist",
    "Pediatric Doctor",
    "Child Specialist",
    "Pediatrics Physician",
    "Pediatric Consultant",
    "Pediatric Specialist",
    "Pediatric Practitioner",
    "Pediatric Surgeon",
    "General Pediatrician",
    "Pediatrician Consultant",
    "Consultant Pediatrician",
    "Pediatrtion",
    "Pediatrition",
    "Pedriatrician",
    "Peditrician",
    "Pedatrician",
    "Pediatrion",
    "Pediatrian",
    "Pediatra",
    "Pediatra General",
    "Pediatra Especialista",
    "Médico Pediatra",
    "Pediatra Consultor",
    "Pediatra Infantil",
    "Pediatra Pediátrico",
    "Pediatra Cirujano",
    "Pediatra Generalista",
    "Pediatric Physician",
    "Child Healthcare Professional",
}

# # Define patterns (these should NOT be changed)
# pediatrician_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

pediatrician_exclusions = {
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
    'Pediatric Physician Recruiter',
}

# Create a mask for Pediatrician
mask_pediatrician = df['speciality'].str.contains('|'.join(pediatrician_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(pediatrician_exact_matches)

# mask_pediatrician_exclusions = df['speciality'].str.contains(pediatrician_exclusions, case=False, na=False, regex=True)
mask_pediatrician_exclusions = df['speciality'].isin(pediatrician_exclusions)

# Final mask: Select Pediatrician
mask_pediatrician_final = mask_pediatrician & ~mask_pediatrician_exclusions

# Store the original values that will be replaced
original_pediatrician_values = df.loc[mask_pediatrician_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_pediatrician_final, 'speciality'] = 'Pediatrician'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Pediatrician", 'green'))
print(df.loc[mask_pediatrician_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_pediatrician_values = df.loc[mask_pediatrician_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Pediatrician", "cyan"))
for original_pediatrician_value in original_pediatrician_values:
    print(f"✅ {original_pediatrician_value} → Pediatrician")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Pediatrician:", 'red'))
print(grouped_pediatrician_values)

# Print summary
matched_count_pediatrician = mask_pediatrician_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Pediatrician: "
        f"{matched_count_pediatrician}",
        'red'))