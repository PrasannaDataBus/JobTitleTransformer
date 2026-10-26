"""Execution order of the curated rule scripts, and the legacy ``run_pipeline`` entry point."""
import warnings

# Preprocessing first, then one script per taxonomy category, in a fixed order.
RULE_SCRIPTS = [
    "_encode_decode.py",
    "Acupuncturist.py",
    "ARNP.py",
    "AestheticAntiAgingPhy.py",
    "AestheticPlasticSurgeon.py",
    "AestheticPhysician.py",
    "AlternativeMedicinePhysician.py",
    "Anaesthesist.py",
    "Anatomist.py",
    "Andrologist.py",
    "AngiologistPhlebologist.py",
    "AntiagingPhysician.py",
    "BiologistBiochemist.py",
    "BiomedicalPhysician.py",
    "Cardiologist.py",
    "ClinicManager.py",
    "ClinicalStaff.py",
    "CompanyCEO.py",
    "CompanyManager.py",
    "CompanyMedicalStaff.py",
    "CompanyRepresentative.py",
    "Consultant.py",
    "CosmeticDermCosmeticSurgeon.py",
    "CosmetologistMD.py",
    "Cytologist.py",
    "DentalAssistant.py",
    "DentalSurgeon.py",
    "Dentist.py",
    "DermatologicSurgeon.py",
    "Dermatologist.py",
    "Distributor.py",
    "Employee.py",
    "Endocrinologist.py",
    "ENTPhysician.py",
    "Esthetician.py",
    "EventManager.py",
    "FacialPlasticSurgeon.py",
    "GeneralPhysician.py",
    "GeneralSurgeon.py",
    "Genetician.py",
    "Geriatrist.py",
    "GynecologistObstetrician.py",
    "HairTransplantSurgeon.py",
    "Headofdepartment.py",
    "Hematologist.py",
    "HospitalManager.py",
    "Immunologist.py",
    "Influencer.py",
    "InternalMedicine.py",
    "LaboratoryMedicine.py",
    "Lawyer.py",
    "LegalCounsel.py",
    "LPN.py",
    "MarketingManager.py",
    "MaxillofacialSurgeon.py",
    "MedicalAdvisor.py",
    "MedicalSpaManager.py",
    "NeonatologistNeurologist.py",
    "Neurophysiologist.py",
    "NonmedicalStaff.py",
    "NursePractitioner.py",
    "Nutritionist.py",
    "OculoplasticSurgeon.py",
    "Oncologist.py",
    "Ophthalmologist.py",
    "OralMaxillofacialSurgeon.py",
    "Orthodontist.py",
    "Orthopedist.py",
    "Owner.py",
    "Pathologist.py",
    "Pediatrician.py",
    "Pharmacist.py",
    "Pharmacologist.py",
    "Photographer.py",
    "PhysicianAssistant.py",
    "Physiotherapist.py",
    "PlasticReconstructiveSurgeon.py",
    "PlasticSurgeon.py",
    "PracticeManager.py",
    "Press.py",
    "ProductProjectManager.py",
    "ProfessorTeacher.py",
    "Psychiatrist.py",
    "Psychologist.py",
    "Psychotherapist.py",
    "Radiologist.py",
    "RN.py",
    "ResearchScientist.py",
    "Rheumatologist.py",
    "Sales.py",
    "SportsMedicinePhysician.py",
    "Stomatologist.py",
    "Student.py",
    "Trichologist.py",
    "Urologist.py",
    "VascularSurgeon.py",
]


def run_pipeline(df):
    """Legacy entry point, kept for backwards compatibility.

    Normalises the ``speciality`` column with the original interactive review of
    semantic matches, and returns the frame with ``speciality`` replaced by the
    normalised label. New code should use :func:`JobTitleTransformer.normalize`.
    """
    warnings.warn(
        "run_pipeline() is deprecated; use JobTitleTransformer.normalize(df, column=...) instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    from .api import normalize

    result = normalize(df, column="speciality", review="interactive", verbose=True)
    out = df.copy()
    out["original_speciality"] = df["speciality"]
    out["speciality"] = result["normalized_title"].where(result["normalized_title"].notna(), df["speciality"])
    out["match_method"] = result["match_method"]
    return out
