import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Hospital Manager related titles

hospital_manager_variants = [
    r"\bHospital\s?Manager\b",

    # Common misspellings and case errors
    r"\bHosptial\s?Manager\b",
    r"\bHospital\s?Manger\b",
    r"\bHospitl\s?Manager\b",
    r"\bHospital\s?Mngr\b",
    r"\bOffice Assistant\b",

    # Spanish variants
    r"\bGerente\s?de\s?Hospital\b",
    r"\bAdministrador\s?de\s?Hospital\b",

    # Other possible variations
    r"\bHealthcare\s?Manager\b",
    r"\bHospital\s?Administrator\b",
    r"\bMedical\s?Facility\s?Manager\b",
    r"\bDirector\s?of\s?Hospital\s?Operations\b",
    r"\bPublic Hospital\b",
    r"\bAssistente Direzione Medica\b",
    r"\bDuty Manager\b",
    r"\bFacilities Manager\b",
    r"\bFacility Manager\b",
    r"\bRnOffice Manager\b",
    r"\bIcu\b",
    r"\bInventory Manager\b",
    r"\bMedical Coordination\b",
    r"\bService Manager\b",
    r"\bHospital Provincial De Pemba\b",
    r"\bService Manager\b",
    r"\bOperational Also Roustabouts\b",
    r"\bHealth Management\b",
    r"\bOperation Room Management\b",
    r"\bHead Of Hospital\b",
    r"\bHead Office\b",
    r"\bReceptionist\b",
    r"\bAnti Aging Center Manager\b",
    r"\bAssociate Chief Division Of Hospital Medicine\b",
    r"\bMedical Officer\b",
    r"\bCho\b",
    r"\bOffice ManagerPatient Coordinator\b",
    r"\bDirector of Aesthetic scheduling\b",
    r"\bFront Desk Patient Concierge\b",
]

# Exact matches that should be updated
hospital_manager_exact_matches = {
    "Hospital Manager",
    "Hosptial Manager",
    "Hospital Manger",
    "Hospitl Manager",
    "Hospital Mngr",
    # Spanish variants
    "Gerente de Hospital",
    "Administrador de Hospital",
    # Other possible variations
    "Healthcare Manager",
    "Hospital Administrator",
    "Medical Facility Manager",
    "Director of Hospital Operations",
    "Health Business/Administration",
    "Health BusinessAdministration",
    'Planner',
    'planner',
    'Coordinator',
    'coordinator',
    'Quality Officer',
    'Hospital Director',
    'Post-16 Manager',
    'Client Services Director',
    'Director Of Customer Experience',
    'Gerante Centre Esthetique',
    'DirectorRn',
    'Director Of Admissions',
    'Group Coordinator',
    'Fukai Ordho Office',
    'Centre Esthetique',
    'Manager Client Services',
    'Head Of Customer Service',
    'The Key To Generating New Patients',
    'Center Manager',
    'Quality Assurance',
    'General Coordinator',
    'Client Services Manager',
    'Director Of Client Services',
    'RnManager',
    'Hospitaldirector',
    'ID Manager',
    'Cho',
    'Patient Coordinator',
    'Front Desk Manager',
    'Client Services Coordinator',
    'Front Desk',
    'Quality Control Manager',
    'Office Coordinator',
    'Administrative Assistant General Surgery',
    'Administrative Coordinator General Surgery & Dermatology',
    'Chief Operating Officer Physicians Healthcare Collaborative',
    'Chief Physician Administrative Services Officer',
    'Chief Physician Executive',
    'Chief Physician Executive Officer Patient Experience',
    'Chief Physician Services Officer',
    'Epic Resolute Hospital Billing & Physician Billing Senior Analyst',
    'Physicians Coordinator',
    'Physicians Surgery Centers Llc',
}

# Define patterns (these should NOT be changed)
hospital_manager_exclusions = {
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
}

# Create a mask for Hospital Manager
mask_hospital_manager = df['speciality'].str.contains('|'.join(hospital_manager_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(hospital_manager_exact_matches)
mask_hospital_manager_exclusions = df['speciality'].isin(hospital_manager_exclusions)

# Final mask: Select Hospital Manager
mask_hospital_manager_final = mask_hospital_manager & ~mask_hospital_manager_exclusions

# Store the original values that will be replaced
original_hospital_manager_values = df.loc[mask_hospital_manager_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_hospital_manager_final, 'speciality'] = 'Hospital Manager'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Hospital Manager", 'green'))
print(df.loc[mask_hospital_manager_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_hospital_manager_values = df.loc[mask_hospital_manager_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Hospital Manager", "cyan"))
for original_hospital_manager_value in original_hospital_manager_values:
    print(f"✅ {original_hospital_manager_value} → Hospital Manager")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Hospital Manager:", 'red'))
print(grouped_hospital_manager_values)

# Print summary
matched_count_hospital_manager = mask_hospital_manager_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Hospital Manager: "
        f"{matched_count_hospital_manager}",
        'red'))