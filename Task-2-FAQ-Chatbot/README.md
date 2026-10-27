# TechAssist — Intelligent FAQ Support Chatbot
### CodeAlpha AI Internship — Task 2

![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.12%20%7C%203.14-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg)
![Tests](https://img.shields.io/badge/pytest-28%20passed-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**TechAssist** is an intelligent, privacy-focused FAQ retrieval chatbot built for the **CodeAlpha AI Internship Task 2**. It delivers instant, accurate technical troubleshooting guidance by pairing Natural Language Processing (NLP) text preprocessing with TF-IDF vectorization and cosine similarity matching over a curated, verified technical knowledge base.

Unlike opaque cloud-based generative AI systems, TechAssist runs **100% locally**, executes deterministically, and provides explainable similarity scores, verified answers, and clear fallback suggestions when a question falls outside its domain.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Product Identity](#product-identity)
3. [Architecture & How It Works](#architecture--how-it-works)
   - [NLP Preprocessing Pipeline](#1-nlp-preprocessing-pipeline)
   - [TF-IDF Vectorization & Cosine Similarity](#2-tf-idf-vectorization--cosine-similarity)
   - [Coverage Guard & Threshold Calibration](#3-coverage-guard--threshold-calibration)
   - [Fallback Mechanism](#4-fallback-mechanism)
4. [Knowledge Base Structure](#knowledge-base-structure)
5. [Project Directory Layout](#project-directory-layout)
6. [Installation & Setup (Windows PowerShell)](#installation--setup-windows-powershell)
7. [Running the Application](#running-the-application)
8. [Running the Test Suite](#running-the-test-suite)
9. [Example Questions Supported](#example-questions-supported)
10. [How to Add or Modify FAQs](#how-to-add-or-modify-faqs)
11. [Known Limitations & Design Trade-offs](#known-limitations--design-trade-offs)
12. [Troubleshooting](#troubleshooting)
13. [Privacy & Security](#privacy--security)

---

## Key Features

- **90+ Verified Technical FAQs**: High-quality troubleshooting instructions across 9 core categories:
  - Computer & Laptop Troubleshooting
  - Software Installation & Updates
  - Internet & Wi-Fi Problems
  - Account Access & Password Issues
  - File Management & Backups
  - Operating-System Issues
  - Application Errors
  - Basic Cybersecurity & Safe Computing
  - General Technical Support
- **Multi-Variant Indexing**: Every FAQ indexes canonical questions plus multiple realistic alternative phrasings (over 465 total indexed variants including conversational English & bilingual Hinglish variants).
- **Meaning-Preserving Preprocessing**: Custom tokenization and lemmatization that preserves critical negation words (`not`, `cannot`, `won't`) and technical terms (`wifi`, `bsod`, `ip`, `ssd`, `usb`).
- **TF-IDF + Cosine Similarity Engine**: Mathematically rigorous information retrieval with unigrams and bigrams.
- **Out-of-Vocabulary Coverage Guard**: Multiplies raw cosine scores by token coverage to prevent false-positive matches on single generic verbs (`make`, `fix`) when the core subject is unknown.
- **Calibrated Decision Threshold**: Rigorously tested cutoff (`0.32`) providing separation between relevant queries and out-of-domain input.
- **Premium SaaS Dark UI**: Modern Streamlit interface with navy/charcoal styling, responsive layouts, suggested topic cards, confidence badges, and interactive category explorer.
- **100% Local & Offline**: Zero external LLM APIs, no API key requirements, and zero user data transmission.

---

## Product Identity

- **Product Name:** TechAssist
- **Subtitle:** Intelligent FAQ Support
- **Welcome Headline:** How can I help you today?
- **Short Description:** Get helpful answers to common technology questions through intelligent FAQ matching.

---

## Architecture & How It Works

```
                                      [User Query]
                                           │
                                           ▼
                            ┌─────────────────────────────┐
                            │  TextPreprocessor           │
                            │  - Unicode NFKD normalizer  │
                            │  - Lowercase & contractions │
                            │  - Negation-preserving stop  │
                            │  - Lemmatization / Stemming │
                            └──────────────┬──────────────┘
                                           │ Preprocessed Query
                                           ▼
                            ┌─────────────────────────────┐
                            │  TF-IDF Vectorizer          │
                            │  (Unigrams & Bigrams)       │
                            └──────────────┬──────────────┘
                                           │ Query Vector
                                           ▼
┌─────────────────────────┐ ┌─────────────────────────────┐
│  Indexed FAQ Variants   │─▶  Cosine Similarity Matrix   │
│  (316 Variants Matrix)  │ └──────────────┬──────────────┘
└─────────────────────────┘                │
                                           ▼
                            ┌─────────────────────────────┐
                            │  Query-Token Coverage Guard │
                            │  (Penalizes OOV Mismatches) │
                            └──────────────┬──────────────┘
                                           │ Calibrated Score
                                           ▼
                                ┌─────────────────────┐
                                │ Score >= Threshold? │
                                └──────────┬──────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼ YES                                 ▼ NO
          ┌───────────────────────────┐         ┌───────────────────────────┐
          │ High/Medium Confidence    │         │ Friendly Fallback State   │
          │ - Parent FAQ Answer       │         │ - "No direct match" note  │
          │ - Category & Match Score  │         │ - Closest Related FAQs    │
          └───────────────────────────┘         └───────────────────────────┘
```

### 1. NLP Preprocessing Pipeline (`nlp_preprocessing.py`)
Incoming queries and FAQ entries undergo systematic text preprocessing:
1. **Unicode Normalization:** Converts accented glyphs and smart characters into canonical ASCII/Unicode form using `unicodedata.normalize('NFKD')`.
2. **Contraction Expansion:** Expands colloquialisms (`won't` $\to$ `will not`, `can't` $\to$ `cannot`).
3. **Punctuation Stripping:** Cleans symbols while standardizing hyphenated tech terms (e.g., `wi-fi` $\to$ `wifi`).
4. **Negation-Preserving Stopword Filtering:** Standard NLP stopword lists discard words like `not` and `no`. TechAssist explicitly protects negations so queries like *"laptop not charging"* are never confused with *"laptop charging"*.
5. **Morphological Lemmatization:** Uses NLTK's `WordNetLemmatizer` (with `PorterStemmer` fallback) to map plural nouns and inflected verbs to their lemma (`freezing` $\to$ `freeze`, `updates` $\to$ `update`).

### 2. TF-IDF Vectorization & Cosine Similarity (`chatbot.py`)
- **Term Frequency-Inverse Document Frequency (TF-IDF)** converts text strings into high-dimensional vector representations. Words unique to specific technical problems receive higher weights, while common conversational fillers receive lower weights.
- **Cosine Similarity** evaluates the normalized inner product between the query vector $\vec{q}$ and document vector $\vec{d}$:
  $$\text{Cosine Similarity}(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\|_2 \|\vec{d}\|_2}$$
  Because vectors are L2-normalized, values range from $0.0$ (orthogonal / no overlap) to $1.0$ (identical vocabulary distribution).

### 3. Coverage Guard & Threshold Calibration
Standard TF-IDF can produce false positives if an out-of-domain query (e.g., *"how to make pizza"*) contains a single generic word (e.g., `make`) that happens to exist in a technical FAQ variant (e.g., *"Make user account an admin"*).

TechAssist implements an **out-of-vocabulary (OOV) coverage penalty**:
$$\text{Score}_{\text{calibrated}} = \text{Score}_{\text{raw}} \times \sqrt{\text{Coverage}}$$
where $\text{Coverage} = \frac{|\text{Query Tokens} \cap \text{Variant Tokens}|}{|\text{Query Tokens}|}$.

- When all words match, $\text{Coverage} = 1.0$ and the score is unchanged.
- When unrelated words are present, the score drops sharply below the threshold.
- **Empirical Threshold:** Set to `0.32`. In calibration benchmarks:
  - Relevant/paraphrased queries score between **0.411 and 1.000**.
  - Unrelated queries score between **0.000 and 0.278**.
  - The resulting **0.134 separation margin** ensures strong classification precision.

### 4. Fallback Mechanism
When the best candidate score is below `0.32`, the chatbot avoids guessing or fabricating answers. Instead, it returns a polite, transparent fallback message:
> *"I'm sorry, I couldn't find a sufficiently relevant answer in my FAQ database. Please try rephrasing your question or check the suggestions below."*

It simultaneously provides the top 2-3 closest related questions from the dataset so users can quickly navigate to the right topic.

---

## Knowledge Base Structure

The knowledge base is maintained in `data/faqs.json`. Each entry adheres to this schema:

```json
{
  "id": "hw-01",
  "category": "Computer and Laptop Troubleshooting",
  "question": "Why is my laptop running so slow and how can I speed it up?",
  "alternatives": [
    "My computer is lagging badly, what can I do?",
    "How to fix a slow laptop?",
    "PC running very slow and freezing",
    "Why is my laptop taking forever to respond?"
  ],
  "answer": "A slow computer is usually caused by excessive startup applications..."
}
```

The system automatically validates that all required fields are present, IDs are unique, questions and answers are non-empty, and alternatives are valid lists.

---

## Project Directory Layout

```
CodeAlpha_FAQChatbot/
├── app.py                      # Premium Streamlit web application & UI
├── chatbot.py                  # Core TF-IDF matching engine & FAQ validator
├── nlp_preprocessing.py        # Text preprocessing, negation handling, lemmatization
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive documentation & user guide
├── .gitignore                  # Git exclusions for environments and caches
├── data/
│   └── faqs.json               # 63+ curated technical FAQ records
└── tests/
    ├── test_chatbot.py         # 19 matching, validation & threshold tests
    └── test_preprocessing.py   # 9 NLP normalization & edge-case tests
```

---

## Installation & Setup (Windows PowerShell)

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.14 installed on your Windows machine.
- Windows PowerShell.

### Step 1: Open PowerShell in the Project Directory
```powershell
cd "c:\Users\Om Tripathi\Downloads\CodeAlpha_AI_Internship_Projects\CodeAlpha_AI_Internship\CodeAlpha_FAQChatbot"
```

### Step 2: Create a Local Virtual Environment
```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell displays an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once).*

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Download Required NLTK Corpora (One-Time)
```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

---

## Running the Application

Launch the Streamlit web interface with:

```powershell
streamlit run app.py
```

Once started, the application opens automatically in your default browser at:
```
http://localhost:8501
```

### Navigating the UI:
- **Chat Assistant**: Ask any technical question in natural language, or click any of the 4 suggested topic cards on the welcome screen.
- **Browse FAQs**: Search the entire knowledge base by keyword or filter by technical category. Click **"Ask this in Chat"** on any FAQ to test it immediately.
- **New Chat**: Click **"➕ New Chat"** in the sidebar at any time to clear history and reset to the welcome state.

---

## Running the Test Suite

The test suite verifies dataset integrity, edge cases, Unicode handling, negation preservation, alternative phrasings, and threshold behavior using `pytest`.

Execute all tests with:

```powershell
pytest -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.x, pytest-9.x.x
collected 28 items

tests/test_chatbot.py::test_dataset_loaded_count PASSED                  [  3%]
tests/test_chatbot.py::test_missing_dataset_file PASSED                  [  7%]
tests/test_chatbot.py::test_invalid_json_file PASSED                     [ 10%]
tests/test_chatbot.py::test_empty_dataset_file PASSED                    [ 14%]
tests/test_chatbot.py::test_validation_detects_missing_fields PASSED     [ 17%]
tests/test_chatbot.py::test_validation_detects_duplicate_ids PASSED      [ 21%]
tests/test_chatbot.py::test_empty_query PASSED                           [ 25%]
tests/test_chatbot.py::test_whitespace_and_punctuation_query PASSED      [ 28%]
tests/test_chatbot.py::test_exact_canonical_question_match PASSED        [ 32%]
tests/test_chatbot.py::test_alternative_phrasing_match PASSED            [ 35%]
tests/test_chatbot.py::test_paraphrased_query_match PASSED               [ 39%]
tests/test_chatbot.py::test_wifi_issue_matching PASSED                   [ 42%]
tests/test_chatbot.py::test_bsod_troubleshooting PASSED                  [ 46%]
tests/test_chatbot.py::test_unrelated_query_rejection PASSED             [ 50%]
tests/test_chatbot.py::test_threshold_behavior PASSED                    [ 53%]
tests/test_chatbot.py::test_unicode_query_matching PASSED                [ 57%]
tests/test_chatbot.py::test_suggested_questions PASSED                   [ 60%]
tests/test_chatbot.py::test_search_faqs_by_keyword PASSED                [ 64%]
tests/test_chatbot.py::test_search_faqs_by_category PASSED               [ 67%]
tests/test_preprocessing.py::test_normalize_lowercase PASSED             [ 71%]
tests/test_preprocessing.py::test_whitespace_normalization PASSED        [ 75%]
tests/test_preprocessing.py::test_punctuation_handling PASSED            [ 78%]
tests/test_preprocessing.py::test_negation_preservation PASSED           [ 82%]
tests/test_preprocessing.py::test_tech_keywords_protection PASSED        [ 85%]
tests/test_preprocessing.py::test_unicode_normalization PASSED           [ 89%]
tests/test_preprocessing.py::test_empty_and_whitespace_input PASSED      [ 92%]
tests/test_preprocessing.py::test_short_and_pure_punctuation PASSED      [ 96%]
tests/test_preprocessing.py::test_convenience_function PASSED            [100%]

============================= 28 passed in 5.37s ==============================
```

---

## Example Questions Supported

| Category | Example User Query | Matched Parent FAQ |
|---|---|---|
| **Computer Troubleshooting** | *"My PC is running very slow and freezing up"* | `hw-01` (Slow laptop troubleshooting) |
| **Hardware** | *"Laptop won't power on or charge at all"* | `hw-02` (Power/battery troubleshooting) |
| **System Crash** | *"Windows crashed with a blue screen of death"* | `hw-04` (BSOD troubleshooting) |
| **Networking** | *"Wi-Fi says connected but no internet access"* | `net-01` (Wi-Fi connectivity & DNS flush) |
| **Security** | *"How do I spot a phishing email scam?"* | `sec-01` (Phishing detection guide) |
| **Accounts** | *"Forgot my Windows login password PIN"* | `acc-01` (Windows credential reset) |
| **File Management** | *"What is the 3-2-1 backup strategy?"* | `file-01` (3-2-1 backup implementation) |
| **Application Errors** | *"VCRUNTIME140.dll missing error when opening game"* | `app-01` (Visual C++ Redistributable fix) |
| **Operating System** | *"How to enter Safe Mode in Windows 11?"* | `os-01` (Windows Safe Mode guide) |

---

## How to Add or Modify FAQs

You can easily expand the knowledge base without modifying any Python code:

1. Open `data/faqs.json` in any text editor.
2. Add a new JSON object adhering to the schema:
   ```json
   {
     "id": "net-08",
     "category": "Internet and Wi-Fi Problems",
     "question": "How do I configure a static IP address on Windows?",
     "alternatives": [
       "Set static IP in Windows 11",
       "Assign manual IP address to computer",
       "How to change from DHCP to static IP?"
     ],
     "answer": "To assign a static IP address: 1) Open Settings > Network & internet..."
   }
   ```
3. Save the file.
4. Restart the Streamlit application (or trigger New Chat); the index rebuilds automatically on startup.

---

## Known Limitations & Design Trade-offs

1. **Information Retrieval vs. Generative Synthesis:** TechAssist is an FAQ retrieval engine, not a generative large language model. It retrieves pre-verified technical answers and will not synthesize answers for unindexed topics.
2. **Vocabulary Dependence:** While unigram/bigram TF-IDF and lemmatization handle common synonyms and inflections effectively, extreme typos or slang not present in alternative phrasings may lower the cosine score below the threshold.
3. **Domain Boundary:** Out-of-scope inquiries (e.g., cooking, politics, geography) are intentionally rejected by design to maintain technical support integrity.

---

## Troubleshooting

- **PowerShell Script Execution Error:**
  - *Fix:* Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell.
- **Port 8501 in Use:**
  - *Fix:* Launch Streamlit on a different port: `streamlit run app.py --server.port 8502`.
- **Missing NLTK Data:**
  - *Fix:* Re-run the one-time NLTK download command specified in Step 5 of the Setup guide.

---

## Privacy & Security

TechAssist is designed with a **privacy-first architecture**:
- **Zero Cloud Calls:** No queries, transcripts, or user telemetry are sent to third-party APIs.
- **Fully Local Processing:** All vectorization, indexing, and scoring take place in system RAM on your machine.
- **Safe Technical Guidance:** Knowledge base answers follow established IT administration standards without destructive automated commands.

---

## Project Metadata & Attribution

- **Project:** CodeAlpha AI Internship — Task 2
- **Developer:** Om Tripathi
- **Repository Scope:** Local standalone development (Git operations excluded per project directive)

