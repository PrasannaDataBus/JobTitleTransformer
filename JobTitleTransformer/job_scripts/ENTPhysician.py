import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for ENT Ear Nose Throat Physician related titles

ENT_variants = [
    r"\bENT\s?physician\b",
    r"\bENT\s?doctor\b",
    r"\bENT\s?specialist\b",
    r"\bENT\s?specialist\s?doctor\b",
    r"\bENT\s?consultant\b",
    r"\bENT\s?practitioner\b",
    r"\bENT\s?expert\b",
    r"\bENT\s?surgeon\b",
    r"\bENT\s?surgeon\s?doctor\b",
    r"\bENT\s?MD\b",
    r"\bENT\s?physician\s?MD\b",
    r"\bENT\s?physician\s?specialist\b",
    r"\bboard\s?certified\s?ENT\s?physician\b",
    # Spanish variants
    r"\botorrihinolaringólogo\b",
    r"\botorrihinolaringóloga\b",
    r"\botorrihinolaringólogos\b",
    r"\botorrihinolaringólogas\b",
    r"\bespecialista\s?en\s?otorinolaringología\b",
    r"\bdoctor\s?en\s?otorinolaringología\b",
    # Ear, Nose, Throat variations
    r"\bEar\s?Nose\s?Throat\s?specialist\b",
    r"\bEar\s?Nose\s?Throat\s?doctor\b",
    r"\bEar\s?Nose\s?Throat\s?physician\b",
    r"\bEar\s?Nose\s?Throat\s?surgeon\b",
    r"\bEar\s?Nose\s?Throat\s?specialist\s?doctor\b",
    r"\bEar\s?Nose\s?Throat\s?MD\b",
    r"\bENT\s?Ear\s?Nose\s?Throat\b",
    # Misspellings
    r"\bOTR\s?physician\b",
    r"\bENTP\b",
    r"\bENT\s?phyician\b",
    r"\bENT\s?phyisician\b",
    r"\bENT\s?dr\b",
    # Case-related errors
    r"\bENT\s?PHYSICIAN\b",
    r"\bENT\s?Physician\b",
    r"\bENT\s?physician\b",
    # Other Possible Variations
    r"\bboard\s?certified\s?ENT\s?physician\b",
    r"\bENT\s?consultant\b",
    r"\bENT\s?expert\b",
    r"\bENT\s?specialist\b",
    r"\bENT\s?doctor\b",
    r"\bENT\s?physician\s?specialist\b",
    r"\bMedica Otorrinolaringologista\b",
    r"\bOtorrinolaringologista\b",
    r"\bOtorrinolaringologista\b",
    r"\bOtolayngologist\b",
    r"\bOtorhinolaryngology\b",
    r"Otorrino Cirugia Estetica",
    r"\bOtolarygology\b",
    r"\bOtorhinolaryngology\b",
]

# Exact matches that should be updated
ENT_exact_matches = {
    'ENT Ear Nose & Throat Physician',
    "ENT Physician",
    "ENT Doctor",
    "ENT Specialist",
    "ENT Specialist Doctor",
    "ENT Consultant",
    "ENT Practitioner",
    "ENT Expert",
    "ENT Surgeon",
    "ENT Surgeon Doctor",
    "ENT MD",
    "ENT Physician MD",
    "ENT Physician Specialist",
    "Board Certified ENT Ear Nose Throat Physician",
    "Otorrihinolaringólogo",
    "Otorrihinolaringóloga",
    "Otorrihinolaringólogos",
    "Otorrihinolaringólogas",
    "Especialista en Otorrinolaringología",
    "Doctor en Otorrinolaringología",
    "OTR Physician",
    "ENTP",
    "ENT Phyician",
    "ENT Phyisician",
    "ENT Dr",
    "ENT PHYSICIAN",
    "ent physician",
    "Ear Nose Throat Specialist",
    "Ear Nose Throat Doctor",
    "Ear Nose Throat Physician",
    "Ear Nose Throat Surgeon",
    "Ear Nose Throat Specialist Doctor",
    "Ear Nose Throat MD",
    "ENT Ear Nose Throat",
    "Ent Ear Nose & Throat",
    'Otolarygology',
    'Otorhinolaryngology',
    "Otorrinolaringologista",
    "Otorrinolaringologista",
    "Otolayngologist",
    "Otolaryngology",
    "Otorhinolaryngology",
    'Ent',
    'Doctor Ent',
}

