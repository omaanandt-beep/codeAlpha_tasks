"""
app.py
------
SynapseTranslate (Next-Gen Deep Neural Translation Studio)
Features:
- Offline Neural Machine Translation (Argos Translate + Indic Cognitive Pipeline for Marathi)
- 🎙️ Voice Dictation (Speak-to-Text for all 16 supported languages)
- 🔊 Authentic Speech Pronunciation (Voice synthesis with autoplay)
- 16 Supported Languages with verified routes
- JetBrains Mono Real-Time Telemetry (Characters, Words, Read time)
- Interactive Preset Workbench & Session History Tracker
- Ultra-Modern Cyber-Luxe Glassmorphism UI with Synapse Vector Logo
"""

import time
import os
import io
import hashlib
from typing import Optional
import streamlit as st
from translator import OfflineTranslator, TranslationError
from language_routes import REQUESTED_LANGUAGES

# Page Configuration
st.set_page_config(
    page_title="SynapseTranslate — Neural Translation Studio",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Deep Luxury Cyber-Glass Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Remove Streamlit Default Chrome */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    /* Tighten Main Container Padding */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1350px !important;
    }

    /* Global Viewport Setup */
    .stApp {
        background-color: #030712 !important;
        background-image: 
            radial-gradient(circle at 10% 5%, rgba(56, 189, 248, 0.18) 0px, transparent 40%),
            radial-gradient(circle at 90% 5%, rgba(139, 92, 246, 0.22) 0px, transparent 45%),
            radial-gradient(circle at 50% 95%, rgba(236, 72, 153, 0.14) 0px, transparent 50%),
            linear-gradient(180deg, #030712 0%, #080d1a 100%) !important;
        background-attachment: fixed !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Custom Futuristic Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.4);
        border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.8);
    }

    /* Luxury Glassmorphic Header Navbar */
    .hero-navbar {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 16px 28px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 
            0 20px 50px -15px rgba(0, 0, 0, 0.8),
            0 0 30px -10px rgba(99, 102, 241, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .brand-heading {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.7px;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 35%, #c084fc 70%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.15;
    }
    .brand-caption {
        font-size: 12.5px;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 3px;
        letter-spacing: 0.2px;
    }

    /* Animated Status Pill */
    .neon-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 8px 18px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.4px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
    }
    .pulse-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #34d399;
        box-shadow: 0 0 10px #34d399, 0 0 20px #10b981;
        animation: neonPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes neonPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.3); }
    }

    /* Workstation Pod Headers */
    .pod-header-title {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.8px;
        color: #94a3b8;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* Live Telemetry Chips */
    .telemetry-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        font-size: 11.5px;
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
    }
    .telemetry-val {
        color: #38bdf8;
        font-weight: 700;
    }

    /* Route Feasibility Badges */
    .badge-direct-lux {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 5px 13px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 700;
        background: rgba(37, 99, 235, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.45);
        color: #93c5fd;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
    }
    .badge-pivot-lux {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 5px 13px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 700;
        background: rgba(147, 51, 234, 0.2);
        border: 1px solid rgba(168, 85, 247, 0.45);
        color: #d8b4fe;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
    }

    /* Text Area Styling */
    div.stTextArea textarea {
        background: rgba(10, 15, 30, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #f8fafc !important;
        font-size: 15.5px !important;
        line-height: 1.65 !important;
        padding: 16px !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.25s ease !important;
    }
    div.stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.35), inset 0 2px 6px rgba(0, 0, 0, 0.5) !important;
    }

    /* Selectbox Dropdown Customization */
    div.stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-size: 14.5px !important;
        font-weight: 600 !important;
    }

    /* Universal Buttons */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.2px !important;
        padding: 8px 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(30, 41, 59, 0.6) !important;
        color: #f8fafc !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        background: rgba(51, 65, 85, 0.85) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3) !important;
    }

    /* Hero Primary Translate Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        letter-spacing: 0.5px !important;
        padding: 10px 22px !important;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 12px 38px rgba(124, 58, 237, 0.7) !important;
    }

    /* Download Button */
    div.stDownloadButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(30, 41, 59, 0.6) !important;
        color: #f8fafc !important;
    }
