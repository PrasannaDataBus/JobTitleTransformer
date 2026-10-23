import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Student Resident Fellow related titles

student_variants = [
# Standard Titles & Variants
    r"\bStudent Resident Fellow\b",  # General term for Student Resident Fellow
    r"\bMedical Student\b",  # Common term for medical students
    r"\bResident Physician\b",  # Resident physician
    r"\bResident Doctor\b",  # Another common term for resident doctors
    r"\bFellow Physician\b",  # Fellow of a specialty
    r"\bResident\b",  # Fellow of a specialty
    r"\bStudent\b",  # Fellow of a specialty
    r"\bFellow\b",  # Fellow of a specialty
    r"\bIntern\b",  # Fellow of a specialty
    r"\bStudy\b",
    r"\bMedica Residente\b",
    r"\bMedico Residente\b",
    r"Residente",
    r"Estudante",
    r"\bMedical School\b",
    r"\bTrainee\b",
    r"\bStudents\b",
    r"\bSenior Resident Department Of Plastic Surgery\b",
    r"\bEstudiante\b",
    r"\bResidence\b",

    # Misspellings & Typographical Errors
    r"\bStudnet Resident Fellow\b",  # Common misspelling
    r"\bSudent Resident Fellow\b",  # Typo with missing 't'
    r"\bStudent Residen Fellow\b",  # Misspelling with 'Resident' typo
    r"\bStduent Resident Fellow\b",  # Misspelling with 't' misplaced
    r"\bStuden Resident Fellow\b",  # Missing 't' in Student

    # Case Variations
    r"\bSTUDENT RESIDENT FELLOW\b",  # Uppercase variant
    r"\bstudent resident fellow\b",  # Lowercase variant
    r"\bStUdEnT ReSiDeNt FeLlOw\b",  # Mixed case variant

    # Spanish Variants
    r"\bEstudiante Residente\b",  # Student Resident in Spanish
    r"\bMédico Residente\b",  # Resident Physician in Spanish
    r"\bResidente Médico\b",  # Another variation for Resident Doctor in Spanish
    r"\bFellow Médico\b",  # Fellow Physician in Spanish

    # Hybrid Spanish-English Variants
    r"\bEstudiante Médico Residente\b",  # Hybrid term for Medical Student Resident
    r"\bFellow Residente Médico\b",  # Hybrid term for Fellow Resident Physician

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bResident Physician Fellow\b",  # Specialized term for residency fellow
    r"\bMedical Resident Fellow\b",  # Common term for medical resident fellows
    r"\bDoctoral Fellow\b",  # Doctoral-level fellow
    r"\bSpecialty Fellow\b",  # Specialty-focused fellowship term
    r"\bDoctor Fellow\b",  # Variant for a general Doctor Fellow
]

# Exact matches that should be updated
student_exact_matches = {
    'Student/Resident',
    'StudentResident',
    'Student Resident',
    'Junior Doctor',
    'Estudannte',
    'Etudiant',
    'ResidentPeriodontist',
    'Estudande de Biomedicina',
}

# # Define patterns (these should NOT be changed)
# student_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

student_exclusions = {'Nurse'}

# Create a mask for Student Resident Fellow
mask_student = df['speciality'].str.contains('|'.join(student_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(student_exact_matches)

# mask_student_exclusions = df['speciality'].str.contains(student_exclusions, case=False, na=False, regex=True)
mask_student_exclusions = df['speciality'].isin(student_exclusions)

# Final mask: Select Student Resident Fellow
mask_student_final = mask_student & ~mask_student_exclusions

# Store the original values that will be replaced
original_student_values = df.loc[mask_student_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_student_final, 'speciality'] = 'Student Resident Fellow'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Student Resident Fellow", 'green'))
print(df.loc[mask_student_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_student_values = df.loc[mask_student_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Student Resident Fellow", "cyan"))
for original_student_value in original_student_values:
    print(f"✅ {original_student_value} → Student Resident Fellow")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Student Resident Fellow:", 'red'))
print(grouped_student_values)

# Print summary
matched_count_student = mask_student_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Student Resident Fellow: "
        f"{matched_count_student}",
        'red'))