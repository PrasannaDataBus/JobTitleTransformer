"""Transformation Hub: the semantic fallback, human review and integrity gates.

Titles that no rule script recognises are matched to the closest label of the
standard taxonomy:

1. The taxonomy labels are embedded with Sentence-BERT (``all-MiniLM-L6-v2``)
   and stored in a FAISS ``IndexFlatL2`` index (exact L2 search).
2. Unmatched titles are embedded in batches and assigned their nearest label.
3. The matches can be reviewed by a person before they are accepted.
4. Integrity gates guarantee that every input row is returned.

The model and index are loaded on first use and cached.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List, Sequence, Tuple

import pandas as pd

DEFAULT_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 30

# Standard taxonomy: every normalised title is one of these labels.
TAXONOMY_LABELS = (
    'Acupuncturist',
    'Advanced Registered Nurse Practitioner (ARNP)',
    'Aesthetic & Anti-aging Physician',
    'Aesthetic & Plastic Surgeon',
    'Aesthetic Physician',
    'Alternative Medicine Physician',
    'Anaesthesist',
    'Anatomist',
    'Andrologist',
    'Angiologist Phlebologist',
    'Anti-aging Physician',
    'Biologist Biochemist',
    'Biomedical Physician',
    'Cardiologist',
    'Clinic Manager',
    'Clinical Staff',
    'Company CEO',
    'Company Manager',
    'Company Medical Staff',
    'Company Representative',
    'Consultant',
    'Cosmetic Dermatologist',
    'Cosmetic Surgeon',
    'Cosmetologist MD',
    'Cytologist',
    'Dental Assistant',
    'Dental Surgeon',
    'Dentist',
    'Dermatologic Surgeon',
    'Dermatologist',
    'Distributor',
    'Employee',
    'Endocrinologist',
    'ENT Ear Nose Throat Physician',
    'Esthetician Cosmetician',
    'Event Manager',
    'Facial Plastic Surgeon',
    'General Physician',
    'General Surgeon',
    'Genetician',
    'Geriatrist',
    'Gynecologist Obstetrician',
    'Hair Transplant Surgeon',
    'Head of department',
    'Hematologist',
    'Hospital Manager',
    'Immunologist',
    'Influencer',
    'Internal Medicine',
    'Laboratory Medicine',
    'Lawyer',
    'Legal Counsel',
    'Licensed Practical Nurse (LPN)',
    'Marketing Manager',
    'Maxillofacial Surgeon',
    'Medical Advisor',
    'Medical Spa Manager',
    'Neonatologist',
    'Neurologist',
    'Neurophysiologist',
    'Non medical Staff',
    'Nurse Practitioner (NP)',
    'Nutritionist',
    'Oculoplastic Surgeon',
    'Oncologist',
    'Ophthalmologist',
    'Oral and Maxillofacial Surgeon',
    'Orthodontist',
    'Orthopedist',
    'Owner',
    'Pathologist',
    'Pediatrician',
    'Pharmacist',
    'Pharmacologist',
    'Photographer',
    'Physician Assistant',
    'Physiotherapist',
    'Plastic and Reconstructive Surgeon',
    'Plastic Surgeon',
    'Practice Manager',
    'Press',
    'Product Project Manager',
    'Professor Teacher',
    'Psychiatrist',
    'Psychologist',
    'Psychotherapist',
    'Radiologist',
    'Registered Nurse (RN)',
    'Research Scientist',
    'Rheumatologist',
    'Sales',
    'Sports Medicine Physician',
    'Stomatologist',
    'Student Resident Fellow',
    'Trichologist',
    'Urologist',
    'Vascular Surgeon',
    'ENT Head and Neck Specialist',  # event-specific label
    'General Manager',  # legacy label: kept as a semantic target, not assigned by the rules
    'Nurse',  # legacy label: kept as a semantic target, not assigned by the rules
)


class SemanticDependencyError(ImportError):
    """Raised when the semantic fallback is requested but its packages are missing."""


class ReviewRejectedError(RuntimeError):
    """Raised when semantic matches are rejected during interactive review."""


class IntegrityError(RuntimeError):
    """Raised when the output would not contain exactly the input rows."""


# ---------------------------------------------------------------------------
# Semantic matching (SBERT + FAISS)
# ---------------------------------------------------------------------------

def _import_backends():
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SemanticDependencyError(
            "The semantic fallback needs sentence-transformers and faiss-cpu. "
            "Install them with: pip install sentence-transformers faiss-cpu  "
            "(or call normalize(..., semantic=False) to use the rules only)."
        ) from exc
    return faiss, np, SentenceTransformer


@lru_cache(maxsize=4)
def _index(model_name: str):
    """Embed the taxonomy labels once and store them in a FAISS L2 index."""
    faiss, np, SentenceTransformer = _import_backends()
    model = SentenceTransformer(model_name)
    embeddings = np.asarray(model.encode(list(TAXONOMY_LABELS)), dtype="float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return model, index, np


def semantic_match(titles: Sequence[str], model_name: str = DEFAULT_MODEL) -> Tuple[List[str], List[float]]:
    """Return the nearest taxonomy label and its L2 distance for each title."""
    if not titles:
        return [], []
    model, index, np = _index(model_name)
    labels: List[str] = []
    distances: List[float] = []
    for start in range(0, len(titles), BATCH_SIZE):
        batch = list(titles[start:start + BATCH_SIZE])
        vectors = np.asarray(model.encode(batch), dtype="float32")
        dist, idx = index.search(vectors, 1)
        labels.extend(TAXONOMY_LABELS[i] for i in idx[:, 0])
        distances.extend(float(d) for d in dist[:, 0])
    return labels, distances


# ---------------------------------------------------------------------------
# Human review
# ---------------------------------------------------------------------------

def review_matches(matches: pd.DataFrame) -> None:
    """Show every semantic match (original → normalised, count) and ask for confirmation."""
    print("\nSemantic matches to review (original → normalised, count):")
    for row in matches.itertuples(index=False):
        print(f"  {row.original_title} → {row.normalized_title} ({row.count})")
    while True:
        answer = input("\nHave you reviewed the semantic matches above? (yes/no): ").strip().lower()
        if answer == "yes":
            return
        if answer == "no":
            raise ReviewRejectedError("Semantic matches were rejected during review.")
        print("Please answer 'yes' or 'no'.")


# ---------------------------------------------------------------------------
# Integrity gates
# ---------------------------------------------------------------------------

def check_integrity(expected_rows: int, accounted_rows: int, output_rows: int) -> None:
    """Every input row must be accounted for and returned exactly once."""
    if not expected_rows == accounted_rows == output_rows:
        raise IntegrityError(
            f"Row count mismatch: {expected_rows} input rows, {accounted_rows} accounted for, "
            f"{output_rows} returned."
        )
