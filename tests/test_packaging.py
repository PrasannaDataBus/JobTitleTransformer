"""Packaging and loader checks: catch broken installs before they reach PyPI."""
from importlib.resources import files

import JobTitleTransformer
from JobTitleTransformer.runner import RULE_SCRIPTS
from JobTitleTransformer.job_scripts.TransformationHub import TAXONOMY_LABELS

SCRIPTS_DIR = files("JobTitleTransformer").joinpath("job_scripts")


def test_public_api_is_exposed():
    assert callable(JobTitleTransformer.run_pipeline)


def test_every_ordered_script_is_packaged():
    missing = [name for name in RULE_SCRIPTS if not SCRIPTS_DIR.joinpath(name).is_file()]
    assert missing == []


def test_no_duplicate_scripts_in_order():
    assert len(RULE_SCRIPTS) == len(set(RULE_SCRIPTS))


def test_preprocessing_runs_first():
    assert RULE_SCRIPTS[0] == "_encode_decode.py"
    assert "TransformationHub.py" not in RULE_SCRIPTS


def test_public_api():
    for name in ("normalize", "normalize_title", "run_pipeline", "NormalizationReport", "__version__"):
        assert hasattr(JobTitleTransformer, name)


def test_taxonomy_has_unique_labels():
    assert len(TAXONOMY_LABELS) == len(set(TAXONOMY_LABELS)) == 100


def test_only_the_expected_hub_scripts_are_shipped():
    names = {p.name for p in SCRIPTS_DIR.iterdir() if p.name.endswith(".py")}
    assert names - set(RULE_SCRIPTS) == {"TransformationHub.py", "__init__.py"}


def test_every_rule_script_compiles():
    for name in RULE_SCRIPTS:
        script = SCRIPTS_DIR.joinpath(name)
        compile(script.read_bytes(), str(script), "exec")
