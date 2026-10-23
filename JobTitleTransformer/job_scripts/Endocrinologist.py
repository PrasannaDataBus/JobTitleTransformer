import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Endocrinologist related titles

endocrinologist_variants = [
    r"\bendocrinologist\b",
    r"\bendocrinologists\b",
    r"\bendocrinologist\s?doctor\b",
    r"\bendocrinology\s?specialist\b",
    r"\bendocrinologist\s?specialist\b",
    r"\bboard\s?certified\s?endocrinologist\b",
    r"\bdoctor\s?of\s?endocrinology\b",
    r"\bdoctor\s?endocrinologist\b",
    r"\bendocrinologist\s?physician\b",
    r"\bendocrinologist\s?md\b",
    r"\bendocrinologist\s?mds\b",
    r"\bendocrinologist\s?consultant\b",
    r"\bendocrinologist\s?expert\b",
    r"\bendocrinologist\s?doctor\b",
    r"\bendocrinologist\s?physician\s?specialist\b",
    # Spanish variants
    r"\bendocrinólogo\b",
    r"\bendocrinóloga\b",
    r"\bendocrinólogos\b",
    r"\bendocrinólogas\b",
    r"\bespecialista\s?en\s?endocrinología\b",
    r"\bdoctor\s?en\s?endocrinología\b",
    # Misspellings
    r"\bendocrinolgist\b",
    r"\bendocrinologiest\b",
    r"\bendocrinlogist\b",
    r"\bendocrinologist\s?doctor\b",
    r"\bendocrinogist\b",
    r"\bendoocrinologist\b",
    r"\bendocrinolgist\b",
    r"\bendocrinologist\s?md\b",
    # Case-related errors
    r"\bendocrinologist\b",
    r"\bENDOCRINOLOGIST\b",
    r"\bEndocrinologist\b",
    r"\bendocrinologist\b",
    # Other Possible Variations
    r"\bboard\s?certified\s?endocrinologist\b",
    r"\bendocrinology\s?expert\b",
    r"\bendocrinologist\s?specialist\b",
    r"\bendocrinology\s?doctor\b",
    r"\bendocrinologist\s?consultant\b",
    r"\bendocrinology\s?practitioner\b",
    r"\bendocrinologist\s?physician\b",
    r"\bendocrine\s?specialist\b",
    r"\bendocrinologist\s?expert\b",
    r"\bMedico Endocrinologista\b",
    r"Endocrinologista",
    r"Endocrinoligista",
    r"\bHrt Pellet Therapy\b",
    r"\bEndocrino\b",
    r"\bHormone Optimization Coordinator\b",
]

# Exact matches that should be updated
endocrinologist_exact_matches = {
    "Endocrinologist",
    "Endocrinologists",
    "Endocrinologist Doctor",
    "Endocrinology Specialist",
    "Endocrinologist Specialist",
    "Board Certified Endocrinologist",
    "Doctor of Endocrinology",
    "Doctor Endocrinologist",
    "Endocrinologist Physician",
    "Endocrinologist MD",
    "Endocrinologist MDs",
    "Endocrinologist Consultant",
    "Endocrinologist Expert",
    "Endocrinologist Physician Specialist",
    "Endocrinólogo",
    "Endocrinóloga",
    "Endocrinólogos",
    "Endocrinólogas",
    "Especialista en Endocrinología",
    "Doctor en Endocrinología",
    "Endocrinolgist",
    "Endocrinologiest",
    "Endocrinlogist",
    "Endocrinogist",
    "Endoocrinologist",
    "ENDOCRINOLOGIST",
    "endocrinologist",
    "Endocrinology Expert",
    "Endocrinology Doctor",
    "Endocrinology Practitioner",
    "Endocrine Specialist",
    'Director Obesity Chair',
}

# Define patterns (these should NOT be changed)
endocrinologist_exclusions = {
    'Resident',
    'resident',
    'student',
    'Trainee',
    'Resident Doctor',
    'Resident Physician',
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

# Create a mask for Endocrinologist
mask_endocrinologist = df['speciality'].str.contains('|'.join(endocrinologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(endocrinologist_exact_matches)
mask_endocrinologist_exclusions = df['speciality'].isin(endocrinologist_exclusions)

# Final mask: Select Endocrinologist
mask_endocrinologist_final = mask_endocrinologist & ~mask_endocrinologist_exclusions

# Store the original values that will be replaced
original_endocrinologist_values = df.loc[mask_endocrinologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_endocrinologist_final, 'speciality'] = 'Endocrinologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Endocrinologist", 'green'))
print(df.loc[mask_endocrinologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_endocrinologist_values = df.loc[mask_endocrinologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Endocrinologist", "cyan"))
for original_endocrinologist_value in original_endocrinologist_values:
    print(f"✅ {original_endocrinologist_value} → Endocrinologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Endocrinologist:", 'red'))
print(grouped_endocrinologist_values)

# Print summary
matched_count_endocrinologist = mask_endocrinologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Endocrinologist: "
        f"{matched_count_endocrinologist}",
        'red'))