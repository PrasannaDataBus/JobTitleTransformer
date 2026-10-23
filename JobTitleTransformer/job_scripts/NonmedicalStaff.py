import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored


# Define regex patterns for Non medical Staff related titles

non_medical_staff_variants = [
    # Standard Titles & Abbreviations
    r"\bNon\s?Medical\s?Staff\b",
    r"\bNon\s?Med\s?Staff\b",
    r"\bNon\s?Healthcare\s?Staff\b",
    r"\bNon\s?Clinical\s?Staff\b",
    r"\bNon\s?Medical\s?Personnel\b",
    r"\bAdministrative\s?Staff\b",
    r"\bHospital\s?Administrative\s?Staff\b",
    r"\bMedical\s?Office\s?Staff\b",
    r"\bHealthcare\s?Support\s?Staff\b",
    r"\bExecutive Assistant\b",
    r"\bMedico Nao Socio\b",
    r"\bHotel Chain\b",
    r"\bDecorator\b",
    r"\bAnalyst\b",
    r"\bData\b",
    r"\bAdministrative Assistant\b",
    r"\bRecruitment Lead\b",
    r"\bTalent Acquisition Manager\b",
    r"Talent Acquisition",
    r"\bOffice Job\b",
    r"\bMedical Technologist\b",
    r"\bSecretaire De Direction\b",
    r"\bInterpreter\b",
    r"\bOffice Staff\b",
    r"\bAmministratore Delegato\b",
    r"\bOffice ManagerBookkeeper\b",
    r"\bSafety Officer\b",
    r"\bKitchen Assistance\b",
    r"\bTecnology\b",
    r"\bAdmin Assist\b",
    r"\bOffice Work\b",
    r"\bProgrammer\b",
    r"\bAdministrative Manager\b",
    r"\bNon Specialist\b",
    r"\bTechnical Department Spare Part Assistant\b",
    r"\bWorldS First Ai Writing Assistant\b",

    # Misspellings & Typographical Errors
    r"\bNon\s?Medial\s?Staff\b",
    r"\bNone\s?Medical\s?Staff\b",
    r"\bNon\s?Medicl\s?Staff\b",
    r"\bNon\s?Medicall\s?Staff\b",
    r"\bNon\s?Medicia\s?Staff\b",
    r"\bNon\s?Mdical\s?Staff\b",
    r"\bNon\s?Meducal\s?Staff\b",
    r"\bNonn\s?Medical\s?Staff\b",
    r"\bNon\s?Medikal\s?Staff\b",
    r"\bNon\s?Meddical\s?Staff\b",

    # Case Variations
    r"\bnon medical staff\b",
    r"\bNon Medical staff\b",
    r"\bnon Medical Staff\b",
    r"\bNON MEDICAL STAFF\b",
    r"\bNonMed Staff\b",

    # Spanish Variants
    r"\bPersonal\s?No\s?Médico\b",
    r"\bEmpleado\s?No\s?Médico\b",
    r"\bTrabajador\s?No\s?Médico\b",
    r"\bStaff\s?No\s?Clínico\b",
    r"\bPersonal\s?Administrativo\s?de\s?Salud\b",

    # Other Possible Variations (Including Doctor/Specialist Forms)
    r"\bNon\s?Medical\s?Assistant\b",
    r"\bMedical\s?Receptionist\b",
    r"\bMedical\s?Secretary\b",
    r"\bHospital\s?Clerk\b",
    r"\bHealthcare\s?Administrative\s?Staff\b",
    r"\bMedical\s?Support\s?Staff\b",
    r"\bIt\b",
    r"\bSecretary\b",
    r"\bAssistant Cook\b",
    r"\bElectricien\b",
    r"\bIngeniero De Sistemas\b",
    r"\bSoftware Engineer\b",
    r"\bAdministrative Officer\b",
    r"\bAdministration\b",
    r"\bControl Officer\b",
    r"\bEngineering\b",
    r"\bEnegineer\b",
    r"\bElectricien\b",
    r"\bTalent Acquisition Manager\b",
    r"\bAnalyst\b",
    r"\bSenior Business Operation Analyst\b",
    r"\bExecutive Assistant\b",
    r"\bData\b",
    r"\bBiomedical Engineer\b",
    r"\bElectrical Engineer\b",
    r"\bAircraft Engineer\b",
    r"\bMedico Nao Socio\b",
    r"\bIngeniero De Sistemas\b",
    r"\bAdministration\b",
    r"\bAdministrative Assistant\b",
    r"\bAdmin\b",
    r"\bAdministrative Officer\b",
    r"\bMedical Technologist\b",
    r"\bOffice Job\b",
    r"\bIt Specialist\b",
    r"\bChemical Engineering\b",
    r"\bData Entry\b",
    r"\bEngineering\b",
    r"\bInformation Technologies It\b",
    r"\bRisk Analyst\b",
    r"\bIt\b",
    r"\bIt Manager\b",
    r"\bKitchen Assistance\b",
    r"\bOffice Staff\b",
    r"\bExecutive Assistant At Skillmed\b",
    r"\bDirector Of It\b",
    r"\bIt Services Manager\b",
    r"\bDecorator\b",
    r"\bInterpreter\b",
    r"\bControl Officer\b",
    r"\bData Entiry\b",
    r"\bIt Director\b",
    r"\bApplication Support Analyst\b",
    r"\bTecnology\b",
    r"\bJapanese Interpreter\b",
    r"\bAmministratore Delegato\b",
    r"\bCredit Control Business Analyst\b",
    r"\bSenior Business Analyst\b",
    r"\bMedical Engineer\b",
    r"\bOffice ManagerBookkeeper\b",
    r"\bSafety Officer\b",
    r"\bAvionics Technician\b",
    r"\bSecretary-General Of The Expert Group\b",
    r"\bData Interi\b",
    r"\bResearch Analyst\b",
    r"\bSecretary Of Society\b",
    r"\bAdmin Assist\b",
    r"\bOffice Work\b",
    r"\bProgrammer\b",
    r"\bAdministrative Manager\b",
    r"\bSecretary Ips\b",
    r"\bBiomedical Enegineer\b",
    r"\bCustomer Service Engineer\b",
    r"\bSystem Analyst\b",
    r"\bRecruitment Lead\b",
    r"\bHotel Chain\b",
    r"\bData Services Executive\b",
    r"\bDeputy Director Of It\b",
    r"\bData Analyst\b",
    r"\bNon Specialist\b",
    r"\bField Application Engineer\b",
    r"\bGraduate In Administration\b",
    r"\bPortfolio Analyst\b",
    r"\bTissue Engineering\b",
    r"\bR&D Engineer\b",
    r"\bYes ItS Free - Bookmark It Now\b",
    r"\bCivil Engineer\b",
    r"\bHead Of It Services\b",
    r"\bWife Secretary\b",
    r"\bApplication Analyst\b",
    r"\bSr  R&D Engineer\b",
    r"\bIt Systems Manager\b",
    r"\bSecurity Analyst\b",
    r"\bData Entry Operator\b",
    r"\bMecatronics & Biomedical Engineering\b",
    r"\bBiiomedical Analyst\b",
    r"\bAdministration & Finance Director\b",
    r"\bPersonal Secretary\b",
    r"\bStudying Business Administration & Management\b",
    r"\bSite Engineer\b",
    r"\bHead Of It\b",
    r"\bIt Consultant\b",
    r"\bOffice Administrative Assistant\b",
    r"\bEnvironmental Safety Officer\b",
    r"\bPaediatrician Analyst Public Health Agency Sweden\b",
    r"\bAssistant Cook\b",
    r"\bData Curator\b",
    r"\bBusiness Administration\b",
    r"\bDirector Engineering Department\b",
    r"\bHealth Engineering Student\b",
    r"\bR&D Quality Engineer\b",
    r"\bElectrical Engineering\b",
    r"\bComputer Engineering\b",
    r"\bBeauty Market Analyst\b",
    r"\bAv Technician\b",
    r"\bData Entry Adds Watching Computer Master\b",
    r"\bIt Helpdesk\b",
    r"\bField Technician\b",
    r"\bMedical Interpreter\b",
    r"\bMedical Administrative Assistant\b",
    r"\bSenior Information Analyst\b",
    r"\bSenior Research Analyst\b",
    r"\bEstimation Engineer\b",
    r"\bApp Analyst\b",
    r"\bBiomedical Engineering\b",
    r"\bPatent Engineer\b",
    r"\bSenior Field Service Engineer\b",
    r"\bClinical Quality & Patient Safety Officer\b",
    r"\bFinancial Analyst\b",
    r"\bInvestment Analyst\b",
    r"\bBusiness Analyst\b",
    r"\bProfessor Of Electrical Engineering Dept\b",
    r"\bDigital Analyst\b",
    r"\bSupercharge Your Writing Skills With Ai - Try It Free Today\b",
    r"\bAc Technician\b",
    r"\bLaunch Your Very Own Ai App Just Like Chatgpt & Charge People For It\b",
    r"\bAssistant Director Of It & Cfh\b",
    r"\bPackaging & Device Engineer\b",
    r"\bTesting Commissioning Engineer\b",
    r"\bData EntryWork Assignment\b",
]

