import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Product Project Manager related titles

project_manager_variants = [
    # Standard Titles & Variants
    r"\bProduct Project Manager\b",
    r"\bProduct & Project Manager\b",
    r"\bProduct-Project Manager\b",
    r"\bProduct / Project Manager\b",
    r"\bProductProject Manager\b",
    r"\bProduct Manager\b",
    r"\bProject Manager\b",
    r"\bExport Manager\b",
    r"\bProject Engineer\b",
    r"\bProducts\b",
    r"\bProduct Specialist\b",
    r"\bHead Of Projects\b",
    r"\bProdact Manager\b",
    r"\bPurchases Manager\b",
    r"\bDirecteur Des Projets Strategiques\b",
    r"\bJr Pdrocut Manager\b",
    r"\bChargee De Projets\b",
    r"Projects",
    r"Projets",
    r"Product",
    r"Project",
    r"\bProject Executive\b",
    r"\bChargee De Developpement Produit\b",
    r"Produit",
    r"Porject",
    r"\bPorject Support Manager\b",
    r"\bProjektmanager\b",
    r"Projekt",
    r"\bCharge De Programmes\b",
    r"\bCreator Of Brand Navi Natural Magic\b",
    r"\bProduct Manager Botox\b",

    # Misspellings & Typographical Errors
    r"\bProduct Proyect Manager\b",
    r"\bProduct Projet Manager\b",
    r"\bProduct Porject Manager\b",
    r"\bProduct Projct Manager\b",
    r"\bProduct Proyect Maneger\b",
    r"\bProduct Projject Managger\b",
    r"\bProduct Pojrect Manager\b",
    r"\bProduct Proyect Lead\b",

    # Case Variations
    r"\bPRODUCT PROJECT MANAGER\b",
    r"\bproduct project manager\b",
    r"\bProDuct PRoject ManAger\b",
    r"\bprOduCt pRojeCT manaGER\b",

    # Spanish Variants
    r"\bGerente de Proyecto de Producto\b",
    r"\bGestor de Proyectos de Producto\b",
    r"\bAdministrador de Proyectos de Producto\b",
    r"\bResponsable de Proyecto y Producto\b",
    r"\bCoordinador de Producto y Proyecto\b",
    r"\bLíder de Proyecto y Producto\b",

    # Hybrid Spanish-English Variants
    r"\bProduct Proyect Gerente\b",
    r"\bProduct Project Coordinador\b",
    r"\bProducto y Proyecto Manager\b",
    r"\bProduct y Project Manager\b",
    r"\bProyect Manager\b",

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bSenior Product Project Manager\b",
    r"\bLead Product Project Manager\b",
    r"\bHead of Product and Project Management\b",
    r"\bChief Product & Project Officer\b",
    r"\bGlobal Product Project Manager\b",
    r"\bProduct & Project Director\b",
    r"\bProduct/Project Coordinator\b",
    r"\bProduct Project Supervisor\b",
    r"\bProject Director\b",
    r"\bProject Coordinator\b",
    r"\bIfbprodact Development Officer\b",
    r"\bIfbprodact Development Officer\b",
]

# Exact matches that should be updated
project_manager_exact_matches = {
    "Product Project Manager",
    "Product & Project Manager",
    "Product-Project Manager",
    "Product / Project Manager",
    "ProductProject Manager",
    "Product Manager",
    "Project Manager",
    "Product Proyect Manager",
    "Product Projet Manager",
    "Product Porject Manager",
    "Product Projct Manager",
    "Product Proyect Maneger",
    "Product Projject Managger",
    "Product Pojrect Manager",
    "Product Proyect Lead",
    "Gerente de Proyecto de Producto",
    "Gestor de Proyectos de Producto",
    "Administrador de Proyectos de Producto",
    "Responsable de Proyecto y Producto",
    "Coordinador de Producto y Proyecto",
    "Líder de Proyecto y Producto",
    "Product Proyect Gerente",
    "Product Project Coordinador",
    "Producto y Proyecto Manager",
    "Product y Project Manager",
    "Senior Product Project Manager",
    "Lead Product Project Manager",
    "Head of Product and Project Management",
    "Chief Product & Project Officer",
    "Global Product Project Manager",
    "Product & Project Director",
    "Product/Project Coordinator",
    "Product Project Supervisor",
    "Product Specialist",
    "Project Director",
    'Service Development',
}

# # Define patterns (these should NOT be changed)
# project_manager_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

project_manager_exclusions = {
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

# Create a mask for Product Project Manager
mask_project_manager = df['speciality'].str.contains('|'.join(project_manager_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(project_manager_exact_matches)

# mask_project_manager_exclusions = df['speciality'].str.contains(project_manager_exclusions, case=False, na=False, regex=True)
mask_project_manager_exclusions = df['speciality'].isin(project_manager_exclusions)

# Final mask: Select Product Project Manager
mask_project_manager_final = mask_project_manager & ~mask_project_manager_exclusions

# Store the original values that will be replaced
original_project_manager_values = df.loc[mask_project_manager_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_project_manager_final, 'speciality'] = 'Product Project Manager'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Product Project Manager", 'green'))
print(df.loc[mask_project_manager_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_project_manager_values = df.loc[mask_project_manager_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Product Project Manager", "cyan"))
for original_project_manager_value in original_project_manager_values:
    print(f"✅ {original_project_manager_value} → Product Project Manager")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Product Project Manager:", 'red'))
print(grouped_project_manager_values)

# Print summary
matched_count_project_manager = mask_project_manager_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Product Project Manager: "
        f"{matched_count_project_manager}",
        'red'))