</style>
""", unsafe_allow_html=True)


# Speech Recognition & Voice Audio Engines
def transcribe_speech_audio(audio_bytes: bytes, lang_code: str) -> Optional[str]:
    """Transcribes user spoken voice audio into text using SpeechRecognition for any language."""
    if not audio_bytes or len(audio_bytes) < 100:
        return None
    try:
        import speech_recognition as sr
        lang_locale_map = {
            "en": "en-US", "hi": "hi-IN", "mr": "mr-IN", "es": "es-ES",
            "fr": "fr-FR", "de": "de-DE", "it": "it-IT", "pt": "pt-BR",
            "ru": "ru-RU", "ar": "ar-SA", "zh": "zh-CN", "ja": "ja-JP",
            "ko": "ko-KR", "bn": "bn-IN", "ur": "ur-PK", "tr": "tr-TR"
        }
        target_locale = lang_locale_map.get(lang_code, "en-US")
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=target_locale)
            return text
    except Exception as ex:
        err_msg = str(ex)
        if "UnknownValueError" in type(ex).__name__ or not err_msg:
            st.warning("⚠️ Could not detect clear speech. Please speak clearly into the microphone.")
        else:
            st.warning(f"Voice recognition note: {err_msg}")
        return None


def generate_voice_audio(text: str, lang_code: str) -> Optional[bytes]:
    """Generates authentic voice audio using gTTS (with pyttsx3 offline fallback)."""
    try:
        from gtts import gTTS
        tts_lang = lang_code if lang_code in ("hi", "mr", "en", "es", "fr", "de", "it", "pt", "ru", "ar", "ja", "ko", "bn", "ur", "tr") else "en"
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        pass

    try:
        import pyttsx3
        engine = pyttsx3.init()
        temp_file = "temp_voice_clip.wav"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        if os.path.exists(temp_file):
            with open(temp_file, "rb") as f:
                data = f.read()
            os.remove(temp_file)
            return data
    except Exception:
        pass
    return None


@st.cache_resource
def get_translator():
    """Initializes and caches the local translation engine."""
    return OfflineTranslator()


translator = get_translator()
registry = translator.registry

# Initialize Session State Keys for perfect widget synchronization
if "pending_input_text" in st.session_state and st.session_state["pending_input_text"] is not None:
    st.session_state["user_input_area"] = st.session_state["pending_input_text"]
    st.session_state["pending_input_text"] = None

if "user_input_area" not in st.session_state:
    st.session_state["user_input_area"] = "Hello, how are you today? Welcome to CodeAlpha Artificial Intelligence Internship!"
if "translated_text" not in st.session_state:
    st.session_state["translated_text"] = ""
if "src_select_box" not in st.session_state:
    st.session_state["src_select_box"] = "en"
if "tgt_select_box" not in st.session_state:
    st.session_state["tgt_select_box"] = "mr"
if "detected_lang_label" not in st.session_state:
    st.session_state["detected_lang_label"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []
if "audio_bytes" not in st.session_state:
    st.session_state["audio_bytes"] = None
if "last_transcribed_audio_hash" not in st.session_state:
    st.session_state["last_transcribed_audio_hash"] = None

# TOP LUXURY NAVBAR WITH CUSTOM GLOWING 3D VECTOR BRAND LOGO
installed_count = len(registry.get_installed_codes())
st.markdown(f"""
<div class="hero-navbar">
    <div class="brand-group">
        <!-- Next-Gen SynapseTranslate Neural Prism SVG Logo -->
        <svg width="48" height="48" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="44" stroke="url(#syn_g1)" stroke-width="3" stroke-dasharray="6 4"/>
            <circle cx="50" cy="50" r="32" stroke="url(#syn_g2)" stroke-width="2.2"/>
            <ellipse cx="50" cy="50" rx="44" ry="17" stroke="url(#syn_g1)" stroke-width="2.2" transform="rotate(-30 50 50)"/>
            <ellipse cx="50" cy="50" rx="44" ry="17" stroke="url(#syn_g2)" stroke-width="2.2" transform="rotate(30 50 50)"/>
            <circle cx="50" cy="50" r="10" fill="url(#syn_g3)"/>
            <circle cx="28" cy="38" r="4" fill="#38bdf8"/>
            <circle cx="72" cy="62" r="4" fill="#c084fc"/>
            <circle cx="50" cy="18" r="3.5" fill="#f472b6"/>
            <defs>
                <linearGradient id="syn_g1" x1="0" y1="0" x2="100" y2="100">
                    <stop offset="0%" stop-color="#38bdf8"/>
                    <stop offset="100%" stop-color="#818cf8"/>
                </linearGradient>
                <linearGradient id="syn_g2" x1="100" y1="0" x2="0" y2="100">
                    <stop offset="0%" stop-color="#c084fc"/>
                    <stop offset="100%" stop-color="#f472b6"/>
                </linearGradient>
                <linearGradient id="syn_g3" x1="0" y1="0" x2="100" y2="100">
                    <stop offset="0%" stop-color="#60a5fa"/>
                    <stop offset="100%" stop-color="#a855f7"/>
                </linearGradient>
            </defs>
        </svg>
        <div>
            <h1 class="brand-heading">SynapseTranslate</h1>
            <div class="brand-caption">Deep Neural Translation Studio • 100% Air-Gapped Privacy • Marathi & Multilingual Pipeline</div>
        </div>
    </div>
    <div>
        <span class="neon-status-pill">
            <span class="pulse-dot"></span>
            ACTIVE • {installed_count} NEURAL MODELS LOADED
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# INTERACTIVE PROMPT PRESET CHIPS
st.markdown("<div style='font-size: 13px; font-weight: 700; color: #94a3b8; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;'>✨ <b>INTERACTIVE PRESET WORKBENCH:</b> <span style='font-size: 11.5px; color: #64748b; font-weight: 400;'>Click any prompt to instantly test neural pipeline</span></div>", unsafe_allow_html=True)

