"""Behaviour of the public API: shapes, order, methods, review and the semantic stage."""
import pandas as pd
import pytest

import JobTitleTransformer as jtt
from JobTitleTransformer.job_scripts import TransformationHub as hub
from JobTitleTransformer.job_scripts.TransformationHub import TAXONOMY_LABELS


@pytest.fixture
def fake_semantic(monkeypatch):
    """Replace the semantic matcher: every title maps to 'General Physician' at distance 0.5."""
    calls = []

    def match(titles, model_name=hub.DEFAULT_MODEL):
        calls.append(list(titles))
        return ["General Physician"] * len(titles), [0.5] * len(titles)

    monkeypatch.setattr(hub, "semantic_match", match)
    return calls


def sample():
    return pd.DataFrame(
        {"id": [1, 2, 3, 4], "job_title": ["Dermatologue", "Other", "Chef", "RN"]},
        index=["a", "b", "c", "d"],
    )


def test_adds_columns_and_preserves_input():
    df = sample()
    out = jtt.normalize(df, column="job_title", semantic=False)
    assert list(out.columns) == ["id", "job_title", "normalized_title", "match_method"]
    assert out.index.tolist() == ["a", "b", "c", "d"]
    assert out["job_title"].tolist() == df["job_title"].tolist()
    assert "normalized_title" not in df.columns  # input not modified


def test_match_methods_without_semantic():
    out = jtt.normalize(sample(), column="job_title", semantic=False)
    assert out["match_method"].tolist() == ["rules", "placeholder", "unmatched", "rules"]
    assert out["normalized_title"].tolist() == ["Dermatologist", None, None, "Registered Nurse (RN)"]


def test_semantic_stage_fills_unmatched_rows(fake_semantic):
    out = jtt.normalize(sample(), column="job_title")
    assert out.loc["c", "normalized_title"] == "General Physician"
    assert out.loc["c", "match_method"] == "semantic"
    assert fake_semantic == [["Chef"]]  # only titles the rules missed are sent


def test_semantic_threshold_rejects_far_matches(fake_semantic):
    out = jtt.normalize(sample(), column="job_title", semantic_threshold=0.1)
    assert out.loc["c", "match_method"] == "unmatched"
    assert pd.isna(out.loc["c", "normalized_title"])


def test_report(fake_semantic):
    _, report = jtt.normalize(sample(), column="job_title", return_report=True)
    assert report.total == 4
    assert report.by_method == {"rules": 2, "placeholder": 1, "semantic": 1}
    assert report.semantic_matches.to_dict("records") == [
        {"original_title": "Chef", "normalized_title": "General Physician", "count": 1, "distance": 0.5}
    ]
    assert "rules" in report.summary()


def test_interactive_review_accept_and_reject(fake_semantic, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    assert jtt.normalize(sample(), column="job_title", review="interactive") is not None
    monkeypatch.setattr("builtins.input", lambda _: "no")
    with pytest.raises(jtt.ReviewRejectedError):
        jtt.normalize(sample(), column="job_title", review="interactive")


def test_accepts_series_list_and_single_title():
    assert jtt.normalize(pd.Series(["Dermatologue"]), semantic=False)["normalized_title"].iloc[0] == "Dermatologist"
    assert jtt.normalize(["RN"], semantic=False)["normalized_title"].iloc[0] == "Registered Nurse (RN)"
    assert jtt.normalize_title("dermatogist", semantic=False) == "Dermatologist"


def test_defaults_to_speciality_column():
    out = jtt.normalize(pd.DataFrame({"speciality": ["Dermatologue"]}), semantic=False)
    assert out["normalized_title"].iloc[0] == "Dermatologist"


def test_helpful_errors():
    with pytest.raises(ValueError):
        jtt.normalize(pd.DataFrame({"x": ["a"]}), semantic=False)
    with pytest.raises(KeyError):
        jtt.normalize(pd.DataFrame({"x": ["a"]}), column="job_title", semantic=False)
    with pytest.raises(ValueError):
        jtt.normalize(["a"], review="maybe")
    with pytest.raises(TypeError):
        jtt.normalize("Dermatologue")


def test_empty_input():
    out = jtt.normalize(pd.DataFrame({"job_title": []}), column="job_title")
    assert len(out) == 0 and "normalized_title" in out.columns


def test_legacy_run_pipeline(fake_semantic, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    df = pd.DataFrame({"speciality": ["Dermatologue", "Chef"]})
    with pytest.warns(DeprecationWarning):
        out = jtt.run_pipeline(df)
    assert out["speciality"].tolist() == ["Dermatologist", "General Physician"]
    assert out["original_speciality"].tolist() == ["Dermatologue", "Chef"]


def test_real_faiss_index_with_stand_in_encoder(monkeypatch):
    """Exercise the real FAISS search path with a deterministic stand-in encoder."""
    faiss = pytest.importorskip("faiss")
    np = pytest.importorskip("numpy")

    class StandInEncoder:
        def __init__(self, name):
            self.name = name

        def encode(self, texts):
            # Bag-of-letters vectors: close strings get close vectors.
            out = np.zeros((len(texts), 26), dtype="float32")
            for i, text in enumerate(texts):
                for ch in text.lower():
                    if "a" <= ch <= "z":
                        out[i, ord(ch) - 97] += 1
            return out

    monkeypatch.setattr(hub, "_import_backends", lambda: (faiss, np, StandInEncoder))
    hub._index.cache_clear()
    try:
        titles = [TAXONOMY_LABELS[5], TAXONOMY_LABELS[42]] * 20  # 40 titles -> two batches of 30
        labels, distances = hub.semantic_match(titles, model_name="stand-in")
        assert labels == titles
        assert all(d == pytest.approx(0.0) for d in distances)
    finally:
        hub._index.cache_clear()


def test_integrity_gate():
    hub.check_integrity(3, 3, 3)
    with pytest.raises(jtt.IntegrityError):
        hub.check_integrity(3, 2, 3)
