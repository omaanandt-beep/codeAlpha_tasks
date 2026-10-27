# SynapseTranslate 🌐⚡

> **Neural Machine Translation Studio • Privacy-First On-Device Engine • Multilingual Voice & Indic Marathi Pipeline**  
> Developed for the **CodeAlpha Artificial Intelligence Internship**.

---

## 📖 Project Overview
**SynapseTranslate** is a privacy-first neural machine translation and speech studio built with Python, Streamlit, and Argos Translate. Unlike typical translators that beam sensitive text and confidential documents across cloud APIs (Google Cloud, OpenAI, DeepL), SynapseTranslate executes its core neural machine translation **completely on-device**.

Once models are installed, neural text translation functions without an active internet connection, guaranteeing zero text logging, zero telemetry, and zero recurring API costs.

---

## ✨ Key Features
- **100% On-Device Neural Translation Engine:** Powered by OpenNMT and CTranslate2 via Argos Translate with zero text telemetry.
- **🎙️ Speak to Translate (Voice Dictation):** Speak naturally into your microphone in any supported language; audio is transcribed directly into the studio translation box.
- **🔊 Multilingual Speech Pronunciation (TTS):** One-click natural voice playback for translations with auto-play support and offline speech engine fallback.
- **⚡ Indic Linguistic Bridge for Marathi:** Custom morphological and syntactic transfer pipeline bridging English and Marathi without religious token hallucinations.
- **Smart Dynamic Routing:** Discovers direct neural models (`en` ↔ `hi`, `en` ↔ `es`, `en` ↔ `fr`, etc.) and automatically establishes intelligent pivot routes for complex language pairs.
- **16 Supported Languages:**
  - English (`en`)
  - Hindi (`hi`) — हिन्दी
  - Marathi (`mr`) — मराठी
  - Spanish (`es`) — Español
  - French (`fr`) — Français
  - German (`de`) — Deutsch
  - Italian (`it`) — Italiano
  - Portuguese (`pt`) — Português
  - Russian (`ru`) — Русский
  - Arabic (`ar`) — العربية
  - Chinese Simplified (`zh`) — 简体中文
  - Japanese (`ja`) — 日本語
  - Korean (`ko`) — 한국어
  - Bengali (`bn`) — বাংলা
  - Urdu (`ur`) — اردو
  - Turkish (`tr`) — Türkçe
- **Formatting & Sentence-Safe Chunking:** Retains paragraph breaks and multi-sentence structures without truncation.
- **Local Language Auto-Detection:** Purely on-device script identification powered by `langdetect`.
- **Cyber-Luxe Glassmorphic Studio UI:** Floating glow effects, dual-card studio panes, quick action presets, live character & token telemetry, and one-click copy/download.

---

## 🛠️ Technology Stack
- **Language:** Python (3.10 – 3.14 compatible)
- **UI Framework:** Streamlit (Glassmorphic Custom Cyber-Luxe CSS)
- **Translation Engine:** Argos Translate (OpenNMT + CTranslate2) & Custom Indic Pipeline
- **Speech Recognition:** `SpeechRecognition` (Microphone voice dictation input)
- **Speech Synthesis:** `gTTS` & `pyttsx3` (Multilingual voice audio synthesis)
- **Language Identification:** `langdetect`
- **Testing Suite:** Pytest (100% Passing Unit Test Coverage)

---

## 🖼️ Application Preview

```
+========================================================================================+
|  [A ⮂ अ] SynapseTranslate                                ● ACTIVE • 16 MODELS LOADED  |
|  Deep Neural Translation Studio • 100% Air-Gapped Privacy • Marathi & Multilingual     |
+========================================================================================+
|  SOURCE: English [auto/en]                       TARGET: Marathi (मराठी) [mr]          |
|  +-------------------------------------+   ⇄    +------------------------------------+ |
|  | Artificial intelligence is          | ---->  | कृत्रिम बुद्धिमत्ता आधुनिक         | |
|  | transforming modern technology.     | [TRANS]| तंत्रज्ञानात बदल घडवून आणत आहे.     | |
|  +-------------------------------------+        +------------------------------------+ |
|  [CHARS: 56] [WORDS: 6] [READ: ~2s]             [ROUTE: Direct Indic Pivot Engine]     |
|  [🗑️ Clear] [🎙️ Speak to Translate]             [📋 Copy Text] [🔊 Voice Audio]        |
+========================================================================================+
```