# Exact matches that should be updated
non_medical_staff_exact_matches = {
    'Non-medical Staff',
    "Non Medical Staff",
    "Non Med Staff",
    "Non Healthcare Staff",
    "Non Clinical Staff",
    "Non Medical Personnel",
    "Administrative Staff",
    "Hospital Administrative Staff",
    "Medical Office Staff",
    "Healthcare Support Staff",
    "Non Medial Staff",
    "None Medical Staff",
    "Non Medicl Staff",
    "Non Medicall Staff",
    "Non Medicia Staff",
    "Non Mdical Staff",
    "Non Meducal Staff",
    "Nonn Medical Staff",
    "Non Medikal Staff",
    "Non Meddical Staff",
    "Personal No Médico",
    "Empleado No Médico",
    "Trabajador No Médico",
    "Staff No Clínico",
    "Personal Administrativo de Salud",
    "Non Medical Assistant",
    "Medical Receptionist",
    "Medical Secretary",
    "Hospital Clerk",
    "Healthcare Administrative Staff",
    "Medical Support Staff",
    "Administrative Employee",
    "Staff",
    "Admin",
    "Administrator",
    'ADMINISTRATOR',
    'Engineer',
    'It',
    'Online Work',
    'Engineer',
    'engineer',
    'Secretary',
    'secretary',
    'Facial Aesthetics Administrative Support',
    'Manager Facial Aesthetics Administrative Support',
    'Non-Medical Staff',
    'Graphic Installer',
    'Stand Builder',
    'Technician',
    'technician',
    'Guest',
    'guest',
    'Escort for attendee',
}

