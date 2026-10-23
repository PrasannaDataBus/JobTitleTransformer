import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Marketing Manager related titles

marketing_manager_variants = [
    # Standard Titles & Abbreviations
    r"\bMarketing\s?Manager\b",
    r"\bMarketing\s?Mng\b",
    r"\bMarketing\s?Mgr\b",
    r"\bMkt\s?Manager\b",
    r"\bMktg\s?Manager\b",
    r"\bMarketing\b",
    r"\bBrand Manager\b",
    r"\bCommercial Director\b",
    r"\bDesigner\b",
    r"\bCommercial Manager\b",
    r"\bChannel Manager\b",
    r"\bCosmetic PhysicianPodcast Host\b",
    r"\bEditorial Coordinator\b",
    r"\bP R  Medicina Estetica\b",
    r"\bP R\b",
    r"\bPR\b",
    r"\bPr & Social Media Coordinator\b",
    r"\bPR Specialist\b",
    r"\bSocial Media Pr Assistant\b",
    r"Social Media",
    r"\bHead Of Mr\b",
    r"\bPortfolio Sr  Manager\b",
    r"\bHead Of Communication\b",
    r"\bCommunication Manager\b",
    r"\bBrand Strategist\b",
    r"\bSeo Errors\b",
    r"\bBusiness Development Health Care\b",
    r"\bDigital Manager\b",
    r"\bAnalista De Mercadeo\b",
    r"\bPrint Strategist\b",
    r"\bAds\b",
    r"Business Development Manager",
    r"Content Strategist",
    r"Publicitaria",
    r"Business Development",
    r"\bPublicist\b",
    r"\bSeo\b",
    r"\bVideo Adds\b",
    r"\bMarket Mgr\b",
    r"\bMrktng Dir\b",
    r"\bStrategist\b",
    r"\bCorporate Communication\b",
    r"\bMedical Communication\b",
    r"\bMkt\b",
    r"\bLatest Innovations In Healthcare News Website\b",
    r"\bBdm\b",
    r"\bDev Web & Communication\b",
    r"\bBusiness Excellence Lead\b",
    r"\bVideos Add\b",
    r"\bEditorial\b",
    r"\bOnline\b",
    r"Facebook",
    r"Instagram",
    r"Digital Marketing",
    r"Marketing",
    r"Copywriter",
    r"\bCommunication\b",
    r"\bBusiness Developement\b",
    r"\bMktg Dir Botox\b",
    r"\bChargee De Communication\b",
    r"\bCommunication Agency\b",
    r"\bBody Contouring Product Marketing Manager\b",
    r"\bBusiness Growth\b",
    r"\bAssociate Media Director\b",
    r"\bBusiness Associate\b",
    r"\bMedia Supervisor\b",
    r"\bHvac Supervisor Or Telecom\b",
    r"\bSenior Media Supervisor\b",
    r"\bPrint Supervisor\b",
    r"\bMarketing & Communications Coordinator\b",
    r"\bSocial Media Coordinator\b",
    r"\bMedia Coordinator\b",
    r"\bMedia Planner\b",
    r"\bMedia Assistant\b",
    r"\bCommunications\b",
    r"\bVidep Editor\b",

    # Misspellings & Typographical Errors
    r"\bMarkting\s?Manager\b",
    r"\bMarketting\s?Manager\b",
    r"\bMarketing\s?Managr\b",
    r"\bMarkting\s?Managr\b",
    r"\bMarkeing\s?Manager\b",
    r"\bMarketing\s?Maneger\b",
    r"\bMarketing\s?Manger\b",
    r"\bMarket\s?Manager\b",

    # Case Variations
    r"\bmarketing manager\b",
    r"\bMarketing manager\b",
    r"\bmarketing Manager\b",
    r"\bMARKETING MANAGER\b",
    r"\bMarkEting ManageR\b",

    # Spanish Variants
    r"\bGerente\s?de\s?Marketing\b",
    r"\bGerente\s?de\s?Mercadeo\b",
    r"\bGerente\s?de\s?Publicidad\b",
    r"\bDirector\s?de\s?Marketing\b",
    r"\bDirector\s?de\s?Mercadotecnia\b",
    r"\bGerente\s?de\s?Comercialización\b",
    r"\bJefe\s?de\s?Marketing\b",
    r"\bJefe\s?de\s?Publicidad\b",
    r"\bGerente\s?de\s?Estrategia\s?de\s?Marketing\b",

    # Other Possible Variations
    r"\bMarketing\s?Head\b",
    r"\bMarketing\s?Lead\b",
    r"\bChief\s?Marketing\s?Officer\b",
    r"\bCMO\b",
    r"\bHead\s?of\s?Marketing\b",
    r"\bDigital\s?Marketing\s?Manager\b",
    r"\bBrand\s?Marketing\s?Manager\b",
    r"\bAdvertising\s?Manager\b",
    r"\bMarketing\s?and\s?Communications\s?Manager\b",
    r"\bStrategic\s?Marketing\s?Manager\b",
    r"\bProduct\s?Marketing\s?Manager\b",
    r"\bCorporate\s?Marketing\s?Manager\b",
    r"\bGrowth\s?Marketing\s?Manager\b",
    r"\bPerformance\s?Marketing\s?Manager\b",
    r"\bContent\s?Marketing\s?Manager\b",
    r"\bBrand Management\b",
    r"\bPracticeMarketing Manager\b",
    r"\bPractice ManagerMarketing\b",
    r"\bBusiness Development Director\b",
    r"\bBd\b",
    r"\bBusiness Developer\b",
    r"\bDirector Of Business Development\b",
    r"\bDesign\b",
    r"\bMktg\b",
    r"Marketer",
    r"Marketing",
    r"\bArt\b",
    r"\bPublisher\b",
    r"\bDeputy Editor\b",
    r"\bMarket Development\b",
    r"\bCommunication Evenementielle\b",
    r"\bPublication Planning\b",
    r"\bPr\b",
    r"\bBrand Manager\b",
    r"\bBusiness Develoment\b",
    r"\bMaketing Manager\b",
    r"\bMarekting Director\b",
    r"\bMrketing Director\b",
    r"\bAesthetic Marketplace Manager\b",
    r"\bCRM Manager\b",
]

