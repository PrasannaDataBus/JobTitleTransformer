"""Run the curated rule scripts on a column of job titles.

The rule scripts in ``job_scripts/`` are executed unchanged, in their original
order. This module only isolates them: it gives them a fresh namespace, keeps
their console diagnostics out of the way unless asked for, and tracks every input
row so results can be returned in the original order.
"""
from __future__ import annotations

import contextlib
import io
import warnings
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files

import pandas as pd

from .runner import RULE_SCRIPTS

ROW_ID = "_jtt_row"
_SCRIPTS_DIR = files("JobTitleTransformer").joinpath("job_scripts")


@lru_cache(maxsize=None)
def _compiled(name: str):
    script = _SCRIPTS_DIR.joinpath(name)
    return compile(script.read_bytes(), str(script), "exec")


@dataclass
class RuleOutput:
    """Rows that went through the rules (``main``) and rows set aside as placeholders."""

    main: pd.DataFrame          # columns: ROW_ID, speciality, original_speciality
    placeholders: pd.DataFrame  # columns: ROW_ID, speciality


def run_rules(titles: pd.Series, verbose: bool = False) -> RuleOutput:
    """Apply preprocessing and every category script to ``titles``."""
    frame = pd.DataFrame({"speciality": titles.astype(object).to_numpy(), ROW_ID: range(len(titles))})
    namespace = {"df": frame}
    stdout = contextlib.nullcontext() if verbose else contextlib.redirect_stdout(io.StringIO())
    with stdout, warnings.catch_warnings():
        warnings.simplefilter("ignore")  # pandas copy / regex-group warnings from the scripts
        for name in RULE_SCRIPTS:
            exec(_compiled(name), namespace)
    main = namespace["df"][[ROW_ID, "speciality", "original_speciality"]].copy()
    placeholders = namespace["df_other"][[ROW_ID, "speciality"]].copy()
    return RuleOutput(main=main, placeholders=placeholders)