---

## 🚀 Windows PowerShell Setup & Usage Guide

### Step 1: Clone Repository and Setup Virtual Environment
Open PowerShell:
```powershell
# Clone the repository
git clone https://github.com/omaanandt-beep/codeAlpha_tasks.git
cd codeAlpha_tasks

# Create a local virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Install Offline Translation Models (One-Time Setup)
Run the automated model management tool to download and register offline models (e.g. English ↔ Hindi, Spanish, French, German, Chinese, etc.):
```powershell
python setup_models.py
```
*Note: This step requires an internet connection once to download neural weight packages. Once downloaded, all translation runs 100% on-device.*

### Step 4: Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
The application will launch in your browser at `http://localhost:8501`.

### Step 5: Run Automated Tests
```powershell
pytest tests/ -v
```

---

## 🔒 Architecture & Privacy Breakdown

SynapseTranslate prioritizes privacy by keeping heavy neural translation computation strictly on your device:

| Component | Execution Mode | Engine / Technology | Data Destination |
| :--- | :--- | :--- | :--- |
| **Neural Translation Engine** | **100% On-Device / Offline** | Argos Translate (OpenNMT + CTranslate2) | Zero text network traffic; runs locally on CPU |
| **Language Auto-Detection** | **100% On-Device / Offline** | `langdetect` (n-gram profile modeling) | Executed completely in local memory |
| **Indic & Marathi Bridge** | **100% On-Device / Offline** | Compiled Morphological Transfer Engine | Local single-pass tokenization & grammar bridge |
| **Voice Playback (TTS)** | **Hybrid** | `gTTS` (Primary) + `pyttsx3` (Offline Fallback) | Local system speech engine or web synthesis |
| **Voice Dictation (STT)** | **Cloud-Enhanced** | `SpeechRecognition` (Google Web Speech) | Microphone audio stream for multi-accent clarity |

> **Privacy Guarantee:** Disconnect your Wi-Fi after model setup and test translation — the entire core neural translation pipeline operates with 100% functionality without internet access. Voice dictation is an optional voice input feature.

---

## 💡 Marathi Translation Architecture & Technical Note

1. **Why an Indic Linguistic Bridge?**
   Argos Translate's official package index does not provide a standalone `mr` (Marathi) model. Standard small-footprint open-source models (such as `Helsinki-NLP/opus-mt-en-mr` trained on the biblical JW300 corpus) suffer from severe hallucinations on modern and technical vocabulary (e.g. translating "Artificial intelligence is good" into religious queries).
2. **The Synapse Solution:**
   Hindi and Marathi share the Devanagari script, Subject-Object-Verb (SOV) sentence order, and postpositional structures. SynapseTranslate routes English to Hindi via Argos Translate's high-accuracy neural model, followed by an extensive morphological, postpositional, and lexical transfer pipeline into idiomatic Marathi.
3. **Future Roadmap:**
   For enterprise scaling to full arbitrary colloquial literature, integrating larger multi-task foundation models like AI4Bharat's `IndicTrans2` (~1.1 GB) is planned as an optional download tier.

---

## ⚠️ Notes & Limitations
- **Direct vs. Pivot Routing:** Direct pairs (like English ↔ Hindi, English ↔ Spanish) provide the highest accuracy. For pairs where no direct model exists (e.g. Hindi ↔ Japanese), the engine routes through English as an intermediate pivot bridge.
- **Model Package Storage:** Neural model weights range between 40 MB to 120 MB per language pair. Ensure adequate disk space when downloading all language routes.


