import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Clinical Staff related titles

clinical_staff_variants = [
    r"\bClinical\s?Staff\b",
    r"\bClinical\s?Team\b",
    r"\bClinical\s?Support\s?Staff\b",
    r"\bHealth\s?Care\s?Team\b",
    r"\bHealthcare\s?Provider\s?Staff\b",
    r"\bNursing\s?Staff\b",
    r"\bSupport\s?Staff\b",
    r"\bClinical\s?Healthcare\s?Staff\b",
    r"\bAnalistaassistente\b",
    r"\bAesthetic Facilitator\b",
    r"\bAesthetic Mediclinic\b",
    r"\bAesthetic Clinician\b",
    r"\bAesthetic Device\b",
    r"\bSeniorclinicalqualitycoordinator\b",
    r"\bClinical Resource Nurse\b",
    r"\bDirectrice Centre Laser\b",
    r"\bAesthetic & Laser\b",
    r"\bClinical Software Nurse\b",
    r"\bPhlebotomy\b",
    r"\bChief Clinical Offier\b",
    r"\bChief Clinical Information Officer\b",
    r"\bClinical Operation\b",
    r"\bCoordinador De Quirofano\b",
    r"\bPlastic Surgery Trauma Co-Ordinator\b",
    r"\bClinical Resource Nurse\b",
    r"\bLaser & Light Therapy Industry\b",
    r"\bMlso\b",
    r"\bSeniorclinicalqualitycoordinator\b",
    r"\bDirectrice Centre Laser\b",
    r"\bLab Technician\b",
    r"\bAesthetic & Laser\b",
    r"\bPhlebotomy\b",
    r"\bClinical Software Nurse\b",
    r"\bAesthetic Mediclinic\b",
    r"\bChief Clinical Offier\b",
    r"\bChief Clinical Information Officer\b",
    r"\bClinical Staff\b",
    r"\bLab Leader\b",
    r"\bClinical Operation\b",
    r"\bCoordinador De Quirofano\b",
    r"\bAnalistaassistente\b",
    r"\bAesthetic Clinician\b",
    r"\bMedical Lab Technologist\b",
    r"\bMedical Lab\b",
    r"\bLab Director\b",
    r"\bHealthcare Staff\b",
    r"\bLab Specialist\b",
    r"\bPlastic Surgery Trauma Co-Ordinator\b",
    r"\bMedical Lab Teachnaligi\b",
    r"\bLab Assistant In Government Hospital\b",
    r"\bAesthetic Facilitator\b",
    r"\bAesthetic Device\b",
    r"\bClinical Education\b",
    r"\bClinical Specialist\b",
    r"\bClincial Specialist\b",
    r"\bSenior Support Specialist\b",
    r"\bHealthcare Professional\b",
    r"\bHealthcare\s?Staff\b",
    r"\bLead Laser Technician\b",
    r"\bLaser Technician Lead\b",
    r"\bLazer Technician\b",
    r"\bAnesthesiologist Technician\b",
    r"\bX-Ray Technician\b",
    r"\bMedical Laboratory Technician\b",
    r"\bPharmacy Technician\b",
    r"\bMental Health Technician\b",
    r"\bCae  & Laser Technician\b",
    r"\bEndoscopy Technician\b",
    r"\bBiomedical Technician\b",
    r"\bHnd Pharmacy Technician\b",
    r"\bEpid  Insp  Technician\b",
]

