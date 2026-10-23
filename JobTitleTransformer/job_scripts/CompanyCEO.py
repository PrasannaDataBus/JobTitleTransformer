import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Company CEO related titles

company_ceo_variants = [
    r"\bCompany\s?CEO\b",
    r"\bChief\s?Executive\s?Officer\b",
    r"\bChief\s?Executive\s?Officer\s?of\s?Company\b",
    r"\bExecutive\s?Officer\b",
    r"\bCEO\s?of\s?Company\b",
    r"\bChief\s?Officer\b",
    r"\bCEO\s?of\s?the\s?Company\b",
    r"\bPresident\s?of\s?Company\b",
    r"\bChief\s?Officer\s?Company\b",
    r"\bHead\s?of\s?Company\b",
    r"\bceo\b",
    r"\bc.e.o\b",
    r"\b(c\.?e\.?o\.?)\b",
    r"\bfounder\b",
    r"\bcoo\b",
    r"\bgm\b",
    r"\bGM\b",
    r"\bGm\b",
    r"\bCfo\b",
    r"\bCFO\b",
    r"\bcfo\b",
    r"\bGeneral Director\b",
    r"\bSenior Vice President\b",
    r"\bPresidentCeo\b",
    r"\bCso\b",
    r"\bCeoManaging Director\b",
    r"\bceo\b",
    r"\bPresident\b",
    r"\bCto\b",
    r"\bSvp\b",
    r"\bBusinessman\b",
    r"\bDeputy General Manager\b",
    r"\bInvestor\b",
    r"\bGeneral Manager Mena\b",
    r"Chief Executive",
    r"\bFounder\b",
    r"\bChief Of The Board\b",
    r"\bPrsidente\b",
    r"\bFondatrice\b",
    r"\bGeneral Managerr\b",
    r"\bChief Financial Officer\b",
    r"\bDirektur\b",
    r"\bGeneral Managing\b",
    r"\bDirecteur General\b",
    r"\bGeneral Manager Uk&I - Ea\b",
    r"\bDirectrice\b",
    r"\bVp National & Strategic Accounts\b",
    r"\bGeneral Manager Uk&I\b",
    r"\bVp\b",
    r"\bCio\b",
    r"\bPresigent\b",
    r"\bVice Secretary Insdv Indonesia\b",
    r"\bAssistant General Manager\b",
    r"\bPresidente\b",
]

# Exact matches that should be updated
company_ceo_exact_matches = {
    'Company CEO',
    'Chief Executive Officer',
    'Chief Executive Officer of Company',
    'Executive Officer',
    'CEO of Company',
    'Chief Officer',
    'CEO of the Company',
    'President of Company',
    'Chief Officer Company',
    'Head of Company',
    'PresidentCeo',
    'G M',
    'GM',
    'Gm',
    'gm',
    'gM',

    # Common misspellings for Company CEO titles
    'Chief Executve Officer',
    'Compnay CEO',
    'Chif Executive Officer',
    'Chief Excutive Officer',
    'Ceo of Company',
    'Chief Excutive Offcer',
    'Comapny CEO',
    'Executive Offcer',
    'Executve Officer',
    'Chief Excutive Ocer',
    'CEO of Comapny',
    'Chief Excutive Ofcer',

    # Case-related errors for Company CEO titles
    'COMPANY CEO',
    'CHIEF EXECUTIVE OFFICER',
    'EXECUTIVE OFFICER',
    'CEO OF COMPANY',
    'CHIEF OFFICER',
    'CEO OF THE COMPANY',
    'PRESIDENT OF COMPANY',
    'CHIEF OFFICER COMPANY',
    'HEAD OF COMPANY',
    'chief executive officer',
    'executive officer',
    'company ceo',
    'Assistant Director',

    # Variants of Company CEO for different types in Spanish
    'CEO de la Compañía',
    'Director Ejecutivo',
    'Presidente de la Compañía',
    'Director General',
    'Director Ejecutivo de la Compañía',
    'Jefe de la Compañía',
    'Jefe Ejecutivo de la Compañía',
    'Presidente Ejecutivo',
    'Director General de la Compañía',
    'Director de la Compañía',

    # Other possible variations (Including Doctor forms, Specialist forms)
    'Managing Director',
    'Executive Director',
    'President of the Company',
    'Principal Executive Officer',
    'Corporate CEO',
    'Chief Operating Officer',
    'Company Head',
    'Corporate President',
    'President',
    "Presidnt",
    "Presdent",
    "Presdient",
    "Preisdent",
    "Presidentt",
    "Preident",
    "Preeident",
    "Presdnt",
    "Ptesident",
    'Vice President',
    'Vp',
    'VP',
    'vp',
    'Cso',
    'CSO',
    'cso',
    'CeoManaging Director',
    'CeoChairmanMd',
    'Business Director',
    'Deputy Director',
    'Regional Director',
    'Business Head',
    'Chairman',
    'CeoMd',
    'FounderCeo',
    'Chairman Sylhet District',
    'Cofounder',
    'Chairman Of Board',
    'Chairman Of The Board',
    'Member - Board Of Directors',
    'CeoPresident',
    'Chief Business Officer',
    'PresidentCeoOwner',
    'Vice Chairman',
    'Chief International Officer',
    'CeoFounder',
    'Dirigeant',
    'Chief Technology Officer',
    'Physician associateCEO',
    'PresidentFounder',
    'CVO',
    'Cvo',
    'cvo',
    'Chief Revenue Officer',
    'Chief Executive Officer & Premier Partners Dentist',
    'CBDO',
    'EVP',
}

# Define patterns for owner (these should NOT be changed)
company_ceo_exclusions = [
    r"\b(owner|co-owner|owner-manager|coowner|owner-|assistant)\b",
    r"\bAssistant\b",
    r"\bSurgeon\b",
    r"\bPhysician\b",
    r"\bRN\b",
    r"\bRn\b",
    r"\bRegistered Nurse\b",
    r"\bARNP\b",
    r"\bLPN\b",
    r"\bNP\b",
    r"\bAdvanced Registered Nurse Practitioner\b",
    r"\bNurse\b",
    r"\bMarketing\b",
    r"\bSales\b",
    r"\bDentist\b",
    r"\bDermatologist\b",
    r"\bCosmetologist\b",
]

# Join exclusion patterns into a single regex string
exclusions_pattern = '|'.join(company_ceo_exclusions)

# Create a mask for Company CEO
mask_company_ceo = df['speciality'].str.contains('|'.join(company_ceo_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(company_ceo_exact_matches)

# Apply exclusions using str.contains() instead of .isin()
mask_company_ceo_exclusions = df['speciality'].str.contains(exclusions_pattern, case=False, na=False, regex=True)

# Final mask: Select Company CEO
mask_company_ceo_final = mask_company_ceo & ~mask_company_ceo_exclusions

# Store the original values that will be replaced
original_company_ceo_values = df.loc[mask_company_ceo_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_company_ceo_final, 'speciality'] = 'Company CEO'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Company CEO", 'green'))
print(df.loc[mask_company_ceo_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_company_ceo_values = df.loc[mask_company_ceo_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Company CEO", "cyan"))
for original_company_ceo_value in original_company_ceo_values:
    print(f"✅ {original_company_ceo_value} → Company CEO")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Company CEO:", 'red'))
print(grouped_company_ceo_values)

# Print summary
matched_count_company_ceo = mask_company_ceo_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Company CEO: "
        f"{matched_count_company_ceo}",
        'red'))