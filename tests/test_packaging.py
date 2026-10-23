"""Packaging and loader checks: catch broken installs before they reach PyPI."""
from importlib.resources import files

import JobTitleTransformer
from JobTitleTransformer.runner import ORDERED_SCRIPTS

SCRIPTS_DIR = files("JobTitleTransformer").joinpath("job_scripts")


def test_public_api_is_exposed():
    assert callable(JobTitleTransformer.run_pipeline)


def test_every_ordered_script_is_packaged():
    missing = [name for name in ORDERED_SCRIPTS if not SCRIPTS_DIR.joinpath(name).is_file()]
    assert missing == []


def test_no_duplicate_scripts_in_order():
    assert len(ORDERED_SCRIPTS) == len(set(ORDERED_SCRIPTS))


def test_preprocessing_runs_first_and_ml_last():
    assert ORDERED_SCRIPTS[0] == "_encode_decode.py"
    assert ORDERED_SCRIPTS[-1] == "TransformationHub.py"


def test_every_rule_script_compiles():
    for name in ORDERED_SCRIPTS:
        script = SCRIPTS_DIR.joinpath(name)
        compile(script.read_bytes(), str(script), "exec")
