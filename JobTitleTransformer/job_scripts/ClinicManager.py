import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Clinic Manager related titles

clinic_manager_variants = [
    r"\bClinic\s?Manager\b",
    r"\bClinic\s?Administrator\b",
    r"\bHealthcare\s?Manager\b",
    r"\bMedical\s?Office\s?Manager\b",
    r"\bClinic\s?Supervisor\b",
    r"\bHealthcare\s?Administrator\b",
    r"\bNurse Manager\b",
    r"\bAestheticianClinic Manager\b",
    r"\bCentro Medico Azuaje\b",
    r"\bMedica Clinica Medica\b",
    r"\bTransportation Before & After Aesthetic Chirurgical Intervention\b",
    r"\bChief Of Staff\b",
    r"\bClinical Receptionist\b",
    r"\bOffice Mgr\b",
    r"\bClinical Support Services Manager\b",
    r"\bClinica Geral\b",
    r"\bClinico Geral\b",
    r"\bRnbn Clinic Director Plastic Surgery Centre\b",
    r"\bClinic Manager\b",
    r"\bClinic Administrator\b",
    r"\bClinicHospital\b",
    r"\bDental Clinic\b",
    r"\bAestetic Clinic Partner\b",
    r"\bRejenerative Clinic\b",
    r"\bOffice Manager\b",
    r"\bMedica Clinico Geral\b",
    r"\bClinical Receptionist\b",
    r"\bCeo Elite Helse Clinic\b",
    r"\bChief Of Staff\b",
    r"\bClinic CoordinatorBesuty Therapist\b",
    r"\bThe Pretty Young Clinic Seoul Korea\b",
    r"\bOffice Mgr\b",
    r"\bClinic Assistant\b",
    r"\bClinical Support Services Manager\b",
    r"\bClinica Geral\b",
    r"\bClinic Nurse\b",
    r"\bAesthetic Clinic Director\b",
    r"\bClinico Geral\b",
    r"\bClinic ManagerAnti-Aging Spacialist\b",
    r"\bAesthetic & Cosmetic Clinic\b",
    r"\bCentro Medico Azuaje\b",
    r"\bCeo Full Face Clinic\b",
    r"\bClinic Management\b",
    r"\bTransportation Before & After Aesthetic Chirurgical Intervention\b",
    r"\bClinic DirectorPlastic SurgeryRnbn\b",
    r"\bMedical Clinic Aesthetic Practice\b",
    r"\bRnbn Clinic Director Plastic Surgery Centre\b",
    r"\bClinic Management Ownership & Administration\b",
    r"\bDirector Cutaneous Imaging Clinic\b",
    r"\bCeo Of A Dermaesthetic Clinic\b",
    r"\bPain Rehabilitation Clinic\b",
    r"\bMedica Clinica Medica\b",
    r"\bNurse Manager\b",
    r"\bCeo Of Medical Clinic\b",
    r"\bClinic Director\b",
    r"\bHappy Aging Clinic Ceo\b",
    r"\bAesthetician & Clinic Assistant\b",
    r"\bCeo Of Aesthetic Clinic\b",
    r"\bClinical Nurse Manager\b",
    r"\bBeauty Clinic Ceo\b",
    r"\bDirector Of Ginza Tarumi Clinic\b",
    r"\bClinical Nurse Manager Emergency Department\b",
    r"\bHead Of The Clinic\b",
    r"\bMedica Clinica Geral\b",
    r"\bStem Cell Clinic\b",
    r"\bNurse Manager Rn\b",
    r"\bMember - Board Of Trustees Chief Of Staff - Umh Hospitals\b",
    r"\bAestheticianClinic Manager\b",
    r"\bClinic Manager Laser & Cosmetic Treatments\b",
    r"\bAesthetic Clinic Manager\b",
    r"\bHead Of Clinic\b",
    r"\bClinical Nurse Manager Of Behavioral Health Outpatient Services\b",
    r"\bClinic Manager Esthetician Not Using Injectables\b",
    r"\bClinical Nurse Manager Nicu Uh Rainbow Babies & ChildrenS\b",
    r"\bClinic ManagerAesthetican\b",
    r"\bClinic Director Of Cares Clinic\b",
    r"\bWellness Clinic\b",
    r"\bCoo Of A Clinic For Plastic Surgery\b",
    r"\bClinical Operations\b",
    r"\bClinical Governance\b",
    r"\bManager For Dr  Aziz\b",
]

