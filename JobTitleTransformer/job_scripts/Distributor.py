import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Distributor related titles

distributor_variants = [
    r"\bdistributor\b",
    r"\bdistributors\b",
    r"\bwholesaler\b",
    r"\bwholesale\s?distributor\b",
    r"\bsupplier\b",
    r"\bproduct\s?supplier\b",
    r"\bvendor\b",
    r"\bsales\s?representative\b",
    r"\bdistribuidor\b",
    r"\bdistribuidores\b",
    r"\bmayorista\b",
    r"\bsuministrador\b",
    r"\bvendedor\b",
    r"\brepresentante\s?de\s?ventas\b",
    # Misspellings
    r"\bdistrbutor\b",
    r"\bdisttributor\b",
    r"\bdistrbutors\b",
    r"\bdistbtr\b",
    r"\bdistrubutor\b",
    # Other Possible Variations
    r"\bdistribution\s?manager\b",
    r"\bdistribution\s?coordinator\b",
    r"\bsales\s?distributor\b",
    r"\bsupply\s?chain\s?distributor\b",
    r"\bdelivery\s?distributor\b",
    r"\bdealer\b",
    r"\bManufacturing\b",
    r"\bDistribucion Nuticosmetica\b",
    r"\bFrangrance & Cosmetic\b",
    r"\bFrangrance & Cosmetic\b",
    r"\bComerciante\b",
    r"\bDistributer\b",
    r"\bSourcing Agent\b",
    r"\bIndependent Rep\b",
    r"\bBiomaterials\b",
    r"\bComprador\b",
    r"\bDistributeur\b",
    r"\bDistributorHolistic Skin Expert\b",
    r"\bDistruteur\b",
    r"\bBiomedical Equipment\b",
]

# Exact matches that should be updated
distributor_exact_matches = {
    "Distributor",
    "Distributors",
    "Wholesaler",
    "Wholesale Distributor",
    "Supplier",
    "Product Supplier",
    "Vendor",
    "Sales Representative",
    "Distribuidor",
    "Distribuidores",
    "Mayorista",
    "Sumistrador",
    "Vendedor",
    "Representante de Ventas",
    "Distrbutor",
    "Disttributor",
    "Distbtr",
    "Distrubutor",
    "Distribution Manager",
    "Distribution Coordinator",
    "Sales Distributor",
    "Supply Chain Distributor",
    "Delivery Distributor",
    "Dealer",
    'Orthopedics Instruments',
    'Wholesale Trader Of Gluathione & Dermal Fillers',
    'Wholesale Accounts Director',
    'Equipment',
    'Aesthetic seller',
}

# Define patterns (these should NOT be changed)
distributor_exclusions = {
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

# Create a mask for Distributor
mask_distributor = df['speciality'].str.contains('|'.join(distributor_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(distributor_exact_matches)
mask_distributor_exclusions = df['speciality'].isin(distributor_exclusions)

# Final mask: Select Distributor
mask_distributor_final = mask_distributor & ~mask_distributor_exclusions

# Store the original values that will be replaced
original_distributor_values = df.loc[mask_distributor_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_distributor_final, 'speciality'] = 'Distributor'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Distributor", 'green'))
print(df.loc[mask_distributor_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_distributor_values = df.loc[mask_distributor_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Distributor", "cyan"))
for original_distributor_value in original_distributor_values:
    print(f"✅ {original_distributor_value} → Distributor")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Distributor:", 'red'))
print(grouped_distributor_values)

# Print summary
matched_count_distributor = mask_distributor_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Distributor: "
        f"{matched_count_distributor}",
        'red'))