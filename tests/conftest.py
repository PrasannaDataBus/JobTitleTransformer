"""Shared fixtures for JobTitleTransformer tests.

The rule engine (deterministic regex + exact-match stage) is tested directly.
The ML fallback (TransformationHub.py) needs sentence-transformers, FAISS and an
interactive review step, so it is excluded from automated tests.
"""
import contextlib
import io

import pandas as pd
import pytest
from importlib.resources import files

from JobTitleTransformer.runner import ORDERED_SCRIPTS

ML_STAGE = "TransformationHub.py"
SCRIPTS_DIR = files("JobTitleTransformer").joinpath("job_scripts")


def run_rules_namespace(titles):
    """Run every rule script (everything except the ML stage) and return the script namespace.

    Besides the main ``df``, preprocessing sets rows aside in ``df_other``
    (placeholders such as "Other" or bare numbers) and ``df_CWS`` (gastronomy titles).
    """
    df = pd.DataFrame({"speciality": list(titles)})
    namespace = {"df": df}
    with contextlib.redirect_stdout(io.StringIO()):  # scripts print diagnostics
        for name in ORDERED_SCRIPTS:
            if name == ML_STAGE:
                continue
            script = SCRIPTS_DIR.joinpath(name)
            exec(compile(script.read_bytes(), str(script), "exec"), namespace)
    return namespace


def run_rules(titles):
    """Return the main dataframe after the rule engine."""
    return run_rules_namespace(titles)["df"]


@pytest.fixture
def rules():
    return run_rules


@pytest.fixture
def rules_namespace():
    return run_rules_namespace