# Exact matches that should be updated
clinic_manager_exact_matches = {
    'Clinic Manager',
    'Clinic Administrator',
    'Healthcare Manager',
    'Medical Office Manager',
    'Clinic Supervisor',
    'Healthcare Administrator',
    'Clinic',

    # Case-related errors
    'clinic manager',
    'clinic administrator',
    'healthcare manager',
    'medical office manager',
    'medical practice manager',
    'clinic supervisor',
    'healthcare administrator',
    'CLINIC MANAGER',
    'CLINIC ADMINISTRATOR',
    'HEALTHCARE MANAGER',
    'MEDICAL OFFICE MANAGER',
    'CLINIC SUPERVISOR',
    'HEALTHCARE ADMINISTRATOR',

    # Common misspellings
    'Clinic Maneger',
    'Clinic Mangager',
    'Clinc Manager',
    'Clinc Maneger',
    'Clinic Mananger',
    'Medial Office Manager',
    'Medicl Office Manager',
    'Medical Office Manger',

    # Spanish-related exclusions
    'Gerente de Clínica',
    'Administrador de Clínica',
    'Gerente de Atención Médica',
    'Gerente de Oficina Médica',
    'Supervisor de Clínica',
    'Administrador de Atención Sanitaria',
    
    # value from data sources
    'Clinic/Hospital',
    'Office Manager',
    'ClinicHospital',
    'Booking Manager',
    'Clinical Manager',
    'Clinic Hospital',
    'Private Clinic Hospital',
    'Other Clinic Hospital',
    'Clinic Operations Director',
    'Clinical Administrator',
    'Lead Patient Coordinator',
    'Treatment Coordinator',
    'Front Desk- Advanced Dermatology',
    'Medical Biller Dermatology',
    'Director of clinic operations',
    'Aesthetics Coordinator',
    'Aesthetics Manager',
    'Aesthetic Manager',
    'Cosmetic Manager',
    'COSMETIC MANAGER',
    'Cosmetic manage',
    'ARC',
    'Adm A',
    'Aesthetic Experience Manager',
    'Aesthetic Supervisor',
    'CHEF DE CLINIQUE',
    'CMM',
    'Consultation Co-ordinator',
    'Cosmetic Supervisor',
    'Director of WOO',
    'Executive Patient Concierge',
}

# Define patterns for  & Resident & Professor (these should NOT be changed)
clinic_manager_exclusions = {
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

# Create a mask for Clinic Manager
mask_clinic_manager = df['speciality'].str.contains('|'.join(clinic_manager_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(clinic_manager_exact_matches)
mask_clinic_manager_exclusions = df['speciality'].isin(clinic_manager_exclusions)

# Final mask: Select Clinic Manager
mask_clinic_manager_final = mask_clinic_manager & ~mask_clinic_manager_exclusions

# Store the original values that will be replaced
original_clinic_manager_values = df.loc[mask_clinic_manager_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_clinic_manager_final, 'speciality'] = 'Clinic Manager'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Clinic Manager", 'green'))
print(df.loc[mask_clinic_manager_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_clinic_manager_values = df.loc[mask_clinic_manager_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Clinic Manager", "cyan"))
for original_clinic_manager_value in original_clinic_manager_values:
    print(f"✅ {original_clinic_manager_value} → Clinic Manager")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Clinic Manager:", 'red'))
print(grouped_clinic_manager_values)

# Print summary
matched_count_clinic_manager = mask_clinic_manager_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Clinic Manager: "
        f"{matched_count_clinic_manager}",
        'red'))