# # Define patterns (these should NOT be changed)
# non_medical_staff_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

non_medical_staff_exclusions = {
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
    'Sales Technician',
    'Sales Administrator',
    'Administrative coordinator',
    'Executive Assistant To Cao & Physician Liaison',
    'Executive Administrative Assistant To The Chief Executive Officer & Dental Manager',
    'Epic Resolute Hospital Billing & Physician Billing Senior Analyst',
    'Physician & Professional Clinic Talent Acquisition Specialist',
    'Dental Administrative Assistant',
    'Administrative Assistant Dental Department',
    'Executive Assistant Dermatology',
    'Physicians Administration',
    'Division Senior Sales Manager Administration L Oreal Dermatological Beauty',
    'Executive Assistant To Chief Commercial Officer Dental & Specialty Markets',
    'Administrative Assistant General Surgery',
}

# Create a mask for Non medical Staff
mask_non_medical_staff = df['speciality'].str.contains('|'.join(non_medical_staff_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(non_medical_staff_exact_matches)

# mask_non_medical_staff_exclusions = df['speciality'].str.contains(non_medical_staff_exclusions, case=False, na=False, regex=True)
mask_non_medical_staff_exclusions = df['speciality'].isin(non_medical_staff_exclusions)

# Final mask: Select Non medical Staff
mask_non_medical_staff_final = mask_non_medical_staff & ~mask_non_medical_staff_exclusions

# Store the original values that will be replaced
original_non_medical_staff_values = df.loc[mask_non_medical_staff_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_non_medical_staff_final, 'speciality'] = 'Non medical Staff'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Non medical Staff", 'green'))
print(df.loc[mask_non_medical_staff_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_non_medical_staff_values = df.loc[mask_non_medical_staff_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Non medical Staff", "cyan"))
for original_non_medical_staff_value in original_non_medical_staff_values:
    print(f"✅ {original_non_medical_staff_value} → Non medical Staff")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Non medical Staff:", 'red'))
print(grouped_non_medical_staff_values)

# Print summary
matched_count_non_medical_staff = mask_non_medical_staff_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Non medical Staff: "
        f"{matched_count_non_medical_staff}",
        'red'))