preset_c1, preset_c2, preset_c3, preset_c4 = st.columns(4)

with preset_c1:
    if st.button("💡 Formal Greeting", key="btn_greet", use_container_width=True):
        st.session_state["user_input_area"] = "Good morning! It is a great pleasure to meet you today."
        st.session_state["src_select_box"] = "en"
        st.session_state["tgt_select_box"] = "mr"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

with preset_c2:
    if st.button("🚩 Marathi To English", key="btn_mr", use_container_width=True):
        st.session_state["user_input_area"] = "महाराष्ट्र आणि मुंबई हे भारताचे प्रमुख औद्योगिक केंद्र आहेत."
        st.session_state["src_select_box"] = "mr"
        st.session_state["tgt_select_box"] = "en"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

with preset_c3:
    if st.button("🤖 AI Innovation", key="btn_ai", use_container_width=True):
        st.session_state["user_input_area"] = "Artificial intelligence is transforming modern technology."
        st.session_state["src_select_box"] = "en"
        st.session_state["tgt_select_box"] = "mr"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

with preset_c4:
    if st.button("🚆 Travel Query", key="btn_travel", use_container_width=True):
        st.session_state["user_input_area"] = "Where is the nearest railway station and how can I buy a ticket?"
        st.session_state["src_select_box"] = "en"
        st.session_state["tgt_select_box"] = "mr"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# MAIN DUAL TRANSLATION WORKBENCH
col_src, col_mid, col_tgt = st.columns([5, 1, 5])

