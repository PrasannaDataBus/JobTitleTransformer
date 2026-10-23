import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Dentist related titles

dentist_variants = [
    r"\bdentist\b",
    r"\bdentis\b",
    r"\bdentis\s?specialist\b",
    r"\bdentista\b",
    r"\bdentista\s?oral\b",
    r"\bdentista\s?general\b",
    r"\bdoctor\s?dentist\b",
    r"\bDDS\b",
    r"\bDMD\b",
    r"\bOdontologist\b",
    r"\bImplantologist\b",
    r"\bDentistAesthetic Physician\b",
    r"\bGeneral Dentiste\b",
    r"\bMedico Odontoiatra\b",
    r"Odontoiatra",
    r"\bDentistry- Removable Prosthodontics\b",
    r"\bBDS\b",
    r"\bB D S\b",
    r"\bOdontologa\b",
    r"\bOdontologia\b",
    r"\bDentiste\b",
    r"\bDentistry Hof\b",
    r"\bProsthodontics\b",
    r"\bDentist & Aesthetician\b",
    r"\bOdontologist\b",
    r"\bImplantologist\b",
    r"\bDentist Aesthetic Doctor\b",
    r"\bOwner Dentist\b",
    r"\bOdontologa\b",
    r"\bDmd\b",
    r"\bDentistry Hof\b",
    r"\bDentistry\b",
    r"\bDentistry- Removable Prosthodontics\b",
    r"\bB D S\b",
    r"\bSpecialist Of Prosthodontics\b",
    r"\bOrofacial Dentist\b",
    r"\bGeneral Dentist\b",
    r"\bDentista Especialista Em Harmonizacao Orofacial\b",
    r"\bDentista\b",
    r"\bOdontologia\b",
    r"\bDentiste\b",
    r"\bBds\b",
    r"\bDoctor Of Dental Medicine\b",
    r"\bPediatric Dentist\b",
    r"\bDentist Orthodontics\b",
    r"\bDental Medicine\b",
    r"\bOdontoiatraa\b",
    r"\bGeneral Dentiste\b",
    r"\bDendis\b",
    r"\bDentist - Facial Harmonization\b",
    r"\bDentist & Esthetician\b",
    r"\bDentist Aesthetic\b",
    r"\bAesthetics Dentist\b",
    r"\bProsthodontics\b",
    r"\bDental Facial Aesthetics\b",
    r"\bDentistAesthetic Physician\b",
    r"\bDental & Skincare\b",
    r"\bDoctor Of Dental Medical\b",
    r"\bCosmetic Dentist Specializing In Veneers\b",
    r"\bDentist Dmd\b",
    r"\bMedico Odontoiatra\b",
    r"\bDentista Harmonizacao Orofacial\b",
    r"\bDental Doctor\b",
    r"\bDentist & Hp\b",
    r"\bGp Dentist\b",
    r"\bMedica Dentista\b",
    r"\bAesthetic Dentist\b",
    r"\bDoctor Dentist Spec\b",
    r"\bDentist Specializing In Orofacial Harmonization\b",
    r"\bDental Professional Aesthetic Practicioner\b",
    r"\bDental Professional\b",
    r"\bProf  Esthetic Medicine Dentist\b",
    r"\bDentist Naturopath\b",
    r"\bCosmetolog Dentist\b",
    r"\bDentist Aesthetic Medicine Doctor\b",
    r"\bDentist Facial Aesthetics\b",
    r"\bDental Therapist\b",
    r"\bMaxilofacial Dentist\b",
    r"\bStaff Dentist\b",
    r"\bDentist & Aesthetic Practiononer\b",
    r"\bMedico Dentista\b",
    r"\bDentist Facial Aesthetic & Dental Implants\b",
    r"\bDental Prosthodontics\b",
    r"\bCosmetic Dentist\b",
    r"\bAesthetician & Pediatric Dentist\b",
    r"\bDental & Aestetic Doctor\b",
    r"\bDentist & Med Spa\b",
]

# Exact matches that should be updated
dentist_exact_matches = {
    "Dr. Dentist",
    "Dr. [General Dentist]",
    "Dentistry",
    'Dental Clinic',
    'Dental Professional',
    'Dental',
    'Doctor Teeth',
    'DentistFacial Aesthetics',
    'Medicina Dentaria',
    'DentistOwner',
    'GDP',
}

# Define patterns (these should NOT be changed)
dentist_exclusions = [
    r"\bMaxillo\s?Facial\b",
    r"\bMaxillo-Facial\b",
    r"\bRecruiter\b",
] # maxillo variants

# Create a mask for Dentist
mask_dentist = df['speciality'].str.contains('|'.join(dentist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(dentist_exact_matches)
mask_dentist_exclusions = df['speciality'].isin(dentist_exclusions)

# Final mask: Select Dentist
mask_dentist_final = mask_dentist & ~mask_dentist_exclusions

# Store the original values that will be replaced
original_dentist_values = df.loc[mask_dentist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_dentist_final, 'speciality'] = 'Dentist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Dentist", 'green'))
print(df.loc[mask_dentist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_dentist_values = df.loc[mask_dentist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Dentist", "cyan"))
for original_dentist_value in original_dentist_values:
    print(f"✅ {original_dentist_value} → Dentist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Dentist:", 'red'))
print(grouped_dentist_values)

# Print summary
matched_count_dentist = mask_dentist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Dentist: "
        f"{matched_count_dentist}",
        'red'))