import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Owner related titles

owner_variants = [
    # Standard Titles & Variants
    r"\bOwner\b",
    r"\bBusiness\s?Owner\b",
    r"\bCompany\s?Owner\b",
    r"\bFounder\b",
    r"\bCo\s?-?\s?Owner\b",
    r"\bEntrepreneur\b",
    r"\bSole\s?Proprietor\b",
    r"\bManaging\s?Owner\b",
    r"\bPrincipal\s?Owner\b",
    r"\bOwner\s?and\s?CEO\b",
    r"\bOwner\s?and\s?Founder\b",
    r"\bOwner\s?Operator\b",
    r"\bSelf\s?-?\s?Employed\b",
    r"\bIndependent\s?Business\s?Owner\b",
    r"\bManaging Partner\b",
    r"\bProprietor\b",
    r"\bPartners\b",
    r"\bMedico Proprietario\b",
    r"Proprietario",
    r"\bOwnerGeneral Manager\b",
    r"\bEntrepreneure Independante\b",
    r"\bOwners\b",
    r"\bBusiness Woman\b",
    r"\bOwnerBarbara JS Chocolates\b",
    r"\bPropietariaEnfermera Cosmetologa\b",
    r"\bOwnerbuyer\b",
    r"\bOwnere\b",
    r"\bOwnerCrnp\b",
    r"\bInjectorOwner\b",
    r"\bDirectorOwner\b",
    r"\bOwnerPhysician Associate\b",

    # Misspellings & Typographical Errors
    r"\bOner\b",
    r"\bOnwer\b",
    r"\bOwneer\b",
    r"\bOwnr\b",
    r"\bOwwner\b",
    r"\bOwnwer\b",

    # Case Variations
    r"\bowner\b",
    r"\bOwNeR\b",
    r"\bOWNER\b",
    r"\bOwNer\b",

    # Spanish Variants
    r"\bPropietario\b",
    r"\bDueño\b",
    r"\bTitular\b",
    r"\bFundador\b",
    r"\bEmprendedor\b",
    r"\bAutónomo\b",
    r"\bGerente\s?Propietario\b",
    r"\bDueño\s?de\s?Negocio\b",
    r"\bPropietario\s?de\s?Empresa\b",

    # Other Possible Variations
    r"\bBusiness\s?Founder\b",
    r"\bBusiness\s?Partner\b",
    r"\bBusiness\s?Owner\s?Operator\b",
    r"\bCompany\s?Director\b",
    r"\bEnterprise\s?Owner\b",
    r"\bStart-up\s?Founder\b",
    r"\bAesthetic Provider\b",
    r"\bBoss\b",
]

# Exact matches that should be updated
owner_exact_matches = {
    "Owner",
    "Business Owner",
    "Company Owner",
    "Founder",
    "Co-Owner",
    "Entrepreneur",
    "Sole Proprietor",
    "Managing Owner",
    "Principal Owner",
    "Owner and CEO",
    "Owner and Founder",
    "Owner Operator",
    "Self-Employed",
    "Independent Business Owner",
    "Oner",
    "Onwer",
    "Owneer",
    "Ownr",
    "Owwner",
    "Ownwer",
    "Propietario",
    "Dueño",
    "Titular",
    "Fundador",
    "Emprendedor",
    "Autónomo",
    "Gerente Propietario",
    "Dueño de Negocio",
    "Propietario de Empresa",
    "Business Founder",
    "Business Partner",
    "Business Owner Operator",
    "Company Director",
    "Enterprise Owner",
    "Start-up Founder",
    "Partner",
    'OwnerDirector',
    'CeoOwner',
    'OwnerCeoPresidentManaging Director',
    'OwnerExecutive Consultant',
    'OwnerLead Injector',
    'OwnerManaging Director',
    'OwnerNurse Injector',
    'Ownerhospital Director',
    'OwnerFounder',
    'Senior Partner',
    'Partner Innovation&Development',
    'PartnerOwner',
    'OwnerPresidentCeo',
    'SocioPropietarioEmpresario',
    'Bisnesman',
    'Inventor',
    'PodiatristOwner',
    'MDOWNER',
    'Ownerpractitioner',
    'RNOwner',
    'RNowner',
    'Nurse PractitionerOwner',
    'ARNPOwner',
    'SOCIA PROPRIETARIA',
}

# # Define patterns (these should NOT be changed)
# owner_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

owner_exclusions = {
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
    'Physician & Owner',
    'Oral & Facial Surgeon & & Owner',
    'Physician & Founder',
    'Plastic Surgeon Owner',
    'Physician Co-Owner',
    'Owner Physician',
    'Owner & Physician',
    'Periodontist & Dental Implant Surgeon & Owner',
    'Physician & Founder Interventional Cardiology',
    'Family Practice Physician Owner',
    'Physician-Owner',
    'Owner Plastic Surgeon',
    'Physician Founder',
    'Physician Medical Director & Owner',
    'Plastic Surgeon & Owner',
    'Plastic Surgeon & Co-Founder',
    'Physician Owner',
    'Physician & Co-Founder',
}

# Create a mask for Owner
mask_owner = df['speciality'].str.contains('|'.join(owner_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(owner_exact_matches)

# mask_owner_exclusions = df['speciality'].str.contains(owner_exclusions, case=False, na=False, regex=True)
mask_owner_exclusions = df['speciality'].isin(owner_exclusions)

# Final mask: Select Owner
mask_owner_final = mask_owner & ~mask_owner_exclusions

# Store the original values that will be replaced
original_owner_values = df.loc[mask_owner_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_owner_final, 'speciality'] = 'Owner'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Owner", 'green'))
print(df.loc[mask_owner_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_owner_values = df.loc[mask_owner_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Owner", "cyan"))
for original_owner_value in original_owner_values:
    print(f"✅ {original_owner_value} → Owner")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Owner:", 'red'))
print(grouped_owner_values)

# Print summary
matched_count_owner = mask_owner_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Owner: "
        f"{matched_count_owner}",
        'red'))