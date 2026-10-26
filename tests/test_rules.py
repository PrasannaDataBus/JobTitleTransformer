"""Behaviour of the deterministic rule engine on real-world title variants."""
import pytest

KNOWN_MAPPINGS = [
    # Canonical titles
    ("Dermatologist", "Dermatologist"),
    ("Plastic Surgeon", "Plastic Surgeon"),
    ("Aesthetic Physician", "Aesthetic Physician"),
    ("Dentist", "Dentist"),
    ("Cardiologist", "Cardiologist"),
    ("Ophthalmologist", "Ophthalmologist"),
    ("Clinic Manager", "Clinic Manager"),
    # Normalised to the taxonomy label
    ("Nurse Practitioner", "Nurse Practitioner (NP)"),
    ("RN", "Registered Nurse (RN)"),
    ("CEO", "Company CEO"),
    ("Gynecologist", "Gynecologist Obstetrician"),
    ("Esthetician", "Esthetician Cosmetician"),
    # Typos
    ("Dermatogist", "Dermatologist"),
    # Multilingual variants
    ("Dermatologue", "Dermatologist"),
    ("dermatologista", "Dermatologist"),
    ("Cirujano Plastico", "Plastic Surgeon"),
    ("Medico Estetico", "Aesthetic Physician"),
    ("Médecin Esthétique", "Aesthetic Physician"),
    # HTML entities decoded before matching
    ("Plastic &amp; Reconstructive Surgeon", "Plastic and Reconstructive Surgeon"),
    ("Dermatologist &amp; Venereologist", "Dermatologist"),
]


@pytest.mark.parametrize("raw, expected", KNOWN_MAPPINGS)
def test_known_titles_map_to_taxonomy(rules, raw, expected):
    assert rules([raw])["speciality"].iloc[0] == expected


def test_unknown_titles_are_left_for_the_ml_stage(rules):
    assert rules(["xyz unknown 123"])["speciality"].iloc[0] == "xyz unknown 123"


def test_no_rows_are_lost_by_the_rule_engine(rules_namespace):
    """Every input row ends up in the main frame or in one of the set-aside frames."""
    raw = [raw for raw, _ in KNOWN_MAPPINGS] + ["xyz unknown 123", "", "Other", "42", "Chef"]
    ns = rules_namespace(raw)
    assert len(ns["df"]) + len(ns["df_other"]) == len(raw)


@pytest.mark.parametrize("title", ["Chef", "Baker", "Gastroenterologist"])
def test_former_gastronomy_titles_flow_through(rules_namespace, title):
    """Gastronomy titles are no longer set aside: they stay in the main frame."""
    ns = rules_namespace(["Dermatologist", title])
    assert ns["df"]["speciality"].tolist() == ["Dermatologist", title]
    assert "df_CWS" not in ns


@pytest.mark.parametrize("placeholder", ["", "Other", "-", "42", "x"])
def test_placeholders_are_set_aside_not_transformed(rules_namespace, placeholder):
    ns = rules_namespace(["Dermatologist", placeholder])
    assert ns["df"]["speciality"].tolist() == ["Dermatologist"]
    assert len(ns["df_other"]) == 1


def test_batch_matches_individual_results(rules):
    raw = [raw for raw, _ in KNOWN_MAPPINGS]
    out = rules(raw)["speciality"].tolist()
    assert out == [expected for _, expected in KNOWN_MAPPINGS]
