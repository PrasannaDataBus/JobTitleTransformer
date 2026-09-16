# JobTitleTransformer

**JobTitleTransformer** is an enterprise-grade, hybrid `NLP pipeline` designed to ingest, sanitize, and normalize highly unstructured, multi-lingual healthcare job titles into a standardized corporate taxonomy. 

Built for seamless integration into broader `ETL workflows`, this library ensures high-quality `Data Modeling` for `Downstream Platforms` , including `Data Lakes`, `Data Hubs`, `Data Warehouses`, `Data Marts`, and `Semantic Models`.

## 🏗️ Pipeline Architecture

The transformation engine operates in a deterministic-to-probabilistic cascading sequence to balance execution speed with high recall:

1. **Vectorized Text Preprocessing:** Utilizes Pandas vectorized string operations for high-performance HTML entity decoding (`html.unescape`), Unicode normalization (`NFKD`), and automated noise/garbage character removal via compiled Regular Expressions.


2. **Deterministic Rules Engine:** Executes 100+ modular taxonomy scripts utilizing exact-match dictionary hashing and complex RegEx patterns for rapid, precise mapping of known variants, typos, and edge cases.


3. **Machine Learning Semantic Search (Fallback):** Unmatched string records are passed to an `AI fallback layer`. The pipeline generates vector embeddings using SBERT (`all-MiniLM-L6-v2`) and performs an L2 distance vector search via `Facebook AI Similarity Search (FAISS)` to semantically map unmatched job titles to the closest valid business category.


4. **Automated Data Integrity Gates:** Implements strict pre- and post-execution dataframe row-count validations to guarantee idempotency and zero data loss during transformations.

> ⚠️ Domain Constraint:** The taxonomy dictionary and ML embeddings are strictly optimized for the **Healthcare and Medical sectors**. 

---

## ⚙️ Installation

```bash
pip install jobtitletransformer
```

> ⚠️ Requirements: 
> * Python 3.8+
> * pandas
> * sentence-transformers
> * faiss-cpu

--- 

## 🚀 Integration & Usage

**Critical Dataframe Contract:** This library currently expects the input dataframe to be instantiated as df and the target text column to be explicitly named speciality.

```bash
# Environment & Installation Diagnostics
# The following checks verify that the package is correctly installed 
# and accessible within your active Python environment.

import sys
import importlib.util

print("sys.path:", sys.path)

# Verify the package specification exists before attempting import

spec = importlib.util.find_spec("JobTitleTransformer")
print("JobTitleTransformer found at:", spec.origin if spec else "NOT FOUND")

# Import the core package

import jobtitletransformer
print("JobTitleTransformer loaded from:", JobTitleTransformer.__file__)

# Data Ingestion

import pandas as pd

# Load your raw dataset. 
# Note: This can be adapted for SQL queries, JSON, or any Pandas-supported format.

raw_data = pd.read_csv("raw_healthcare_contacts.csv")

# Schema Enforcement
# The pipeline relies on a strict schema contract: 
# The dataframe must be named 'df' and the target column must be 'speciality'.
# We append .copy() to ensure we are working with a fresh dataframe in memory 
# and to prevent Pandas 'SettingWithCopy' warnings downstream.

df = raw_data.rename(columns={"job_title": "speciality"}).copy()

# Pipeline Execution
# Pass the dataframe into the transformation hub.
# The engine will sequentially execute RegEx dictionaries -> SBERT embeddings -> FAISS matching.
# It prints CLI diagnostics during execution and returns the fully normalized dataframe.

enriched_df = jobtitletransformer.run_pipeline(df)
```

🧠 Author & Maintainer

Prasanna - Senior Data Engineer & Analytics Specialist

📧 prasannadatabuss@gmail.com

🌐 GitHub: PrasannaDataBus