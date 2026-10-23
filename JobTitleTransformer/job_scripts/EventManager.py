import pandas as pd
import re
import unicodedata
import sys
import os
from termcolor import colored

# Define regex patterns for Event Manager related titles

event_manager_variants = [
    r"\bevent\s?manager\b",
    r"\bevent\s?planner\b",
    r"\bevent\s?coordinator\b",
    r"\bevent\s?supervisor\b",
    r"\bevent\s?director\b",
    r"\bevent\s?organizer\b",
    r"\bevent\s?planning\s?manager\b",
    r"\bevent\s?production\s?manager\b",
    r"\bevent\s?operations\s?manager\b",
    r"\bevent\s?staff\s?manager\b",
    r"\bevent\s?marketing\s?manager\b",
    r"\bevent\s?project\s?manager\b",
    r"\bevent\s?management\s?specialist\b",
    r"\bevent\s?consultant\b",
    r"\bevent\s?strategist\b",
    r"\bevent\s?administrator\b",
    r"\bTrade Show\b",
    r"\bEvents Manager\b",
    r"Events",
    r"Tradeshow",
    r"Exhibition Manager",
    r"\bChef De Projet Congres\b",
    r"\bConfirm The Booth\b",
    r"Mice",
    r"Teamlead Congresses",
    r"Conference Producer",
    r"Booth Staff",
    r"Exhibitions",
    r"Exhibition",
    r"\bCongress Agency\b",
    r"\bCongress\b",
    r"\bExpo Man\b",
    r"\bOnsite Registration Support\b",
    r"\bSymposia&Congress Expert\b",
    r"\bConference\b",
    r"\bEvent Booking\b",
    r"\bHost\b",
    r"\bEvent Services Manager\b",
    r"\bExhibit Planning\b",
    r"\bEvent Assistant\b",
    r"\bEvent Planning\b",
    r"\bConvention Coordinator\b",
    r"\bConvention Manager\b",

    # Spanish variants
    r"\bgerente\s?de\s?eventos\b",  # Spanish form (event manager)
    r"\bplanificador\s?de\s?eventos\b",  # Spanish form (event planner)
    r"\bcoordinador\s?de\s?eventos\b",  # Spanish form (event coordinator)
    r"\borganizador\s?de\s?eventos\b",  # Spanish form (event organizer)
    r"\bdirector\s?de\s?eventos\b",  # Spanish form (event director)
    r"\bresponsable\s?de\s?eventos\b",  # Spanish form (event supervisor)
    r"\bplanificador\s?de\s?eventos\s?certificado\b",  # Spanish form (certified event planner)
    r"\bcoordinador\s?de\s?eventos\s?profesional\b",  # Spanish form (professional event coordinator)
    r"\bcoordinador\s?de\s?eventos\s?certificado\b",  # Spanish form (certified event coordinator)

    # Other possible variations
    r"\bmanager\s?of\s?events\b",
    r"\bplanner\s?of\s?events\b",
    r"\bcoordinator\s?of\s?events\b",
    r"\bevent\s?project\s?coordinator\b",
    r"\bevent\s?program\s?manager\b",
    r"\bcelebration\s?planner\b",
    r"\bconference\s?organizer\b",
    r"\bfestival\s?organizer\b",
    r"\bmeeting\s?planner\b",
    r"\bparty\s?planner\b",
    r"\bconference\s?manager\b",
    r"\bconvention\s?planner\b",
    r"\bcorporate\s?event\s?manager\b",
]

# Exact matches that should be updated
event_manager_exact_matches = {
    "Event Manager",
    "Event Planner",
    "Event Coordinator",
    "Event Supervisor",
    "Event Director",
    "Event Organizer",
    "Event Planning Manager",
    "Event Production Manager",
    "Event Operations Manager",
    "Event Staff Manager",
    "Event Marketing Manager",
    "Event Project Manager",
    "Event Management Specialist",
    "Event Consultant",
    "Event Strategist",
    "Event Administrator",
    # Spanish form matches
    "Gerente de Eventos",
    "Planificador de Eventos",
    "Coordinador de Eventos",
    "Organizador de Eventos",
    "Director de Eventos",
    "Responsable de Eventos",
    "Planificador de Eventos Certificado",
    "Coordinador de Eventos Profesional",
    "Coordinador de Eventos Certificado",
    'Attendee Manager',
    'Meeting Producer',
    'Show Coordinator',
    'Booth Operator',
    'Director of Conferences Logistics',
}

# Define patterns (these should NOT be changed)
event_manager_exclusions = {
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

# Create a mask for Event Manager
mask_event_manager = df['speciality'].str.contains('|'.join(event_manager_variants), case = False,
                                                          na = False, regex = True) | \
                            df['speciality'].isin(event_manager_exact_matches)
mask_event_manager_exclusions = df['speciality'].isin(event_manager_exclusions)

# Final mask: Select Event Manager
mask_event_manager_final = mask_event_manager & ~mask_event_manager_exclusions

# Store the original values that will be replaced
original_event_manager_values = df.loc[mask_event_manager_final, 'speciality'].unique()

# Update the speciality column based on exact matches
df.loc[mask_event_manager_final, 'speciality'] = 'Event Manager'

# Check AFTER updating
print(colored("\nUnique values AFTER updating: Event Manager", 'green'))
print(df.loc[mask_event_manager_final, 'speciality'].unique())

# GroupBy to count how many records were replaced by the new value
grouped_event_manager_values = df.loc[mask_event_manager_final, 'speciality'].value_counts()

# Print the exact replacements
print(colored("\nReplaced Values: Event Manager", "cyan"))
for original_event_manager_value in original_event_manager_values:
    print(f"✅ {original_event_manager_value} → Event Manager")

# GroupBy after replacement (to show the new value)
print(colored("\nGroupBy counts AFTER replacing with Event Manager:", 'red'))
print(grouped_event_manager_values)

# Print summary
matched_count_event_manager = mask_event_manager_final.sum()

# Print results
print(
    colored(
        f"\nTotal values matched and changed (Stage 1) to Event Manager: "
        f"{matched_count_event_manager}",
        'red'))