# Define patterns (these should NOT be changed)
ENT_exclusions = {
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
    'Ent Resident',
    'Professor Of Otorhinolaryngology',
    'Ent Plastic Surgery',
    'Consultant Ent Rhinologist & Facial Plastic Surgeon',
    'University ProfessorOtolaryngologyFacial Plastic',
    "ENT Head and Neck Physician",
    "ENT Head and Neck Doctor",
    "ENT Head and Neck Specialist",
    "ENT Head and Neck Surgeon",
    "ENT Head and Neck MD",
    "ENT Head and Neck Consultant",
    "ENT Head and Neck Practitioner",
    "ENT Head and Neck Expert",
    "ENT Head and Neck Surgeon Doctor",
    "Board Certified ENT Head and Neck Physician",
    "Head and Neck ENT Specialist",
    "Head and Neck ENT Doctor",
    "Head and Neck ENT Surgeon",
    "Head and Neck ENT Physician",
    "Head and Neck ENT Consultant",
    "ENT Head & Neck Specialist",
    "ENT Head & Neck Doctor",
    "ENT Head & Neck Surgeon",
    "ENT Head & Neck MD",
    "ENT Head & Neck Consultant",
    "Especialista en Cabeza y Cuello",
    "Cirujano de Cabeza y Cuello",
    "Médico de Cabeza y Cuello",
    "Otorrinolaringólogo de Cabeza y Cuello",
    "Ear Nose Throat Head and Neck Specialist",
    "Ear Nose Throat Head and Neck Doctor",
    "Ear Nose Throat Head and Neck Surgeon",
    "Ear Nose Throat Head and Neck Physician",
    "Ear Nose Throat Head and Neck MD",
    "ENT Ear Nose Throat Head and Neck",
    "ENT H&N Physician",
    "ENT H&N Doctor",
    "ENT H&N Specialist",
    "ENT H&N Surgeon",
    "ENT H&N MD",
    "ENT H&N Consultant",
    'ENT/Head & Neck Specialist',
    'ENTHead & Neck Specialist',
    "EntHead & Neck Surgery",
    "Head & Neck Surgery",
    "EntHead & Neck Surgeon",
    "Head & Neck Surgeon",
    "Head & Neck Specialist",
}