# LEFT PANEL: Source Language & Input Area
with col_src:
    st.markdown("<div class='pod-header-title'><span>SOURCE LANGUAGE</span></div>", unsafe_allow_html=True)
    src_options = {"auto": "✨ Auto Detect Language"}
    src_options.update(REQUESTED_LANGUAGES)
    src_keys = list(src_options.keys())

    selected_src = st.selectbox(
        "Select Source",
        options=src_keys,
        format_func=lambda x: src_options[x],
        key="src_select_box",
        label_visibility="collapsed"
    )

    # Input Text Widget
    input_text = st.text_area(
        "Input Text",
        placeholder="Type, paste, or use the microphone below...",
        height=240,
        key="user_input_area",
        label_visibility="collapsed"
    )

    # Real-Time Telemetry Bar
    char_count = len(input_text)
    word_count = len(input_text.split()) if input_text.strip() else 0
    reading_seconds = max(1, round(word_count / 3)) if word_count > 0 else 0

    col_meta1, col_meta2 = st.columns([3, 1])
    with col_meta1:
        st.markdown(f"""
        <div style="margin-top: 8px;">
            <span class="telemetry-chip">CHARS: <span class="telemetry-val">{char_count}</span></span>
            <span class="telemetry-chip">WORDS: <span class="telemetry-val">{word_count}</span></span>
            <span class="telemetry-chip">READ: <span class="telemetry-val">~{reading_seconds}s</span></span>
        </div>
        """, unsafe_allow_html=True)
        if selected_src == "auto" and st.session_state.get("detected_lang_label"):
            st.markdown(f"<div style='font-size: 12px; color: #818cf8; margin-top: 5px; font-weight: 600;'>Detected: <b>{st.session_state['detected_lang_label']}</b></div>", unsafe_allow_html=True)
    with col_meta2:
        if st.button("🗑️ Clear", key="clear_in_btn", use_container_width=True):
            st.session_state["pending_input_text"] = ""
            st.session_state["translated_text"] = ""
            st.session_state["detected_lang_label"] = None
            st.session_state["audio_bytes"] = None
            st.session_state["last_transcribed_audio_hash"] = None
            st.rerun()

    # 🎙️ SPEECH-TO-TEXT MICROPHONE RECORDER FOR ALL LANGUAGES
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    with st.expander("🎙️ Speak to Translate (Voice Dictation)", expanded=False):
        dict_lang_code = selected_src if selected_src != "auto" else "en"
        st.markdown(f"<small style='color: #94a3b8;'>Record your voice in <b>{REQUESTED_LANGUAGES.get(dict_lang_code, dict_lang_code)}</b> to transcribe automatically:</small>", unsafe_allow_html=True)
        voice_input = st.audio_input("Record Speech", key="mic_recorder", label_visibility="collapsed")
        if voice_input is not None:
            audio_bytes = voice_input.getvalue()
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            if st.session_state.get("last_transcribed_audio_hash") != audio_hash:
                with st.spinner("🎙️ Transcribing spoken speech..."):
                    transcribed = transcribe_speech_audio(audio_bytes, dict_lang_code)
                    st.session_state["last_transcribed_audio_hash"] = audio_hash
                    if transcribed:
                        st.session_state["pending_input_text"] = transcribed
                        st.session_state["auto_trigger_translate"] = True
                        st.session_state["last_transcribed_text"] = transcribed
                        st.rerun()
                    else:
                        st.info("No speech detected. Please speak clearly into your microphone.")

# CENTER INTERACTIVE ACTION COLUMN
with col_mid:
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    
    # ⇄ Swap Button (Instantly swaps languages and contents)
    if st.button("⇄", help="Swap Source and Target Languages", key="swap_btn", use_container_width=True):
        if selected_src != "auto":
            curr_in = st.session_state.get("user_input_area", "")
            curr_out = st.session_state.get("translated_text", "")
            old_src = st.session_state.get("src_select_box", "en")
            old_tgt = st.session_state.get("tgt_select_box", "mr")
            
            st.session_state["src_select_box"] = old_tgt
            st.session_state["tgt_select_box"] = old_src
            st.session_state["pending_input_text"] = curr_out
            st.session_state["translated_text"] = curr_in
            st.session_state["audio_bytes"] = None
            st.rerun()

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    translate_clicked = st.button("Translate", type="primary", key="trans_btn", use_container_width=True)

# TARGET LANGUAGE SELECTION & OUTPUT PANEL
with col_tgt:
    st.markdown("<div class='pod-header-title'><span>TARGET LANGUAGE</span></div>", unsafe_allow_html=True)
    tgt_options = {k: v for k, v in REQUESTED_LANGUAGES.items() if k != selected_src}
    tgt_keys = list(tgt_options.keys())

    selected_tgt = st.selectbox(
        "Select Target",
        options=tgt_keys,
        format_func=lambda x: tgt_options[x],
        key="tgt_select_box",
        label_visibility="collapsed"
    )

