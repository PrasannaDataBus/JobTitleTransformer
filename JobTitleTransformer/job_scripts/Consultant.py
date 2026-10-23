import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Consultant related titles

consultant_variants = [
    r"\bSenior\s?Consultant\b",
    r"\bMedical\s?Consultant\b",
    r"\bBusiness\s?Consultant\b",
    r"\bCorporate\s?Consultant\b",
    r"\bProfessional\s?Consultant\b",
    r"\bSpecialist\s?Consultant\b",
    r"\bIndustry\s?Consultant\b",
    r"\bAesthetic ConsultantManager\b",
    r"\bCosmetic Business Consultancy\b",
    r"\bMedical Writing\b",
    r"\bConsultant Dermatology Oncology\b",
    r"\bCertified Uae Innovation Award Assessor\b",
    r"\bConsultant Otorhinolaryngology\b",
    r"\bHead Of Enterprise Architecture Office\b",
    r"\bRuralplanningField\b",
    r"\bMedical Scientific Consultant\b",
    r"\bConsultant Medical\b",
    r"\bStrategic Leadership Consulting & Account Services\b",
    r"\bBroker\b",
    r"\bPatient Consultant\b",
    r"\bPublic Health Specialist\b",
    r"\bMedical Information Specialist\b",
    r"\bMedical Writing\b",
    r"\bConsultant Specialist\b",
    r"\bCertified Uae Innovation Award Assessor\b",
    r"\bAesthetics Business Consultant\b",
    r"\bHead Of Enterprise Architecture Office\b",
    r"\bHealth Industry Consultant\b",
    r"\bHealthcare Information Services\b",
    r"\bAccount Specialist\b",
    r"\bMedical Scientific Consultant\b",
    r"\bMedical Consultant\b",
    r"\bEnvironmental Health Specialist\b",
    r"\bConsultora\b",
    r"\bSpecialist Financial Asviswr To Medics & Dentists\b",
    r"\bRuralplanningField\b",
    r"\bConsultant Medical\b",
    r"\bMedical DirectorInjectorHormone Specialist\b",
    r"\bStrategic Leadership Consulting & Account Services\b",
    r"\bBroker\b",
    r"\bPatient Consultant\b",
    r"\bSenior Consultant\b",
    r"\bBusiness Consultant\b",
    r"\bMedical Specialist\b",
    r"\bSr  Live Chat Specialist\b",
    r"\bAesthetic ConsultantManager\b",
    r"\bConsultant Medical Specialist\b",
    r"\bSpecialist Registrar\b",
    r"\bIndustry Consultant\b",
    r"\bLeading Specialist\b",
    r"\bAesthetic Medical Consultant\b",
    r"\bRegulatory & Npd Specialist\b",
    r"\bBd Specialist\b",
    r"\bRegulator Of Medical Devices\b",
    r"Claims Consultant",
]

# Exact matches that should be updated
consultant_exact_matches = {
    "Consultant",
    "Senior Consultant",
    "Medical Consultant",
    "Business Consultant",
    "Corporate Consultant",
    "Professional Consultant",
    "Specialist Consultant",
    "Industry Consultant",
    'Specialist',
    'Consulting',

    # Common misspellings for Consultant titles
    "Consulant",
    "Consultent",
    "Consultnt",
    "Consultat",
    "Conslutant",
    "Consulatnt",
    "Consutant",
    "Cosultant",

    # Case-related errors for Consultant
    "consultant",
    "CONSULTANT",
    "Consultant",
    "senior consultant",
    "Senior consultant",
    "medical consultant",
    "business consultant",
    "corporate consultant",

    # Variants of Consultant for different types in Spanish
    "Consultor",
    "Consultora",
    "Consultor Médico",
    "Consultor de Negocios",
    "Consultor Corporativo",
    "Consultor Profesional",
    "Consultor Especialista",

    # Other possible variations (Including related terms)
    "Adviser",
    "Advisor",
    "Senior Adviser",
    "Medical Adviser",
    "Corporate Adviser",
    "Professional Adviser",
    "Industry Adviser",
    "Specialist Adviser",
    
    # values from data sources
    'Specialist',
    'specialist',
    'Consultant Dermatology',
    'Healthcare Information Services',
    'Specialist',
    'Consultante',
    'Consaltant',
    'Aesthetic Consultant',
    'Cosmetic Consultant',
    'Aesthetic Retail Consultant',
    'C M E',
    'CLIFTONLARSONALLEN LLP',
    'Cosmetic Concierge',
    'Exosome Specialist BENEV Consultant',
    'Functional Medicine Consultant',
    'Aesthetic Technology Consultant',
    'General Vascular & Trauma Surgery Consultant Hayes Locums',
    'Claims Consultant - Physicians & Surgeons Mideast',
    'Client Developer - Pathology & Dermatology',
    'Physician Advocate',
    'Physician Human Resources Advocate',
    'Physician Informatics Senior Advocate',
    'Physician Liaison',
    'Physician Liaison Physician Outreach & Engagement',
    'Physician Liaison Soar',
    'Physician Network Liaison',
    'Senior Locums Consultant General Trauma & Vascular Surgery',
    'Senior Physician Liaison',
    'Sound Physicians Privileging Consultant',
    'Transplant Physician Liaison Senior',
    'Autonomous',
    'CAC',
}

# Define patterns (these should NOT be changed)
consultant_exclusions = {
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
    'Aesthetic Resident'
}

# Create a mask for Consultant
mask_consultant = df['speciality'].str.contains('|'.join(consultant_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(consultant_exact_matches)
mask_consultant_exclusions = df['speciality'].isin(consultant_exclusions)

# Final mask: Select Consultant
mask_consultant_final = mask_consultant & ~mask_consultant_exclusions

# Store the original values that will be replaced
original_consultant_values = df.loc[mask_consultant_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_consultant_final, 'speciality'] = 'Consultant'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Consultant", 'green'))
print(df.loc[mask_consultant_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_consultant_values = df.loc[mask_consultant_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Consultant", "cyan"))
for original_consultant_value in original_consultant_values:
    print(f"✅ {original_consultant_value} → Consultant")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Consultant:", 'red'))
print(grouped_consultant_values)

# Print summary
matched_count_consultant = mask_consultant_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Consultant: "
        f"{matched_count_consultant}",
        'red'))