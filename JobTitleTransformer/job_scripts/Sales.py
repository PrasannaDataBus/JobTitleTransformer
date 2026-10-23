import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Sales related titles

sales_variants = [
    # Standard Titles & Variants
    r"\bSales\b",
    r"\bSales Representative\b",
    r"\bSales Manager\b",
    r"\bSales Director\b",
    r"\bSales Specialist\b",
    r"\bSales Executive\b",
    r"\bAccount Manager\b",
    r"\bBusiness Development Representative\b",
    r"\bSales Associate\b",
    r"\bAccount Executive\b",
    r"\bOperations Manager\b",
    r"\bRsm\b",
    r"\bAesthetic Accounting\b",
    r"\bSalesEvent Coordinator\b",
    r"Sales",
    r"Visitadora Medica",
    r"Sale Manager",
    r"Financial Manager",
    r"\bDemand Generation Manager\b",
    r"\bDirecteur Commercial\b",
    r"\bResponsavel Comercial\b",
    r"\bAccount Exec\b",
    r"\bCommercial\b",
    r"\bResponsable\b",
    r"\bSale\b",
    r"\bMgr Sr Dev - Botox Cosmetic Us Facial Aes Sales\b",
    r"\bE-Commerce\b",
    r"\bSalesClient\b",
    r"\bCommerciale\b",
    r"\bAccount Executive\b",

    # Misspellings & Typographical Errors
    r"\bSlaes\b",
    r"\bSals\b",
    r"\bSlaesman\b",
    r"\bSalesman\b",
    r"\bSalses\b",

    # Case Variations
    r"\bSALES\b",
    r"\bsales\b",
    r"\bSaLeS\b",
    r"\bSALESMAN\b",

    # Spanish Variants
    r"\bVentas\b",
    r"\bRepresentante de Ventas\b",
    r"\bGerente de Ventas\b",
    r"\bDirector de Ventas\b",
    r"\bEspecialista en Ventas\b",
    r"\bEjecutivo de Ventas\b",
    r"\bAsociado de Ventas\b",
    r"\bDesarrollo de Negocios en Ventas\b",
    r"\bRepresentante de Ventas\b",

    # Hybrid Spanish-English Variants
    r"\bSales Representante\b",
    r"\bSales Gerente de Ventas\b",
    r"\bSales Ejecutivo\b",
    r"\bBusiness Development Ventas\b",

    # Other Possible Variations (Doctor Forms, Specialist Forms)
    r"\bAccount Sales Manager\b",
    r"\bClient Relations Specialist\b",
    r"\bBusiness Development Sales\b",
    r"\bSales Lead Specialist\b",
    r"\bRegional Sales Manager\b",
    r"\bBilling Contact\b",
    r"\bAccountant\b",
    r"\bCOMMERICIAL ASSISTANT\b",
    r"Sales",
]

# Exact matches that should be updated
sales_exact_matches = {
    "Sales",
    "Sales Representative",
    "Sales Manager",
    "Sales Director",
    "Sales Specialist",
    "Sales Executive",
    "Account Manager",
    "Business Development Representative",
    "Sales Associate",
    "Slaes",
    "Sals",
    "Slaesman",
    "Salesman",
    "Salses",
    "SALES",
    "sales",
    "SaLeS",
    "SALESMAN",
    "Ventas",
    "Representante de Ventas",
    "Gerente de Ventas",
    "Director de Ventas",
    "Especialista en Ventas",
    "Ejecutivo de Ventas",
    "Asociado de Ventas",
    "Desarrollo de Negocios en Ventas",
    "Sales Representante",
    "Sales Gerente de Ventas",
    "Sales Ejecutivo",
    "Business Development Ventas",
    "Account Sales Manager",
    "Client Relations Specialist",
    "Business Development Sales",
    "Sales Lead Specialist",
    "Regional Sales Manager",
    "Specialized StoreConcept Store",
    'Account Coordinator',
    'Finance',
    'Account Director',
    'Group Account Director',
    'Commercialdirector',
    'Franchise Manager',
    'Comercial',
    'Dir Comercial',
    'National Accounts Director',
    'Teleshopping',
    'Ready-To-Wear Fashion Store',
    'Travel Retail Duty Free',
    'Account Directpr',
    'AE',
}

# # Define patterns (these should NOT be changed)
# sales_exclusions = r'\b(?:Plastic)|(?:Physician)\b'

sales_exclusions = {
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

# Create a mask for Sales
mask_sales = df['speciality'].str.contains('|'.join(sales_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(sales_exact_matches)

# mask_sales_exclusions = df['speciality'].str.contains(sales_exclusions, case=False, na=False, regex=True)
mask_sales_exclusions = df['speciality'].isin(sales_exclusions)

# Final mask: Select Sales
mask_sales_final = mask_sales & ~mask_sales_exclusions

# Store the original values that will be replaced
original_sales_values = df.loc[mask_sales_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_sales_final, 'speciality'] = 'Sales'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Sales", 'green'))
print(df.loc[mask_sales_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_sales_values = df.loc[mask_sales_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Sales", "cyan"))
for original_sales_value in original_sales_values:
    print(f"✅ {original_sales_value} → Sales")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Sales:", 'red'))
print(grouped_sales_values)

# Print summary
matched_count_sales = mask_sales_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Sales: "
        f"{matched_count_sales}",
        'red'))