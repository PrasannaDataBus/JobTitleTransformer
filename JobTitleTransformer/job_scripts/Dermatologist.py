import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Dermatologist related titles

dermatologist_variants = [
    r"\bdermatologist\b",
    r"\bdermatologists\b",
    r"\bdermatologist\s?md\b",
    r"\bdermatologist\s?doctor\b",
    r"\bdermatology\s?specialist\b",
    r"\bboard-certified\s?dermatologist\b",
    r"\bcertified\s?dermatologist\b",
    r"\bskin\s?specialist\b",
    r"\bdoctor\s?of\s?dermatology\b",
    r"\bdermatology\s?physician\b",
    r"\bdermatologiste\b",
    r"\bdermatologo\b",
    r"\bdermatologo(a)?\b",
    r"\bDermatologista\b",
    r"\bDermatologia\b",
    r"\bMedica Dermatologista\b",
    r"\bDermatologue\b",
    r"\bDermatologie\b",
    r"\bDermatologa\b",
    r"\bDermatovenereologist\b",
    r"\bDermatology & Venereology\b",
    r"\bAesthetic Dermatilogy\b",
    r"\bAesthetic Dernatology\b",
    r"\bAesthetic MedicineDermatology\b",
    r"\bMedica Dematologista\b",
    r"\bDermatogist\b",
    r"\bHead Of Dermatology\b",
    r"\bMole Screening\b",
    r"\bAesthetic & Clinical Dermatology\b",
    r"\bMsc Dermatology\b",
    r"\bPedderm\b",
    r"\bDermat\b",
    r"\bDermatologyst\b",
    r"\bDermathology\b",
    r"\bDermatologi Dan Venereologi\b",
    r"\bDermatovenerologist\b",
    r"\bDermatologyst\b",
    r"\bDermatologyst\b",
    r"\bDermatovenerology\b",
    r"\bDeematology\b",
    r"\bDermotoloji\b",
    r"\bDermatolgy\b",
    r"\bSkin Medical & Aesthetic\b",
    r"\bDermatoloji\b",
    r"\bDermstolog\b",
    r"\bImmunodermatology\b",
    r"\bDeramtology\b",
    r"\bSkin Msc\b",
    r"\bFamily PracticeDermatology\b",
    r"\bDermato Funcional\b",
    r"\bDermatologiss\b",
    r"\bSkin Specialist\b",
    r"\bDr Skin Care Professional\b",
    r"\bAesthetic DermatologistAnti-Aging\b",
]

# Exact matches that should be updated
dermatologist_exact_matches = {
    "Dermatologist",
    "Dermatologists",
    "Dermatologist MD",
    "Board-Certified Dermatologist",
    "Certified Dermatologist",
    "Doctor of Dermatology",
    "Skin Specialist",
    "Dermatologo",
    "Dermatologo(a)",
    "Dermatology",
    "Derm",
    "Derma",
    "Skin",
    "Aesthetic Dermatology",
    "Skin Clinic",
    'Filler',
    'Specialist Dermatology',
    'ConsultantDermatology',
    'Dermal Clinician',
    'Dermato',
    'Dermatolog',
    'Doctor Dermatology',
    'Md PhdDermatologist',
    'Chairman Dermatology Department',
    'Aesthetics & Dermatology',
    'Chair Of The Department Of Dermatology ',
    'Medicos Dermatologistas Credenciados A SbdSbcp',
    'Skin Aesthetic',
    'Chair Of The Department Of Dermatology',
    'Dermato Venereologist',
    'Dermatology & Aesthetic Medicine',
    'Dermatology & Medical Aesthetics',
    'Deematologist',
    'Specialist In Dermatology',
    'Dermatologogist',
    'Dermatolyst',
    'Dermatoly',
    'DermatologistaDermatologia Estetica',
    'Dermato-Venereologist',
    'Consultants Dermatology',
    'Dermatology Consultant',
}

# Define patterns (these should NOT be changed)
dermatologist_exclusions = {
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
    'Cosmetic Dermatologist',
    'Estudiante De Dermatologia  Cosmetologa En Ucrania',
    'Resident Of Dermatology & Venereology',
    'Resident Of Dermatovenereologist',
    'Dermatovenereologist Resident',
    'Consultant Dermatologist & Hair Transplant Surgeon',
    'Professor Of Dermatology & Co-Director Immunodermatology Laboratory',
    'Dermatologist Resident',
    'Residence Dermatologist',
    'Dermatologie Residence',
    'Sales Medical Dermatology Specialist',
    'Sales Executive & Immunology Dermatology Specialist',
    'Immunology Sales -Dermatology Specialist',
    'Dermatology Physician Assistant',
    'Immunology Sales Dermatology Specialist',
    'Resident dermatologist',
}

# Create a mask for Dermatologist
mask_dermatologist = df['speciality'].str.contains('|'.join(dermatologist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(dermatologist_exact_matches)
mask_dermatologist_exclusions = df['speciality'].isin(dermatologist_exclusions)

# Final mask: Select Dermatologist
mask_dermatologist_final = mask_dermatologist & ~mask_dermatologist_exclusions

# Store the original values that will be replaced
original_dermatologist_values = df.loc[mask_dermatologist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_dermatologist_final, 'speciality'] = 'Dermatologist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Dermatologist", 'green'))
print(df.loc[mask_dermatologist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_dermatologist_values = df.loc[mask_dermatologist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Dermatologist", "cyan"))
for original_dermatologist_value in original_dermatologist_values:
    print(f"✅ {original_dermatologist_value} → Dermatologist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Dermatologist:", 'red'))
print(grouped_dermatologist_values)

# Print summary
matched_count_dermatologist = mask_dermatologist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Dermatologist: "
        f"{matched_count_dermatologist}",
        'red'))