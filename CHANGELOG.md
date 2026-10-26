# Changelog

All notable changes to this project are documented here. This project follows [Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-10

### Added
- `normalize(data, column=...)`: works with any DataFrame and column name, a Series, or a list of titles.
- `normalize_title(title)`: normalise a single job title.
- New output columns `normalized_title` and `match_method` (`rules`, `semantic`, `placeholder`, `unmatched`).
- `semantic_threshold` to reject low-confidence semantic matches.
- `review="interactive"` to confirm semantic matches; rejection raises `ReviewRejectedError` instead of exiting.
- `NormalizationReport` with counts per method and label, semantic matches and unmatched titles.
- `TAXONOMY_LABELS`: the 100 standard labels.
- Quiet by default; `verbose=True` shows the rule engine's diagnostics.

### Changed
- The input DataFrame is never modified; row order and index are preserved and no row is dropped.
- Gastronomy titles are no longer set aside: they go through the rules and semantic stages like any other title.
- The embedding model and FAISS index are loaded once and cached.
- `run_pipeline()` is deprecated in favour of `normalize()`; it still works and now preserves row order.
- `TransformationHub.py` restructured into clean functions (semantic matching, review, integrity gates) that the library calls directly; same model, index, batch size and taxonomy.

### Removed
- `TransformationHubInternSources.py` (internal-only variant). Use `normalize(..., semantic=False)` for a rules-only run.
- Unused dependencies `nltk`, `scikit-learn` and the explicit `torch` pin (`sentence-transformers` still installs what it needs).

### Fixed
- The pipeline no longer stops (`sys.exit`) when gastronomy titles are present.

## [0.1.23] - 2026-10
### Added
- Automated test suite and GitHub Actions CI on Python 3.9–3.13.
### Fixed
- Crash on Python 3.11+ caused by inline regex flags (matching results unchanged).

## [0.1.22] - 2026-10
### Fixed
- README import example, missing `unidecode` dependency, deprecated `pkg_resources`, Windows build encoding.
