import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for General Surgeon related titles

general_surgeon_variants = [
    r"\bGeneral\s?Surgeon\b",
    r"\bGeneral\s?Surgeon\s?Specialist\b",
    r"\bBoard\s?Certified\s?General\s?Surgeon\b",
    r"\bCertified\s?General\s?Surgeon\b",
    r"\bGeneral Surgery\b",

    # Spanish variants
    r"\bCirujano\s?General\b",
    r"\bCirujano\s?Generalista\b",
    r"\bCirujano\s?de\s?Atención\s?Primaria\b",

    # Other possible variations
    r"\bDoctor\s?General\s?Surgeon\b",
    r"\bDoctor\s?en\s?Cirugía\s?General\b",
    r"\bGeneral\s?Surgical\s?Specialist\b",
    r"\bGeneral\s?Surgical\s?Doctor\b",
    r"\bGeneral\s?Surgical\s?Physician\b",
    r"\bLicensed\s?General\s?Surgeon\b",
    r"\bTrauma Physician\b",
    r"\bConsultant Surgeon\b",
    r"\bGeneral Suegery\b",
    r"\bConsultant General Sugeon\b",
    r"\bGeneral & Aesthetic Surged\b",
    r"\bMedico Cirugiao Geral\b",
    r"\bChief Surgeon\b",
    r"\bChief Of Surgery\b",
    r"\bSurgical & Diagnostics\b",
    r"\bConsultanttraumasurgeon\b",
    r"\bOhner The Surgery\b",
    r"\bChirurgie Generale Et Senologique\b",
    r"\bChirurgie Main\b",
    r"\bCirujano General\b",
    r"\bGeneral Surgeon\b",
    r"\bConsultant General Sugeon\b",
    r"\bConsultant Surgeon\b",
    r"\bChief Surgeon\b",
    r"\bGeneral Surgery\b",
    r"\bSurgical & Diagnostics\b",
    r"\bChief Of Surgery\b",
    r"\bGeneral Surgeon Facial Surgery Breast Surgery\b",
    r"\bConsultanttraumasurgeon\b",
    r"\bOhner The Surgery\b",
    r"\bChirurgie Generale Et Senologique\b",
    r"\bGeneral & Aesthetic Surged\b",
    r"\bChirurgie Main\b",
    r"\bGeneral Surgeon Specialized In Abdominal Wall Reconstruction\b",
    r"\bTrauma Physician\b",
    r"\bMedico Cirugiao Geral\b",
    r"\bMedico Cirujano Y Partero\b",
    r"\bGeneral Surgery &Laser Applications\b",
    r"\bConsultant General Surgery\b",
    r"\bChirurgie Generale\b",
    r"\bGeneral Suegery\b",
    r"\bM S  General Surgery\b",
    r"\bCirurgia Geral\b",
    r"\bCirujano General Medico Esteticista\b",
    r"\bCirujano General\b",
    r"\bGeneral Surgery Bariatric Cosmetic\b",
    r"\bGeneral Surgery Specialist& Aestetic Medecin\b",
    r"\bConsultants General Surgery\b",
]

# Exact matches that should be updated
general_surgeon_exact_matches = {
    "General Surgeon",
    "General Surgeon Specialist",
    "Board Certified General Surgeon",
    "Certified General Surgeon",
    # Spanish form matches
    "Cirujano General",
    "Cirujano Generalista",
    "Cirujano de Atención Primaria",
    # Other possible variations
    "Doctor General Surgeon",
    "Doctor en Cirugía General",
    "General Surgical Specialist",
    "General Surgical Doctor",
    "General Surgical Physician",
    "Licensed General Surgeon",
    "Surgeon",
    "Surgery",
    'Chirurgie',
    'Cirurgia',
    'Chirurgie',
    'Cirurgia',
    'Cirujano',
    'Chirurgie Generale',
    'CirujanoMedico',
    'General Suegery',
    'Cirurgia Geral',
    'Surgeries',
    'Surgeon',
    "surgeon",
    "surgery",
    'chirurgie',
    'cirurgia',
    'chirurgie',
    'cirurgia',
    'cirujano',
    'chirurgie Generale',
    'cirujanoMedico',
    'general suegery',
    'cirurgia geral',
    'surgeries',
    'surgeon',
    'Medico Chirurgo',
    'medico chirurgo',
    'Khirurg',
    'khirurg',
    'Medico Cirujano',
    'medico cirujano',
    'Medico Chirurgo',
    'medico chirurgo',
    'Medico Cirujana',
    'medico cirujana',
    'CirujanoMedico',
    'cirujanomedico',
    'Medico Y Cirujano',
    'medico Y cirujano',
    'Consultant SurgeonClinical Director Im&T',
    'Director Of Surgery Center',
    'Proctologist',
    'Sirgeon',
    'Medico Especialista En Cirugia General Estetica',
    'Bariatric Surgeon',
    'Cirurgiao',
    'Physician Surgeonowner',
    'Surgeonowner',
    'MEDICO CIRUJANO',
    'Medico cirujano',
    'President Surgeon',
    'Surgical Specialist',
}

# Define patterns (these should NOT be changed)
general_surgeon_exclusions = {
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
    'Cirurgia Plastica',
    'Cirujano Plastico',
    'Administrative Coordinator General Surgery & Dermatology',
    'Program Manager General Surgery Residency Program',
    'Residency Program General Surgery Coordinator',
    'Site Manager - General Surgery',
    'Trauma & General Surgery App Supervisor',
    'General Surgery Research Resident',
    'Manager Marketing General Surgery & Gyn',
    'General Surgery Inventory Coordinator',
    'Nurse Practitioner - Acute Care General Surgery',
    'Nurse Practitioner General Surgery',
    'Practice Administrator General Surgery',
    'Program Director General Surgery Residency',
    'Group Manager Marketing General Surgery & Gyn',
    'Plastic & General Surgery Coordinator',
    'General Surgery Clinical Coordinator',
    'General Surgery Chief Resident',
    'Graduate Medical Education & General Surgery Program Coordinator',
    'Administrative Assistant General Surgery',
    'General Surgery Residency Interim Program Director',
    'Program Director General Surgery',
    'Physician Assistant - General Surgery',
    'Orthopedic & General Surgery Nurse Case Manager',
    'General Surgery Territory Sales Manager',
    'Surgical Coordinator Colorectal & General Surgery',
    'Client Developer & General Surgery',
    'Pediatric General Surgery Nurse Practitioner',
    'Medical Director Region General Surgery South',
    'Pgy- 2 General Surgery Resident',
}

# Create a mask for General Surgeon
mask_general_surgeon = df['speciality'].str.contains('|'.join(general_surgeon_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(general_surgeon_exact_matches)
mask_general_surgeon_exclusions = df['speciality'].isin(general_surgeon_exclusions)

# Final mask: Select General Surgeon
mask_general_surgeon_final = mask_general_surgeon & ~mask_general_surgeon_exclusions

# Store the original values that will be replaced
original_general_surgeon_values = df.loc[mask_general_surgeon_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_general_surgeon_final, 'speciality'] = 'General Surgeon'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: General Surgeon", 'green'))
print(df.loc[mask_general_surgeon_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_general_surgeon_values = df.loc[mask_general_surgeon_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: General Surgeon", "cyan"))
for original_general_surgeon_value in original_general_surgeon_values:
    print(f"✅ {original_general_surgeon_value} → General Surgeon")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with General Surgeon:", 'red'))
print(grouped_general_surgeon_values)

# Print summary
matched_count_general_surgeon = mask_general_surgeon_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to General Surgeon: "
        f"{matched_count_general_surgeon}",
        'red'))