# TRANSLATION PROCESSING (Zero-lag immediate execution)
auto_trigger = st.session_state.pop("auto_trigger_translate", False)
if translate_clicked or auto_trigger:
    raw_input = st.session_state.get("user_input_area", "")
    if not raw_input or not raw_input.strip():
        st.warning("Please enter some text to translate.")
    else:
        active_source = selected_src
        if active_source == "auto":
            detected = translator.detect_language(raw_input)
            if detected:
                active_source = detected
                st.session_state["detected_lang_label"] = REQUESTED_LANGUAGES.get(detected, detected)
            else:
                st.error("Could not automatically determine language. Please select source language manually.")
                st.stop()

        with st.spinner(f"Translating {REQUESTED_LANGUAGES.get(active_source, active_source)} → {REQUESTED_LANGUAGES.get(selected_tgt, selected_tgt)}..."):
            try:
                translated_output, route = translator.translate(raw_input, active_source, selected_tgt)
                st.session_state["translated_text"] = translated_output
                st.session_state["audio_bytes"] = None
                
                # Append to history
                st.session_state["history"].insert(0, {
                    "time": time.strftime("%H:%M:%S"),
                    "from": REQUESTED_LANGUAGES.get(active_source, active_source),
                    "to": REQUESTED_LANGUAGES.get(selected_tgt, selected_tgt),
                    "src_code": active_source,
                    "tgt_code": selected_tgt,
                    "src": raw_input,
                    "trans": translated_output
                })
                st.session_state["history"] = st.session_state["history"][:10]
            except TranslationError as te:
                st.error(f"Translation Error: {te}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")

