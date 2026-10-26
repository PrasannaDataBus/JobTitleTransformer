"""JobTitleTransformer: normalise messy, multilingual healthcare job titles to a standard taxonomy.

>>> import JobTitleTransformer as jtt
>>> jtt.normalize_title("Dermatologue", semantic=False)
'Dermatologist'
"""
from .api import NormalizationReport, normalize, normalize_title
from .job_scripts.TransformationHub import (
    TAXONOMY_LABELS,
    IntegrityError,
    ReviewRejectedError,
    SemanticDependencyError,
)
from .runner import run_pipeline

__version__ = "0.3.0"

__all__ = [
    "normalize",
    "normalize_title",
    "run_pipeline",
    "NormalizationReport",
    "ReviewRejectedError",
    "IntegrityError",
    "SemanticDependencyError",
    "TAXONOMY_LABELS",
    "__version__",
]
