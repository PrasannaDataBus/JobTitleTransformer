import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Pharmacist related titles

pharmacist_variants = [
    # Standard Titles & Variants
    r"\bPharmacist\b",
    r"\bPharmacy Specialist\b",
    r"\bClinical Pharmacist\b",
    r"\bCommunity Pharmacist\b",
    r"\bHospital Pharmacist\b",
    r"\bPharmacological Specialist\b",
    r"\bPharmaceutical Professional\b",
    r"\bPharmacy Doctor\b",
    r"\bLicensed Pharmacist\b",
    r"\bPharmacist Consultant\b",
    r"\bConsultant Pharmacist\b",
    r"\bPharmacy\b",
    r"\bPharma\b",
    r"\bPharmd\b",
    r"\bM8Pharma\b",

    # Misspellings & Typographical Errors
    r"\bPharmicist\b",
    r"\bFarmacist\b",
    r"\bPhamacist\b",
    r"\bPharmasist\b",
    r"\bPharmocist\b",
    r"\bPharacist\b",
    r"\bPharmacisst\b",

    # Case Variations
    r"\bpharmacist\b",
    r"\bPHARMACIST\b",
    r"\bPhArMaCiSt\b",
    r"\bPhArMacIst\b",

    # Spanish Variants
    r"\bFarmacéutico\b",
    r"\bFarmacéutica\b",
    r"\bFarmacéutico\s?Clínico\b",
    r"\bFarmacéutico\s?Comunitario\b",
    r"\bFarmacéutico\s?Hospitalario\b",
    r"\bEspecialista\s?Farmacéutico\b",
    r"\bDoctor\s?Farmacéutico\b",
    r"\bFarmacéutico\s?Consultor\b",
    r"\bConsultor\s?Farmacéutico\b",
    r"\bProfesional\s?Farmacéutico\b",
    r"\bFarmacia\s?Clínica\b",

    # Other Possible Variations
    r"\bPharmacy Professional\b",
    r"\bPharmacy Consultant\b",
    r"\bPharmaceutical Practitioner\b",
    r"\bPharmaceutical Care Specialist\b",
    r"\bPharmaceutical Practitioner\b",
    r"Farmaceutica",
    r"\bFarmalider\b",
]

# Exact matches that should be updated
pharmacist_exact_matches = {
    "Pharmacist",
    "Pharmacy Specialist",
    "Clinical Pharmacist",
    "Community Pharmacist",
    "Hospital Pharmacist",
    "Pharmacological Specialist",
    "Pharmaceutical Professional",
    "Pharmacy Doctor",
    "Licensed Pharmacist",
    "Pharmacist Consultant",
    "Consultant Pharmacist",
    "Pharmicist",
    "Farmacist",
    "Phamacist",
    "Pharmasist",
    "Pharmocist",
    "Pharacist",
    "Pharmacisst",
    "Farmacéutico",
    "Farmacéutica",
    "Farmacéutico Clínico",
    "Farmacéutico Comunitario",
    "Farmacéutico Hospitalario",
    "Especialista Farmacéutico",
    "Doctor Farmacéutico",
    "Farmacéutico Consultor",
    "Consultor Farmacéutico",
    "Profesional Farmacéutico",
    "Farmacia Clínica",
    "Pharmacy Professional",
    "Pharmacy Consultant",
    "Pharmaceutical Practitioner",
    "Pharmaceutical Care Specialist",
    'Apothecary',
    'Pharmacists',
    'D Pham',
    'PharmacistClinical Staff',
}

# # Define patterns (these should NOT be changed)
# pharmacist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

pharmacist_exclusions = {
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
    'Pharma Sales Manager',
}

# Create a mask for Pharmacist
mask_pharmacist = df['speciality'].str.contains('|'.join(pharmacist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(pharmacist_exact_matches)

# mask_pharmacist_exclusions = df['speciality'].str.contains(pharmacist_exclusions, case=False, na=False, regex=True)
mask_pharmacist_exclusions = df['speciality'].isin(pharmacist_exclusions)

# Final mask: Select Pharmacist
mask_pharmacist_final = mask_pharmacist & ~mask_pharmacist_exclusions

# Store the original values that will be replaced
original_pharmacist_values = df.loc[mask_pharmacist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_pharmacist_final, 'speciality'] = 'Pharmacist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Pharmacist", 'green'))
print(df.loc[mask_pharmacist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_pharmacist_values = df.loc[mask_pharmacist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Pharmacist", "cyan"))
for original_pharmacist_value in original_pharmacist_values:
    print(f"✅ {original_pharmacist_value} → Pharmacist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Pharmacist:", 'red'))
print(grouped_pharmacist_values)

# Print summary
matched_count_pharmacist = mask_pharmacist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Pharmacist: "
        f"{matched_count_pharmacist}",
        'red'))