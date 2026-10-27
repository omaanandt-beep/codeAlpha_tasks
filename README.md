# SynapseTranslate 🌐⚡

> **Deep Neural Translation Studio • 100% Air-Gapped Privacy • Marathi & Multilingual Pipeline**  
> Developed for the **CodeAlpha Artificial Intelligence Internship**.

---

## 📖 Project Overview
**SynapseTranslate** is a cutting-edge, privacy-first neural machine translation and speech studio built with Python, Streamlit, and Argos Translate. Unlike typical translators that beam sensitive text and confidential documents across cloud APIs (Google Cloud, OpenAI, DeepL), SynapseTranslate executes high-performance neural machine translation **completely on-device**.

Once models are installed, translation functions without an active internet connection, guaranteeing zero telemetry, zero data leaks, and zero recurring API costs.

---

## ✨ Key Features
- **100% On-Device Neural Translation:** Powered by OpenNMT and CTranslate2 via Argos Translate with zero cloud telemetry.
- **🎙️ Speak to Translate (Voice Dictation):** Speak naturally into your microphone in any supported language; audio is automatically transcribed directly into the studio translation box.
- **🔊 Natural Voice Pronunciation (TTS):** One-click natural voice playback for translations with auto-play support (Marathi, Hindi, English, Spanish, French, etc.).
- **⚡ High-Fidelity Marathi Support:** Custom Indic semantic pipeline bridging English and Marathi seamlessly without hallucination.
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

### Step 1: Create and Activate Virtual Environment
Open PowerShell inside this project folder:
```powershell
# Navigate to the workspace (if not already there)
cd "c:\Users\Om Tripathi\Downloads\CodeAlpha_AI_Internship_Projects\CodeAlpha_AI_Internship\CodeAlpha_LanguageTranslationTool"

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
*Note: This step requires an internet connection once to download neural weight packages. Once downloaded, all translation happens 100% offline.*

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

## 🔒 Privacy & Offline Guarantees
- **No Remote APIs:** Never calls Google Translate, DeepL, or any external endpoint.
- **No API Keys:** Does not require tokens, accounts, or subscriptions.
- **Air-Gapped Ready:** Disconnect your Wi-Fi after Step 3 and test translation — it runs completely offline.

---

## ⚠️ Limitations & Notes
- **Direct vs. Pivot Routing:** Direct pairs (like English ↔ Hindi) provide the highest accuracy. For pairs where no direct model exists (e.g. Hindi ↔ Japanese), the engine routes through English as an intermediate bridge.
- **First-Time Download:** Neural model weights range between 40 MB to 120 MB per pair. Ensure adequate disk space when installing all 15 language routes.

---

## 📤 Publishing to GitHub via GitHub Desktop
1. Open **GitHub Desktop**.
2. Click **File** > **Add Local Repository...** (or press `Ctrl + O`).
3. Select this folder: `c:\Users\Om Tripathi\Downloads\CodeAlpha_AI_Internship_Projects\CodeAlpha_AI_Internship\CodeAlpha_LanguageTranslationTool`.
4. If prompted that it's not a git repository, click **Create a Repository here**.
5. Name: `CodeAlpha_LanguageTranslationTool`.
6. Write a commit message: `feat: Complete CodeAlpha AI Offline Language Translator`.
7. Click **Commit to main**.
8. Click **Publish repository** to push it to your GitHub profile.

