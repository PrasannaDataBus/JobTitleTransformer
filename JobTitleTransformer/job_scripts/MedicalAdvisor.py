import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Medical Advisor related titles

medical_advisor_variants = [
    # Standard Titles & Abbreviations
    r"\bMedical\s?Advisor\b",
    r"\bMedical\s?Affairs\s?Advisor\b",
    r"\bHealthcare\s?Advisor\b",
    r"\bMedical\s?Affairs\s?Specialist\b",
    r"\bScientific\s?Advisor\b",
    r"\bClinical\s?Advisor\b",
    r"\bSenior\s?Medical\s?Advisor\b",
    r"\bChief\s?Medical\s?Advisor\b",
    r"\bMedical\s?Affairs\s?Manager\b",
    r"\bHead Of Advisory\b",
    r"\bPhysician Liason\b",
    r"\bApprentice Medical Communication\b",
    r"\bMsd\b",
    r"\bScience Executive Advisor\b",
    r"\bSenior Regulatory Advisor\b",

    # Misspellings & Typographical Errors
    r"\bMedcial\s?Advisor\b",
    r"\bMediacl\s?Advisor\b",
    r"\bMedical\s?Advisr\b",
    r"\bMedical\s?Advissor\b",
    r"\bMedical\s?Advisro\b",
    r"\bMedcial\s?Advisr\b",
    r"\bMedical\s?Advizeor\b",
    r"\bMedicall\s?Advisor\b",
    r"\bMedical\s?Advisour\b",
    r"\bMedical\s?Adviosr\b",

    # Case Variations
    r"\bmedical advisor\b",
    r"\bMedical advisor\b",
    r"\bmedical Advisor\b",
    r"\bMEDICAL ADVISOR\b",
    r"\bMedIcal AdvIsor\b",

    # Spanish Variants
    r"\bAsesor\s?Médico\b",
    r"\bEspecialista\s?en\s?Asuntos\s?Médicos\b",
    r"\bConsejero\s?Médico\b",
    r"\bDirector\s?Médico\s?Consultor\b",
    r"\bGestor\s?de\s?Asuntos\s?Médicos\b",
    r"\bAsesor\s?de\s?Salud\b",

    # Other Possible Variations (Including Doctor/Specialist Titles)
    r"\bMedical\s?Director\b",
    r"\bMedical\s?Strategy\s?Advisor\b",
    r"\bRegulatory\s?Medical\s?Advisor\b",
    r"\bPharmaceutical\s?Advisor\b",
    r"\bDrug\s?Safety\s?Advisor\b",
    r"\bClinical\s?Regulatory\s?Advisor\b",
    r"\bSenior\s?Medical\s?Consultant\b",
    r"\bGlobal\s?Medical\s?Advisor\b",
    r"\bHealth\s?Policy\s?Advisor\b",
    r"\bHealthcare\s?Regulatory\s?Advisor\b",
    r"\bMedical Affairs Lead\b",
]

# Exact matches that should be updated
medical_advisor_exact_matches = {
    "Medical Advisor",
    "Medical Affairs Advisor",
    "Healthcare Advisor",
    "Medical Affairs Specialist",
    "Scientific Advisor",
    "Clinical Advisor",
    "Senior Medical Advisor",
    "Chief Medical Advisor",
    "Medical Affairs Manager",
    "Medcial Advisor",
    "Mediacl Advisor",
    "Medical Advisr",
    "Medical Advissor",
    "Medical Advisro",
    "Medcial Advisr",
    "Medical Advizeor",
    "Medicall Advisor",
    "Medical Advisour",
    "Medical Adviosr",
    "Asesor Médico",
    "Especialista en Asuntos Médicos",
    "Consejero Médico",
    "Director Médico Consultor",
    "Gestor de Asuntos Médicos",
    "Asesor de Salud",
    "Medical Director",
    "Medical Strategy Advisor",
    "Regulatory Medical Advisor",
    "Pharmaceutical Advisor",
    "Drug Safety Advisor",
    "Clinical Regulatory Advisor",
    "Senior Medical Consultant",
    "Global Medical Advisor",
    "Health Policy Advisor",
    "Healthcare Regulatory Advisor",
    "Surgical Equipment",
    'Advisor',
    'Adviser',
    'Director Of Medical Supply',
    'Program Manager Health Public & Government Affairs',
    'Medicina Estrategica',
    'Director II Skincare Clinical Development & Medical Affairs',
    'Global Medical Advocacy',
    'HCP Advocacy',
    'MEDICA',
    'MEDICO',
    'MSL',
    'Medical Affairs Clinician',
    'Medical Science Liaison Skincare',
    'Physician Advisor',
    'Certified Dermatology Coder',
    'Dermatology Medical Affairs Head Us',
    'Director Field Medical Dermatology',
    'Director Medical Affairs Dermatology Us',
    'Medical Science Dermatology & Iai Liaison',
    'Medical Science Executive & Dermatology Immunology Liaison',
    'Director Medical Affairs',
    'Director Medical Affairs Clinical & Medical Affairs',
    'Medical Affairs',
    'Sr  Director Medical Affairs',
    'Associate Medical Affair Advisor - Neuromodulators',
    'DMP',
}

# Define patterns (these should NOT be changed)
medical_advisor_exclusions = r'\b(?:Plastic)|(?:Physician)|(?:Neonatology)\b'

# Create a mask for Medical Advisor
mask_medical_advisor = df['speciality'].str.contains('|'.join(medical_advisor_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(medical_advisor_exact_matches)
mask_medical_advisor_exclusions = df['speciality'].str.contains(medical_advisor_exclusions, case=False, na=False, regex=True)

# Final mask: Select Medical Advisor
mask_medical_advisor_final = mask_medical_advisor & ~mask_medical_advisor_exclusions

# Store the original values that will be replaced
original_medical_advisor_values = df.loc[mask_medical_advisor_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_medical_advisor_final, 'speciality'] = 'Medical Advisor'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Medical Advisor", 'green'))
print(df.loc[mask_medical_advisor_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_medical_advisor_values = df.loc[mask_medical_advisor_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Medical Advisor", "cyan"))
for original_medical_advisor_value in original_medical_advisor_values:
    print(f"✅ {original_medical_advisor_value} → Medical Advisor")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Medical Advisor:", 'red'))
print(grouped_medical_advisor_values)

# Print summary
matched_count_medical_advisor = mask_medical_advisor_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Medical Advisor: "
        f"{matched_count_medical_advisor}",
        'red'))