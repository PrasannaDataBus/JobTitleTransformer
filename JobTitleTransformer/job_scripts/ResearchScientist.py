import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Research Scientist related titles

research_scientist_variants = [
    # Standard Titles & Variants
    r"\bResearch Scientist\b",
    r"\bScientific Researcher\b",
    r"\bScientist\b",
    r"\bPrincipal Investigator\b",
    r"\bLaboratory Scientist\b",
    r"\bScientific Researcher (Research Scientist)\b",
    r"\bResearch Associate\b",
    r"\bPostdoctoral Researcher\b",
    r"\bBiomedical Research Scientist\b",
    r"\bR&D\b",
    r"\bAnalyst\b",
    r"\bResearcher\b",
    r"\bRa\b",
    r"\bOrganism\b",
    r"\bPrecision Medicine\b",
    r"\bScientific Writer\b",
    r"\bEvidence Generation\b",
    r"\bDirecteur Scientifique\b",
    r"\bScientific Manager\b",
    r"\bChief Scientific Officer\b",
    r"\bInnovation Et Valorisation Scientifique\b",
    r"\bBioinformatics\b",
    r"\bScientifique\b",
    r"\bEnvironmental Health\b",

    # Misspellings & Typographical Errors
    r"\bReseach Scientist\b",
    r"\bResearch Scienist\b",
    r"\bReserch Scientist\b",
    r"\bResarch Scientist\b",
    r"\bReseach Sientist\b",

    # Case Variations
    r"\bRESEARCH SCIENTIST\b",
    r"\bResearch SCIENTIST\b",
    r"\bresearch scientist\b",
    r"\bRESEARCH scientist\b",

    # Spanish Variants
    r"\bCientífico Investigador\b",
    r"\bInvestigador Científico\b",
    r"\bCientífico de Investigación\b",
    r"\bInvestigador\b",
    r"\bInvestigador Postdoctoral\b",
    r"\bInvestigador Principal\b",
    r"\bCientífico Biomédico\b",
    r"\bCientífico de Laboratorio\b",

    # Hybrid Spanish-English Variants
    r"\bResearch Científico\b",
    r"\bResearcher Científico\b",

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bBiomedical Researcher\b",
    r"\bLaboratory Researcher\b",
    r"\bResearch Specialist\b",
    r"\bSenior Research Scientist\b",
    r"\bResearch Director\b",
    r"\bPrincipal Investigator (Research Scientist)\b",
    r"\bScientific Lead\b",
    r"\bClinical Research Scientist\b",
    r"\bResearch Coordinator\b",
    r"\bResearch\b",
    r"\bScoentist\b",
    r"\bVeterinary Science\b",
]

# Exact matches that should be updated
research_scientist_exact_matches = {
    "Research Scientist",
    "Scientific Researcher",
    "Scientist",
    "Principal Investigator",
    "Laboratory Scientist",
    "Scientific Researcher (Research Scientist)",
    "Research Associate",
    "Postdoctoral Researcher",
    "Biomedical Research Scientist",
    "Reseach Scientist",
    "Research Scienist",
    "Reserch Scientist",
    "Resarch Scientist",
    "Reseach Sientist",
    "Científico Investigador",
    "Investigador Científico",
    "Científico de Investigación",
    "Investigador",
    "Investigador Postdoctoral",
    "Investigador Principal",
    "Científico Biomédico",
    "Científico de Laboratorio",
    "Research Científico",
    "Researcher Científico",
    "Biomedical Researcher",
    "Laboratory Researcher",
    "Research Specialist",
    "Senior Research Scientist",
    "Research Director",
    "Principal Investigator (Research Scientist)",
    "Scientific Lead",
    "Clinical Research Scientist",
    "Research Coordinator",
    "Research",
    'Chief Science Officer',
    'Doctorat En Sciences De La Vie Et De La Sante - Specialisation Vieillissement Et Glycations',
    'Diretora De Pesquisa E Desenvolvimento',
    'Principal Medical Writer',
    'Exosome Specialist',
}

# # Define patterns (these should NOT be changed)
# research_scientist_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

research_scientist_exclusions = {
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
    'General Surgery Research Resident',
    'Epic Resolute Hospital Billing & Physician Billing Senior Analyst',
}

# Create a mask for Research Scientist
mask_research_scientist = df['speciality'].str.contains('|'.join(research_scientist_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(research_scientist_exact_matches)

# mask_research_scientist_exclusions = df['speciality'].str.contains(research_scientist_exclusions, case=False, na=False, regex=True)
mask_research_scientist_exclusions = df['speciality'].isin(research_scientist_exclusions)

# Final mask: Select Research Scientist
mask_research_scientist_final = mask_research_scientist & ~mask_research_scientist_exclusions

# Store the original values that will be replaced
original_research_scientist_values = df.loc[mask_research_scientist_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_research_scientist_final, 'speciality'] = 'Research Scientist'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Research Scientist", 'green'))
print(df.loc[mask_research_scientist_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_research_scientist_values = df.loc[mask_research_scientist_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Research Scientist", "cyan"))
for original_research_scientist_value in original_research_scientist_values:
    print(f"✅ {original_research_scientist_value} → Research Scientist")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Research Scientist:", 'red'))
print(grouped_research_scientist_values)

# Print summary
matched_count_research_scientist = mask_research_scientist_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Research Scientist: "
        f"{matched_count_research_scientist}",
        'red'))