# Create a mask for ENT Ear Nose Throat Physician
mask_ENT = df['speciality'].str.contains('|'.join(ENT_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(ENT_exact_matches)
mask_ENT_exclusions = df['speciality'].isin(ENT_exclusions)

# Final mask: Select ENT Ear Nose Throat Physician
mask_ENT_final = mask_ENT & ~mask_ENT_exclusions

# Store the original values that will be replaced
original_ENT_values = df.loc[mask_ENT_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_ENT_final, 'speciality'] = 'ENT Ear Nose Throat Physician'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: ENT Ear Nose Throat Physician", 'green'))
print(df.loc[mask_ENT_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_ENT_values = df.loc[mask_ENT_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: ENT Ear Nose Throat Physician", "cyan"))
for original_ENT_value in original_ENT_values:
    print(f"✅ {original_ENT_value} → ENT Ear Nose Throat Physician")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with ENT Ear Nose Throat Physician:", 'red'))
print(grouped_ENT_values)

# Print summary
matched_count_ENT = mask_ENT_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to ENT Ear Nose Throat Physician: "
        f"{matched_count_ENT}",
        'red'))

# Fix / Handle ENT Head and Neck which is important value for EUROGIN

ENT_head_neck_variants = [
    r"\bENT\s?head\s?and\s?neck\s?physician\b",
    r"\bENT\s?head\s?and\s?neck\s?doctor\b",
    r"\bENT\s?head\s?and\s?neck\s?specialist\b",
    r"\bENT\s?head\s?and\s?neck\s?surgeon\b",
    r"\bENT\s?head\s?and\s?neck\s?MD\b",
    r"\bENT\s?head\s?and\s?neck\s?consultant\b",
    r"\bENT\s?head\s?and\s?neck\s?practitioner\b",
    r"\bENT\s?head\s?and\s?neck\s?expert\b",
    r"\bENT\s?head\s?and\s?neck\s?surgeon\s?doctor\b",
    r"\bboard\s?certified\s?ENT\s?head\s?and\s?neck\s?physician\b",
    r"\bhead\s?and\s?neck\s?ENT\s?specialist\b",
    r"\bhead\s?and\s?neck\s?ENT\s?doctor\b",
    r"\bhead\s?and\s?neck\s?ENT\s?surgeon\b",
    r"\bhead\s?and\s?neck\s?ENT\s?physician\b",
    r"\bhead\s?and\s?neck\s?ENT\s?consultant\b",
    r"\bENT\s?head\s?&\s?neck\s?specialist\b",
    r"\bENT\s?head\s?&\s?neck\s?doctor\b",
    r"\bENT\s?head\s?&\s?neck\s?surgeon\b",
    r"\bENT\s?head\s?&\s?neck\s?MD\b",
    r"\bENT\s?head\s?&\s?neck\s?consultant\b",
    # Spanish Variants
    r"\bEspecialista\s?en\s?cabeza\s?y\s?cuello\b",
    r"\bCirujano\s?de\s?cabeza\s?y\s?cuello\b",
    r"\bMédico\s?de\s?cabeza\s?y\s?cuello\b",
    r"\bOtorrinolaringólogo\s?de\s?cabeza\s?y\s?cuello\b",
    # Ear, Nose, Throat, Head and Neck Variations
    r"\bHead\s?and\s?Neck\s?specialist\b",
    r"\bHead\s?and\s?Neck\s?doctor\b",
    r"\bHead\s?and\s?Neck\s?surgeon\b",
    r"\bHead\s?and\s?Neck\s?physician\b",
    r"\bHead\s?and\s?Neck\s?MD\b",
    # Common Misspellings
    r"\bENT\s?head\s?and\s?neck\s?phyisician\b",
    r"\bENT\s?head\s?and\s?neck\s?phyician\b",
    r"\bENT\s?H&N\s?physician\b",
    r"\bENT\s?H&N\s?doctor\b",
    r"\bENT\s?H&N\s?specialist\b",
    r"\bENT\s?H&N\s?surgeon\b",
    r"\bENT\s?H&N\s?MD\b",
    r"\bENT\s?H&N\s?consultant\b",
    r"\bENT/Head & Neck Specialist\b",
    r"\bEntHead & Neck Specialist\b",
    r"\bEntHead & Neck Surgery\b",
    r"\bHead & Neck Surgery\b",
    r"\bEntHead & Neck Surgeon\b",
    r"\bHead & Neck Surgeon\b",
    r"\bHead & Neck Specialist\b",
    r"\bENT/Head & Neck Specialist\b"
]


ENT_head_neck_exact_matches = {
    'ENT/Head & Neck Specialist',
    "ENT Head and Neck Physician",
    "ENT Head and Neck Doctor",
    "ENT Head and Neck Specialist",
    "ENT Head and Neck Surgeon",
    "ENT Head and Neck MD",
    "ENT Head and Neck Consultant",
    "ENT Head and Neck Practitioner",
    "ENT Head and Neck Expert",
    "ENT Head and Neck Surgeon Doctor",
    "Board Certified ENT Head and Neck Physician",
    "Head and Neck ENT Specialist",
    "Head and Neck ENT Doctor",
    "Head and Neck ENT Surgeon",
    "Head and Neck ENT Physician",
    "Head and Neck ENT Consultant",
    "ENT Head & Neck Specialist",
    "ENT Head & Neck Doctor",
    "ENT Head & Neck Surgeon",
    "ENT Head & Neck MD",
    "ENT Head & Neck Consultant",
    "Especialista en Cabeza y Cuello",
    "Cirujano de Cabeza y Cuello",
    "Médico de Cabeza y Cuello",
    "Otorrinolaringólogo de Cabeza y Cuello",
    "Ear Nose Throat Head and Neck Specialist",
    "Ear Nose Throat Head and Neck Doctor",
    "Ear Nose Throat Head and Neck Surgeon",
    "Ear Nose Throat Head and Neck Physician",
    "Ear Nose Throat Head and Neck MD",
    "ENT Ear Nose Throat Head and Neck",
    "ENT H&N Physician",
    "ENT H&N Doctor",
    "ENT H&N Specialist",
    "ENT H&N Surgeon",
    "ENT H&N MD",
    "ENT H&N Consultant",
    'ENT/Head & Neck Specialist',
    'ENTHead & Neck Specialist',
    "EntHead & Neck Surgery",
    "Head & Neck Surgery",
    "EntHead & Neck Surgeon",
    "Head & Neck Surgeon",
    "Head & Neck Specialist",
    'Dr  Ent&Hns',
}

# Define patterns (these should NOT be changed)
ENT_head_neck_exclusions = {
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
    'Ent Resident',
    'Professor Of Otorhinolaryngology',
    'Ent Plastic Surgery',
    'Consultant Ent Rhinologist & Facial Plastic Surgeon',
    'University ProfessorOtolaryngologyFacial Plastic',
    'ENT Ear Nose Throat Physician',
    "ENT Physician",
    "ENT Doctor",
    "ENT Specialist",
    "ENT Specialist Doctor",
    "ENT Consultant",
    "ENT Practitioner",
    "ENT Expert",
    "ENT Surgeon",
    "ENT Surgeon Doctor",
    "ENT MD",
    "ENT Physician MD",
    "ENT Physician Specialist",
    "Board Certified ENT Ear Nose Throat Physician",
    "Otorrihinolaringólogo",
    "Otorrihinolaringóloga",
    "Otorrihinolaringólogos",
    "Otorrihinolaringólogas",
    "Especialista en Otorrinolaringología",
    "Doctor en Otorrinolaringología",
    "OTR Physician",
    "ENTP",
    "ENT Phyician",
    "ENT Phyisician",
    "ENT Dr",
    "ENT PHYSICIAN",
    "ent physician",
    "Ear Nose Throat Specialist",
    "Ear Nose Throat Doctor",
    "Ear Nose Throat Physician",
    "Ear Nose Throat Surgeon",
    "Ear Nose Throat Specialist Doctor",
    "Ear Nose Throat MD",
    "ENT Ear Nose Throat",
    "Ent Ear Nose & Throat",
}


# Create a mask for ENT Ear Nose Throat Physician
mask_ENT_head_neck = df['speciality'].str.contains('|'.join(ENT_head_neck_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(ENT_head_neck_exact_matches)
mask_ENT_head_neck_exclusions = df['speciality'].isin(ENT_head_neck_exclusions)

# Final mask: Select ENT Ear Nose Throat Physician
mask_ENT_head_neck_final = mask_ENT_head_neck & ~mask_ENT_head_neck_exclusions

# Store the original values that will be replaced
original_ENT_head_neck_values = df.loc[mask_ENT_head_neck_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_ENT_head_neck_final, 'speciality'] = 'ENT Head and Neck Specialist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: ENT Head and Neck Specialist", 'green'))
print(df.loc[mask_ENT_head_neck_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_ENT_head_neck_values = df.loc[mask_ENT_head_neck_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: ENT Head and Neck Specialist", "cyan"))
for original_ENT_head_neck_value in original_ENT_head_neck_values:
    print(f"✅ {original_ENT_head_neck_value} → ENT Head and Neck Specialist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with ENT Head and Neck Specialist:", 'red'))
print(grouped_ENT_head_neck_values)

# Print summary
matched_count_ENT_head_neck = mask_ENT_head_neck_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to ENT Head and Neck Specialist: "
        f"{matched_count_ENT_head_neck}",
        'red'))