"""Public API: normalise job titles in a DataFrame, a Series, a list or a single string."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Union

import pandas as pd

from ._rules import ROW_ID, run_rules
from .job_scripts import TransformationHub as hub
from .job_scripts.TransformationHub import ReviewRejectedError, TAXONOMY_LABELS

logger = logging.getLogger("JobTitleTransformer")

NORMALIZED = "normalized_title"
METHOD = "match_method"

RULES = "rules"
SEMANTIC = "semantic"
PLACEHOLDER = "placeholder"
UNMATCHED = "unmatched"

_REVIEW_MODES = ("none", "interactive")
_LABELS = set(TAXONOMY_LABELS)


@dataclass
class NormalizationReport:
    """Summary of a normalisation run."""

    total: int
    by_method: dict
    by_label: dict
    semantic_matches: pd.DataFrame = field(repr=False)
    unmatched: List[str] = field(default_factory=list, repr=False)

    def summary(self) -> str:
        lines = [f"JobTitleTransformer: {self.total} titles"]
        for method in (RULES, SEMANTIC, PLACEHOLDER, UNMATCHED):
            count = self.by_method.get(method, 0)
            share = f"{count / self.total:.1%}" if self.total else "0.0%"
            lines.append(f"  {method:<12} {count:>8}  ({share})")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.summary()


def normalize(
    data: Union[pd.DataFrame, pd.Series, Iterable[str]],
    column: Optional[str] = None,
    *,
    semantic: bool = True,
    semantic_threshold: Optional[float] = None,
    model: str = hub.DEFAULT_MODEL,
    review: str = "none",
    verbose: bool = False,
    return_report: bool = False,
):
    """Normalise job titles to the standard taxonomy.

    Parameters
    ----------
    data:
        A DataFrame (with ``column``), a Series, or any iterable of strings.
    column:
        Name of the job-title column when ``data`` is a DataFrame.
    semantic:
        Use the SBERT + FAISS fallback for titles the rules do not recognise.
    semantic_threshold:
        Maximum L2 distance accepted from the semantic stage. Matches further away
        are reported as ``unmatched``. ``None`` accepts the nearest label, as the
        original pipeline did.
    model:
        Sentence-Transformers model used by the semantic stage.
    review:
        ``"none"`` (default) returns semantic matches flagged in ``match_method``;
        ``"interactive"`` prints them and asks for confirmation before returning.
    verbose:
        Show the rule scripts' detailed console diagnostics.
    return_report:
        Also return a :class:`NormalizationReport`.

    Returns
    -------
    pandas.DataFrame
        A copy of the input with two new columns, ``normalized_title`` and
        ``match_method`` (``rules``, ``semantic``, ``placeholder`` or ``unmatched``).
        Row order, index and the original column are preserved. With
        ``return_report=True``, a ``(DataFrame, NormalizationReport)`` tuple.
    """
    if review not in _REVIEW_MODES:
        raise ValueError(f"review must be one of {_REVIEW_MODES}, got {review!r}")

    frame, titles = _as_frame(data, column)
    n = len(titles)

    normalized: List[Optional[str]] = [None] * n
    method: List[str] = [UNMATCHED] * n
    distance: List[Optional[float]] = [None] * n

    if n:
        rules = run_rules(titles, verbose=verbose)
        hub.check_integrity(n, len(rules.main) + len(rules.placeholders), n)

        for row in rules.placeholders[ROW_ID]:
            method[row] = PLACEHOLDER

        hits = rules.main[rules.main["speciality"].isin(_LABELS)]
        for row, label in zip(hits[ROW_ID], hits["speciality"]):
            normalized[row], method[row] = label, RULES

        misses = rules.main[~rules.main["speciality"].isin(_LABELS)]
        logger.info("Rules matched %d of %d titles; %d placeholders; %d left for the semantic stage",
                    len(hits), n, len(rules.placeholders), len(misses))

        if semantic and len(misses):
            labels, dists = hub.semantic_match(misses["original_speciality"].astype(str).tolist(), model)
            for row, label, dist in zip(misses[ROW_ID], labels, dists):
                distance[row] = dist
                if semantic_threshold is None or dist <= semantic_threshold:
                    normalized[row], method[row] = label, SEMANTIC

    out = frame.copy()
    out[NORMALIZED] = pd.Series(normalized, index=out.index, dtype=object)
    out[METHOD] = pd.Series(method, index=out.index, dtype=object)

    hub.check_integrity(n, n, len(out))
    report = _build_report(titles, out, distance)
    if review == "interactive" and len(report.semantic_matches):
        hub.review_matches(report.semantic_matches)

    logger.info("\n%s", report.summary())
    return (out, report) if return_report else out


def normalize_title(title: str, **kwargs) -> Optional[str]:
    """Normalise a single job title and return its taxonomy label (or ``None``)."""
    kwargs.pop("return_report", None)
    return normalize([title], **kwargs)[NORMALIZED].iloc[0]


def _as_frame(data, column):
    if isinstance(data, pd.DataFrame):
        if column is None:
            if "speciality" in data.columns:
                column = "speciality"
            else:
                raise ValueError("Pass column=... with the name of the job-title column.")
        if column not in data.columns:
            raise KeyError(f"Column {column!r} not found. Available columns: {list(data.columns)}")
        return data, data[column]
    if isinstance(data, pd.Series):
        return data.to_frame(name=data.name if data.name is not None else "job_title"), data
    if isinstance(data, str):
        raise TypeError("Use normalize_title() for a single string, or pass a list of titles.")
    series = pd.Series(list(data), name="job_title", dtype=object)
    return series.to_frame(), series


def _build_report(titles, out, distance):
    semantic_rows = out[METHOD].to_numpy() == SEMANTIC
    matches = pd.DataFrame({
        "original_title": titles.to_numpy()[semantic_rows],
        NORMALIZED: out[NORMALIZED].to_numpy()[semantic_rows],
        "distance": [d for d, s in zip(distance, semantic_rows) if s],
    })
    if len(matches):
        matches = (matches.groupby(["original_title", NORMALIZED], as_index=False)
                   .agg(count=("distance", "size"), distance=("distance", "first"))
                   .sort_values(["count", "distance"], ascending=[False, True], ignore_index=True))
    unmatched = sorted({str(t) for t, m in zip(titles, out[METHOD]) if m == UNMATCHED})
    return NormalizationReport(
        total=len(out),
        by_method=out[METHOD].value_counts().to_dict(),
        by_label=out[NORMALIZED].value_counts().to_dict(),
        semantic_matches=matches,
        unmatched=unmatched,
    )

