import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Employee related titles

employee_variants = [
    r"\bemployee\b",
    r"\bemployees\b",
    r"\bworker\b",
    r"\bworkers\b",
    r"\bstaff\s?member\b",
    r"\bteam\s?member\b",
    r"\bsubordinate\b",
    r"\bemployee\s?worker\b",
    r"\bempleado\b",
    r"\bempleados\b",
    r"\btrabajador\b",
    r"\btrabajadores\b",
    r"\bmiembro\s?de\s?equipo\b",
    r"\bcolaborador\b",
    r"\bsubordinado\b",
    r"\basociado\b",
    # Misspellings
    r"\bemplyee\b",
    r"\bemploye\b",
    r"\bemployye\b",
    r"\beployee\b",
    r"\bempoyee\b",
    r"\bemloyee\b",
    r"\bemployee\s?worker\b",
    # Other Possible Variations
    r"\bfull\s?time\s?employee\b",
    r"\bpart\s?time\s?employee\b",
    r"\btemporary\s?employee\b",
    r"\bpermanent\s?employee\b",
    r"\bcontract\s?employee\b",
    r"\bvolunteer\b",
    r"\bstaff\s?member\b",
    r"\btemporary\s?worker\b",
    r"\bWorker\b",
    r"\bEmployee\b",
    r"\bTechnical Associate\b",
    r"\bSecretaire De Direction\b",
    r"\bDaily Worker\b",
    r"\bCompany Employee\b",
    r"\bAs Worker\b",
    r"\bGovt Employee\b",
    r"\bAssistant Worker\b",
    r"\bStaff Member\b",
    r"\bI Am A Social Worker\b",
    r"\bGeneral Worker\b",
    r"\bWorker At Shop\b",
    r"\bGalderma Employee\b",
    r"\bInjectables Employee\b",
    r"\bLaborConstruction Worker\b",
    r"\bAbbvie Worker\b",
    r"\bFarm Worker\b",
    r"\bSocial Worker\b",
    r"\bPrivate Company Employee\b",
    r"\bWorkers\b",
]

# Exact matches that should be updated
employee_exact_matches = {
    "Employee",
    "Employees",
    "Worker",
    "Workers",
    "Staff",
    "Team Member",
    "Personnel",
    "Team",
    "Associate",
    "Subordinate",
    "Empleado",
    "Empleados",
    "Trabajador",
    "Trabajadores",
    "Miembro de Equipo",
    "Personal",
    "Colaborador",
    "Subordinado",
    "Asociado",
    "Empllyee",
    "Employe",
    "Employye",
    "Eployee",
    "Empoyee",
    "Emloyee",
    "Employee Worker",
    "Full Time Employee",
    "Part Time Employee",
    "Temporary Employee",
    "Permanent Employee",
    "Contract Employee",
    "Intern",
    "Volunteer",
    "Staff Member",
    "Temporary Worker",
    "Patient/Other",
    'Associate',
    'associate',
    'Direction',
    'direction',
    'staff',
    'Staff',
    'Senior Clerk',
}

# Define patterns (these should NOT be changed)
employee_exclusions = {
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
    'Volunteer Professor Of Dermatology',
    'Volunteer Assistant Clinical Professor',
}

# Create a mask for Employee
mask_employee = df['speciality'].str.contains('|'.join(employee_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(employee_exact_matches)
mask_employee_exclusions = df['speciality'].isin(employee_exclusions)

# Final mask: Select Employee
mask_employee_final = mask_employee & ~mask_employee_exclusions

# Store the original values that will be replaced
original_employee_values = df.loc[mask_employee_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_employee_final, 'speciality'] = 'Employee'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Employee", 'green'))
print(df.loc[mask_employee_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_employee_values = df.loc[mask_employee_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Employee", "cyan"))
for original_employee_value in original_employee_values:
    print(f"✅ {original_employee_value} → Employee")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Employee:", 'red'))
print(grouped_employee_values)

# Print summary
matched_count_employee = mask_employee_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Employee: "
        f"{matched_count_employee}",
        'red'))