# Exact matches that should be updated
marketing_manager_exact_matches = {
    "Marketing Manager",
    "Marketing Mgr",
    "Mkt Manager",
    "Mktg Manager",
    "Markting Manager",
    "Marketting Manager",
    "Marketing Managr",
    "Marketing Mngr",
    "Marketing Maneger",
    "Marketing Manger",
    "Market Manager",
    "Gerente de Marketing",
    "Gerente de Mercadeo",
    "Gerente de Publicidad",
    "Director de Marketing",
    "Director de Mercadotecnia",
    "Gerente de Comercialización",
    "Jefe de Marketing",
    "Jefe de Publicidad",
    "Gerente de Estrategia de Marketing",
    "Marketing Head",
    "Marketing Lead",
    "Chief Marketing Officer",
    "CMO",
    "Head of Marketing",
    "Digital Marketing Manager",
    "Brand Marketing Manager",
    "Advertising Manager",
    "Marketing and Communications Manager",
    "Strategic Marketing Manager",
    "Product Marketing Manager",
    "Corporate Marketing Manager",
    "Growth Marketing Manager",
    "Performance Marketing Manager",
    "Content Marketing Manager",
    "Marketing",
    "Markting",
    "Maketing",
    "Marekting",
    "Marrketing",
    "Markeitng",
    "Maketting",
    "Business Development Manager",
    "Marketing Director",
    "Dev",
    "dev",
    "Business Development",
    "PracticeMarketing Manager",
    "Practice ManagerMarketing",
    "Business Development Director",
    "Bd",
    "Director Of Business Development",
    'Design',
    'Graphiste',
    'Brand Specialist',
    'Facial Aesthetic Publications',
    'Publication Manager',
    'Topic Lead Websessions',
    'Creative Director',
    'Director Of Biz Dev',
    'Advertising Director',
    'Business Stretagy Executive',
    'Desiger',
    'Advertising',
    'Hd Of Bus Dvlpmnt & CommL Ops',
    'Brand Developer',
    'Dev Director',
    'Director of Development',
    'Client Relations',
    'Platform Manager',
    'Director of Business Strategies',
    'Director of Client Relations',
    'Global PRE',
    'Global PRE Director',
    'Loyalty Director',
    'V P Patient Acquisition',
    'Global Development Manager',
    'Regional Director Of Growth & Development',
    'A V',
    'AV',
    'Animator',
    'Creative Director Alle',
    'Creative Partner',
    'Creative director',
    'Digital Content Manager',
    'Dir Global Commerical Development',
    'Display Works',
    'EltaMD Brand Director',
}

# Define patterns (these should NOT be changed)
marketing_manager_exclusions = {
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

# Create a mask for Marketing Manager
mask_marketing_manager = df['speciality'].str.contains('|'.join(marketing_manager_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(marketing_manager_exact_matches)
mask_marketing_manager_exclusions = df['speciality'].isin(marketing_manager_exclusions)

# Final mask: Select Marketing Manager
mask_marketing_manager_final = mask_marketing_manager & ~mask_marketing_manager_exclusions

# Store the original values that will be replaced
original_marketing_manager_values = df.loc[mask_marketing_manager_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_marketing_manager_final, 'speciality'] = 'Marketing Manager'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Marketing Manager", 'green'))
print(df.loc[mask_marketing_manager_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_marketing_manager_values = df.loc[mask_marketing_manager_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Marketing Manager", "cyan"))
for original_marketing_manager_value in original_marketing_manager_values:
    print(f"✅ {original_marketing_manager_value} → Marketing Manager")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Marketing Manager:", 'red'))
print(grouped_marketing_manager_values)

# Print summary
matched_count_marketing_manager = mask_marketing_manager_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Marketing Manager: "
        f"{matched_count_marketing_manager}",
        'red'))