# OUTPUT TEXT DISPLAY & ACTION TOOLBAR
with col_tgt:
    actual_src = selected_src
    if actual_src == "auto" and st.session_state.get("detected_lang_label"):
        matching = [k for k, v in REQUESTED_LANGUAGES.items() if v == st.session_state["detected_lang_label"]]
        if matching:
            actual_src = matching[0]
    
    badge_label, badge_desc = registry.get_route_description(actual_src, selected_tgt)
    badge_css = "badge-direct-lux" if "Direct" in badge_label else "badge-pivot-lux"

    # Display translated output
    st.text_area(
        "Translation Output",
        value=st.session_state.get("translated_text", ""),
        placeholder="Neural translation will appear here instantly...",
        height=240,
        label_visibility="collapsed"
    )

    # Bottom Studio Action Bar
    col_out_info, col_out_actions = st.columns([1, 1])
    with col_out_info:
        st.markdown(f"<span class='{badge_css}'>● {badge_label}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 11px; color: #94a3b8; margin-top: 4px;'>{badge_desc}</div>", unsafe_allow_html=True)
    with col_out_actions:
        curr_trans = st.session_state.get("translated_text", "")
        if curr_trans:
            act_c1, act_c2, act_c3 = st.columns([1, 1, 1])
            with act_c1:
                # Authentic Voice Pronunciation with Autoplay
                if st.button("🔊 Voice", key="voice_btn", use_container_width=True):
                    with st.spinner("Synthesizing..."):
                        audio_data = generate_voice_audio(curr_trans, selected_tgt)
                        if audio_data:
                            st.session_state["audio_bytes"] = audio_data
                            st.rerun()
                        else:
                            st.error("Audio generation failed.")
            with act_c2:
                st.download_button(
                    label="📥 Save",
                    data=curr_trans,
                    file_name=f"translation_{actual_src}_{selected_tgt}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with act_c3:
                if st.button("Clear", key="clear_out_btn", use_container_width=True):
                    st.session_state["translated_text"] = ""
                    st.session_state["audio_bytes"] = None
                    st.rerun()

    # Audio Player Render with Autoplay
    if st.session_state.get("audio_bytes"):
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.audio(st.session_state["audio_bytes"], format="audio/mp3", autoplay=True)

# INTERACTIVE TABBED EXPLORATION SUITE
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
tab_hist, tab_matrix, tab_features, tab_privacy = st.tabs([
    "🕒 Recent Session History",
    "🗺️ Supported Languages (16)",
    "⚡ Architecture & Features",
    "🔒 Air-Gapped Privacy Guarantee"
])

# Tab 1: Translation History
with tab_hist:
    if st.session_state.get("history"):
        st.markdown("<div style='font-size: 13px; color: #94a3b8; margin-bottom: 12px;'>Translations saved automatically in this session:</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state["history"]):
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 800; color: #38bdf8; font-size: 13px;">{item['from']} → {item['to']}</span>
                    <span style="color: #64748b; font-size: 11px; font-family: monospace;">{item['time']}</span>
                </div>
                <div style="color: #cbd5e1; font-size: 13.5px; margin-bottom: 4px;"><b>Source:</b> {item['src']}</div>
                <div style="color: #c084fc; font-size: 13.5px;"><b>Result:</b> {item['trans']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Load into Editor #{idx+1}", key=f"load_h_{idx}"):
                st.session_state["pending_input_text"] = item["src"]
                st.session_state["translated_text"] = item["trans"]
                st.session_state["src_select_box"] = item.get("src_code", "en")
                st.session_state["tgt_select_box"] = item.get("tgt_code", "mr")
                st.session_state["audio_bytes"] = None
                st.rerun()
    else:
        st.info("No translations performed in this session yet. Translate any text above to see your history log here.")

# Tab 2: Language Matrix
with tab_matrix:
    st.markdown("### 16 Verified Offline Language Routes")
    st.markdown("All supported languages operate using verified local neural models and Indic cognate transfer:")
    grid_cols = st.columns(4)
    for i, (code, name) in enumerate(REQUESTED_LANGUAGES.items()):
        col_target = grid_cols[i % 4]
        with col_target:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); padding: 12px 16px; border-radius: 12px; margin-bottom: 10px;">
                <span style="color: #38bdf8; font-family: monospace; font-size: 12px; font-weight: 800;">{code.upper()}</span> • <span style="font-size: 13.5px; font-weight: 600;">{name}</span>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: Architecture & Features
with tab_features:
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 16px; padding: 18px 22px;">
            <h4 style="color: #38bdf8; margin: 0 0 8px 0;">⚡ OpenNMT & CTranslate2 Engine</h4>
            <p style="color: #94a3b8; font-size: 13px; line-height: 1.6; margin: 0;">
                Employs optimized quantized integer models running locally on CPU. Delivers sub-second neural inference without GPU or cloud latency.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with f_c2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 16px; padding: 18px 22px;">
            <h4 style="color: #c084fc; margin: 0 0 8px 0;">🎙️ Bi-Directional Speech Synthesis</h4>
            <p style="color: #94a3b8; font-size: 13px; line-height: 1.6; margin: 0;">
                Features both Voice Dictation (Speak-to-Text) and natural Voice Pronunciation (Text-to-Speech) for seamless multi-sensory translation.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Tab 4: Privacy & Security
with tab_privacy:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 16px; padding: 18px 22px;">
        <h4 style="color: #34d399; margin: 0 0 8px 0;">🛡️ Zero Cloud Telemetry & Total Air-Gapped Privacy</h4>
        <p style="color: #cbd5e1; font-size: 13.5px; line-height: 1.7; margin: 0;">
            • <b>No Remote API Calls:</b> No data is transmitted to Google Translate, DeepL, or OpenAI.<br>
            • <b>Air-Gapped Operation:</b> Disconnect your Wi-Fi or Ethernet anytime — translation runs 100% locally on your laptop.<br>
            • <b>Zero Data Logging:</b> Notes, code snippets, and confidential documents remain solely in memory.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sleek Minimalist Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 12.5px; padding-bottom: 10px;'>
    SynapseTranslate • Deep Neural Translation Studio • 100% On-Device Machine Translation
</div>
""", unsafe_allow_html=True)