# Exact matches that should be updated
clinical_staff_exact_matches = {
    'Clinical Staff',
    'Clinical Team',
    'Clinical Support Staff',
    'Health Care Team',
    'Healthcare Provider Staff',
    'Nursing Staff',
    'Support Staff',
    'Clinical Healthcare Staff',
    'Lab',
    'lab',
    'Lead',
    'lead',
    'Laser',
    'laser',

    # Common misspellings for Clinical Staff titles
    'Clincal Staff',
    'Clinicial Staff',
    'Clincial Team',
    'Clinical Teamm',
    'Clinical Support Staffs',

    # Case-related errors for Clinical Staff titles
    'CLINICAL STAFF',
    'clinical STAFF',
    'clinical staff',
    'CLINICAL Team',
    'Healthcare Team',
    'support STAFF',

    # Variants of Clinical Staff for different types in Spanish
    'Personal Clínico',
    'Personal Médico',
    'Equipo Clínico',
    'Equipo de Atención Médica',
    'Personal de Apoyo Clínico',
    'Personal de Salud',
    'Personal de Soporte',
    'Equipo de Proveedores de Atención Médica',
    'Personal de Enfermería',
    'Personal Clínico de Salud',

    # Other possible variations (Including Doctor forms, Specialist forms)
    'Medical Support Staff',
    'Clinical Care Staff',
    'Clinical Providers',
    'Medical Support Team',

    # other values from data sources
    'Mlso',
    'Lead',
    'Laser & Light Therapy Industry',
    'Laser',
    'laser',
    'Cco',
    'Ami Coordinator',
    'Director Of Operating Room',
    'Clinical Nurse Coordinator',
    'Surgical Technologist',
    'Coordinator Of New Life Plastic & Dermatology Plovdiv',
    'Healthcare Staff',
    'Healthcar Staff',
    'Healtcare Staff',
    'HealthCare Staff',
    'HEALTHCARE STAFF',
    'healthcare staff',
    'Healthcare Professional Staff',
    'Healthcare Professional',
    'Healthcare Services Staff',
    'Support Healthcare Staff',
    'Support Specialist',
    'Laser Technician',
    'Clincal Manager',
    'Surgical coordinator',
    'Scrub Tech',
    'Laser Tech',
    'Medical coordinator',
    'Patient Care Coordinator',
    'Patient care Coordinator',
    'Patient coordinator',
    'Woundcare Specialist',
    'Certified Chief Surgical Technician Bariatrics Colorectal General & Robotic Surgery',
    'Certified Dermatology Technician',
    'Dermatology Clinical Assistant',
    'Dermatology Technician',
    'General Surgery Clinical Coordinator',
    'General Surgery Inventory Coordinator',
    'Plastic & General Surgery Coordinator',
    'Residency Program General Surgery Coordinator',
    'Primary Coordinator',
    'Medical Coordinator',
    'Positions assistant',
    'Surgical Scrub Tech',
    'TECNICA',
    'Auxiliar en enfermeria',
    'C&D',
    'CMA',
    'CNA',
    'FSC',
    'FSE',
    'FSU',
    'Field Service Engineer',
}

# Define patterns for  & Resident & Professor (these should NOT be changed)
clinical_staff_exclusions = {
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
    'Physician Clinical Education Consultant',
}

# Create a mask for Clinical Staff
mask_clinical_staff = df['speciality'].str.contains('|'.join(clinical_staff_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(clinical_staff_exact_matches)
mask_clinical_staff_exclusions = df['speciality'].isin(clinical_staff_exclusions)

# Final mask: Select Clinical Staff
mask_clinical_staff_final = mask_clinical_staff & ~mask_clinical_staff_exclusions

# Store the original values that will be replaced
original_clinical_staff_values = df.loc[mask_clinical_staff_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_clinical_staff_final, 'speciality'] = 'Clinical Staff'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Clinical Staff", 'green'))
print(df.loc[mask_clinical_staff_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_clinical_staff_values = df.loc[mask_clinical_staff_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Clinical Staff", "cyan"))
for original_clinical_staff_value in original_clinical_staff_values:
    print(f"✅ {original_clinical_staff_value} → Clinical Staff")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Clinical Staff:", 'red'))
print(grouped_clinical_staff_values)

# Print summary
matched_count_clinical_staff = mask_clinical_staff_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Clinical Staff: "
        f"{matched_count_clinical_staff}",
        'red'))