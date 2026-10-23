import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Esthetician Cosmetician related titles

esthetician_variants = [
    r"\besthetician\b",
    r"\bcosmetician\b",
    r"\bestheticien\b",
    r"\bbeauty\s?therapist\b",
    r"\bcosmetic\s?esthetician\b",
    r"\blicensed\s?esthetician\b",
    r"\bcertified\s?esthetician\b",
    r"\bprofessional\s?esthetician\b",
    r"\bskin\s?care\s?specialist\b",
    r"\bcosmetic\s?specialist\b",
    r"\bskin\s?specialist\b",
    r"\bfacial\s?specialist\b",
    r"\bfacial\s?therapist\b",
    r"\bbeauty\s?specialist\b",
    r"\bbeauty\s?expert\b",
    r"\besthetician\s?MD\b",
    r"\bSkin Care\b",
    r"\bAesthetic Therapist\b",
    r"\bEstheticianMassage Therapist\b",
    r"\bDental Therapist\b",
    r"\bEsthetics\b",
    r"\bOther Cosmetic Beauty Specialty\b",
    r"\bOccupational Therapist\b",
    r"\bHair Removal\b",
    r"\bCosmetique\b",
    r"\bTherapist\b",
    r"\bBrows\b",
    r"\bCosmetologa Asesora\b",
    r"Aethetician",
    r"Aesthetician",
    r"Esthetician",
    r"Maquillista",
    r"\bKometyka\b",
    r"\bCertified Advanced EsthetcianAspiring Fnp\b",
    r"\bManicure Pedicure\b",
    r"\bEsthetic Beauty\b",
    r"\bSemi Permanent Makeup\b",
    r"\bSkintherapist & Podiatrist\b",
    r"\bCosmetic & Personal Care\b",
    r"\bFacialistBeautician\b",
    r"\bLash Master\b",
    r"\bNursBeautician\b",
    r"\bAltomaquiagem\b",
    r"\bPdo Threads\b",
    r"\bBeauticianPress\b",
    r"\bSkintherapist\b",
    r"\bHairSkin\b",
    r"\bAesthetic Laser Specialist\b",
    r"\bSkin & Laser Specialist\b",
    r"\bLazer & Skin Care Specialist\b",
    r"\bNurseSkin\b",
   r"\bParamedical Dermal\b",
   r"\bLaser Specialist\b",
   r"\bAesthetican\b",

    # Spanish variants
    r"\besteticista\b",  # Spanish form (esthetician)
    r"\besteticistas\b",  # Spanish plural form (esthetician)
    r"\bterapeuta\s?de\s?belleza\b",  # Spanish form (beauty therapist)
    r"\bestetista\s?profesional\b",  # Spanish form (professional esthetician)
    r"\bespecialista\s?en\s?cuidado\s?de\s?la\s?piel\b",  # Spanish form (skin care specialist)
    r"\besteticista\s?certificado\b",  # Spanish form (certified esthetician)

    # Other possible variations
    r"\bdoctor\s?in\s?esthetician\b",
    r"\bskin\s?care\s?doctor\b",
    r"\besthetician\s?expert\b",
    r"\bAesthetician\b",
    r"Aesthetician",
    r"\bAesthetician\b",
]

# Exact matches that should be updated
esthetician_exact_matches = {
    "Esthetician Cosmetician",
    "Certified Esthetician",
    "Beauty Therapist",
    "Skin Care Specialist",
    "Cosmetology Expert",
    "Facial Specialist",
    "Skincare",
    "Cosmetics",
    'Esthetics',
    'Esteticista',
    'Estheticienne',
    'Cosmetic Coordinator',
    'Hydro Facial',
    'Kosmetolog Massazhist',
    'Facial Massage',
    'Freelance Makeup Artist',
    'Internationally Certified Permananet Makeup Artist',
    'Esterica',
    'Waxing',
    'Micropigmentation',
    'Beauty Aesthetic',
    'Aestician',
    'Aesthetian',
    'Cosmetisc',
    'Aesthetian',
    'Facials',
    'Cosmetic NurseTrainer',
    'Aesthetcian',
    'Doctor Aestetician',
    'Facial consultant',
    'Cosmetic Lead',
}

# Define patterns (these should NOT be changed)
esthetician_exclusions = {
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
    'Cirujano General Medico Esteticista',
    'Esthetician Student',
    'Student Esthetician',
    'Aesthetician Student Nurse',
    'Medico CirujanoMedico Esteticista',
    'Skin Care Brand'
}

# Create a mask for Esthetician Cosmetician
mask_esthetician = df['speciality'].str.contains('|'.join(esthetician_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(esthetician_exact_matches)
mask_esthetician_exclusions = df['speciality'].isin(esthetician_exclusions)

# Final mask: Select Esthetician Cosmetician
mask_esthetician_final = mask_esthetician & ~mask_esthetician_exclusions

# Store the original values that will be replaced
original_esthetician_values = df.loc[mask_esthetician_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_esthetician_final, 'speciality'] = 'Esthetician Cosmetician'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Esthetician Cosmetician", 'green'))
print(df.loc[mask_esthetician_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_esthetician_values = df.loc[mask_esthetician_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Esthetician Cosmetician", "cyan"))
for original_esthetician_value in original_esthetician_values:
    print(f"✅ {original_esthetician_value} → Esthetician Cosmetician")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Esthetician Cosmetician:", 'red'))
print(grouped_esthetician_values)

# Print summary
matched_count_esthetician = mask_esthetician_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Esthetician Cosmetician: "
        f"{matched_count_esthetician}",
        'red'))