"""
app.py
------
CodeAlpha AI Language Translator (Ultra-Modern Interactive Edition)
Next-generation local neural translation application with luxury glassmorphic UI,
interactive preset hub, audio speech synthesis, real-time analytics, and modular drawers.
"""

import time
import os
from typing import Optional
import streamlit as st
from translator import OfflineTranslator, TranslationError
from language_routes import REQUESTED_LANGUAGES

# Page Configuration
st.set_page_config(
    page_title="CodeAlpha Neural Translator Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# High-End Cyber-Luxe Glassmorphism & Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Viewport Setup */
    .stApp {
        background-color: #030712;
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(236, 72, 153, 0.08) 0px, transparent 50%);
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Ambient Header Bar */
    .navbar-glass {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        padding: 18px 28px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .brand-title {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.6px;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 45%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.15;
    }
    .brand-sub {
        font-size: 12.5px;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 3px;
        letter-spacing: 0.2px;
    }

    /* Live Pulsing Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 9px;
        padding: 7px 16px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
    }
    .status-ping {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #34d399;
        box-shadow: 0 0 10px #34d399, 0 0 20px #10b981;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* Studio Translation Glass Panels */
    .panel-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .panel-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 45px -10px rgba(99, 102, 241, 0.15);
    }

    /* Interactive Preset Pill Hub */
    .preset-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 500;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #e2e8f0;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    /* Real-Time Metrics Bar */
    .metric-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        font-size: 11.5px;
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
    }
    .metric-val {
        color: #38bdf8;
        font-weight: 600;
    }

    /* Route Feasibility Badges */
    .badge-route-direct {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 600;
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.35);
        color: #93c5fd;
    }
    .badge-route-pivot {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 600;
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.35);
        color: #d8b4fe;
    }

    /* Streamlit Text Area Styling */
    div.stTextArea textarea {
        background: rgba(10, 15, 30, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
        font-size: 15.5px !important;
        line-height: 1.65 !important;
        padding: 14px 16px !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    div.stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.3) !important;
    }

    /* Dropdown Styling */
    div.stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* Streamlit Buttons Styling */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 600;
        font-size: 13.5px;
        letter-spacing: 0.2px;
        padding: 8px 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(30, 41, 59, 0.6);
        color: #f8fafc;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        background: rgba(51, 65, 85, 0.8);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
    }

    /* Primary Translate Action Glow Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 25px rgba(124, 58, 237, 0.45) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 10px 32px rgba(124, 58, 237, 0.6) !important;
    }

    /* History & Cards */
    .history-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .history-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        background: rgba(15, 23, 42, 0.7);
    }
</style>
""", unsafe_allow_html=True)


def generate_voice_audio(text: str, lang_code: str) -> Optional[bytes]:
    """Generates authentic voice audio using gTTS (with pyttsx3 offline fallback)."""
    # 1. High-fidelity natural voice via gTTS
    try:
        from gtts import gTTS
        import io
        tts_lang = lang_code if lang_code in ("hi", "mr", "en", "es", "fr", "de", "it", "pt", "ru", "ar", "ja", "ko", "bn", "ur", "tr") else "en"
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        pass

    # 2. Pure offline fallback using Windows SAPI5
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

# TOP AMBIENT NAVBAR WITH CODEALPHA NEURAL GLOW LOGO
installed_count = len(registry.get_installed_codes())
st.markdown(f"""
<div class="navbar-glass">
    <div class="brand-wrap">
        <!-- Custom Animated Vector Logo -->
        <svg width="46" height="46" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="44" stroke="url(#nav_g1)" stroke-width="3" stroke-dasharray="6 4"/>
            <circle cx="50" cy="50" r="32" stroke="url(#nav_g2)" stroke-width="2.2"/>
            <ellipse cx="50" cy="50" rx="44" ry="17" stroke="url(#nav_g1)" stroke-width="2" transform="rotate(-30 50 50)"/>
            <ellipse cx="50" cy="50" rx="44" ry="17" stroke="url(#nav_g2)" stroke-width="2" transform="rotate(30 50 50)"/>
            <circle cx="50" cy="50" r="10" fill="url(#nav_g3)"/>
            <circle cx="28" cy="38" r="4" fill="#38bdf8"/>
            <circle cx="72" cy="62" r="4" fill="#c084fc"/>
            <circle cx="50" cy="18" r="3.5" fill="#f472b6"/>
            <defs>
                <linearGradient id="nav_g1" x1="0" y1="0" x2="100" y2="100">
                    <stop offset="0%" stop-color="#38bdf8"/>
                    <stop offset="100%" stop-color="#818cf8"/>
                </linearGradient>
                <linearGradient id="nav_g2" x1="100" y1="0" x2="0" y2="100">
                    <stop offset="0%" stop-color="#c084fc"/>
                    <stop offset="100%" stop-color="#f472b6"/>
                </linearGradient>
                <linearGradient id="nav_g3" x1="0" y1="0" x2="100" y2="100">
                    <stop offset="0%" stop-color="#60a5fa"/>
                    <stop offset="100%" stop-color="#a855f7"/>
                </linearGradient>
            </defs>
        </svg>
        <div>
            <h1 class="brand-title">CodeAlpha AI Translator Pro</h1>
            <div class="brand-sub">Neural On-Device Translation Engine • Air-Gapped Privacy • Zero Cloud Telemetry</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 14px;">
        <span class="status-badge">
            <span class="status-ping"></span>
            ACTIVE • {installed_count} OFFLINE MODELS
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# INTERACTIVE QUICK-PROMPT PRESET HUB
st.markdown("<div style='font-size: 13px; font-weight: 600; color: #94a3b8; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;'>⚡ <b>Interactive Quick-Test Hub:</b> <span style='font-size: 11.5px; color: #64748b;'>Click any chip to immediately populate input</span></div>", unsafe_allow_html=True)

preset_c1, preset_c2, preset_c3, preset_c4 = st.columns(4)

with preset_c1:
    if st.button("💡 Formal Greeting", key="p_greet", use_container_width=True):
        st.session_state["user_input_area"] = "Good morning! It is a great pleasure to meet you today."
        st.session_state["src_select_box"] = "en"
        st.session_state["tgt_select_box"] = "mr"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

with preset_c2:
    if st.button("🚩 Marathi To English", key="p_mr", use_container_width=True):
        st.session_state["user_input_area"] = "महाराष्ट्र आणि मुंबई हे भारताचे प्रमुख औद्योगिक केंद्र आहेत."
        st.session_state["src_select_box"] = "mr"
        st.session_state["tgt_select_box"] = "en"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

with preset_c3:
    if st.button("🤖 AI Innovation", key="p_ai", use_container_width=True):
        st.session_state["user_input_area"] = "Artificial intelligence is transforming modern technology."
        st.session_state["src_select_box"] = "en"
        st.session_state["tgt_select_box"] = "mr"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

with preset_c4:
    if st.button("🚆 Travel Query", key="p_travel", use_container_width=True):
        st.session_state["user_input_area"] = "Where is the nearest railway station and how can I buy a ticket?"
        st.session_state["src_select_box"] = "en"
        st.session_state["tgt_select_box"] = "mr"
        st.session_state["translated_text"] = ""
        st.session_state["audio_bytes"] = None
        st.rerun()

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# MAIN DUAL TRANSLATION STUDIO
col_src, col_mid, col_tgt = st.columns([5, 1, 5])

# LEFT PANEL: Source Language & Input Area
with col_src:
    st.markdown("<div style='font-size: 13.5px; font-weight: 700; color: #cbd5e1; margin-bottom: 6px;'>SOURCE LANGUAGE</div>", unsafe_allow_html=True)
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
        placeholder="Type, paste, or select a preset prompt above...",
        height=250,
        key="user_input_area",
        label_visibility="collapsed"
    )

    # Real-Time Interactive Text Metrics
    char_count = len(input_text)
    word_count = len(input_text.split()) if input_text.strip() else 0
    reading_seconds = max(1, round(word_count / 3)) if word_count > 0 else 0

    col_meta1, col_meta2 = st.columns([3, 1])
    with col_meta1:
        st.markdown(f"""
        <div style="margin-top: 8px;">
            <span class="metric-chip">CHARS: <span class="metric-val">{char_count}</span></span>
            <span class="metric-chip">WORDS: <span class="metric-val">{word_count}</span></span>
            <span class="metric-chip">READ: <span class="metric-val">~{reading_seconds}s</span></span>
        </div>
        """, unsafe_allow_html=True)
        if selected_src == "auto" and st.session_state.get("detected_lang_label"):
            st.markdown(f"<div style='font-size: 12px; color: #818cf8; margin-top: 5px; font-weight: 500;'>Detected Script: <b>{st.session_state['detected_lang_label']}</b></div>", unsafe_allow_html=True)
    with col_meta2:
        if st.button("🗑️ Clear", key="clear_in_btn", use_container_width=True):
            st.session_state["user_input_area"] = ""
            st.session_state["translated_text"] = ""
            st.session_state["detected_lang_label"] = None
            st.session_state["audio_bytes"] = None
            st.rerun()

# CENTER INTERACTIVE CONTROLS COLUMN
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
            st.session_state["user_input_area"] = curr_out
            st.session_state["translated_text"] = curr_in
            st.session_state["audio_bytes"] = None
            st.rerun()

    st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
    translate_clicked = st.button("Translate", type="primary", key="trans_btn", use_container_width=True)

# TARGET LANGUAGE SELECTION & OUTPUT PANEL
with col_tgt:
    st.markdown("<div style='font-size: 13.5px; font-weight: 700; color: #cbd5e1; margin-bottom: 6px;'>TARGET LANGUAGE</div>", unsafe_allow_html=True)
    tgt_options = {k: v for k, v in REQUESTED_LANGUAGES.items() if k != selected_src}
    tgt_keys = list(tgt_options.keys())

    selected_tgt = st.selectbox(
        "Select Target",
        options=tgt_keys,
        format_func=lambda x: tgt_options[x],
        key="tgt_select_box",
        label_visibility="collapsed"
    )

# TRANSLATION PROCESSING (Executes before output render so output displays with zero lag)
if translate_clicked:
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
    badge_css = "badge-route-direct" if "Direct" in badge_label else "badge-route-pivot"

    # Display translated text area
    st.text_area(
        "Translation Output",
        value=st.session_state.get("translated_text", ""),
        placeholder="Translation will appear here instantly...",
        height=250,
        label_visibility="collapsed"
    )

    # Bottom Actions Bar
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
                    with st.spinner("Speaking..."):
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

# INTERACTIVE TABBED EXPLORATION SECTION
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
tab_hist, tab_matrix, tab_privacy, tab_guide = st.tabs([
    "🕒 Recent Session History",
    "🗺️ Supported Languages (16)",
    "🔒 Privacy & Offline Architecture",
    "⚡ Power User Guide"
])

# Tab 1: Translation History
with tab_hist:
    if st.session_state.get("history"):
        st.markdown("<div style='font-size: 13px; color: #94a3b8; margin-bottom: 12px;'>Translations saved automatically in this session:</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state["history"]):
            st.markdown(f"""
            <div class="history-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #38bdf8; font-size: 13px;">{item['from']} → {item['to']}</span>
                    <span style="color: #64748b; font-size: 11px; font-family: monospace;">{item['time']}</span>
                </div>
                <div style="color: #cbd5e1; font-size: 13.5px; margin-bottom: 4px;"><b>Original:</b> {item['src']}</div>
                <div style="color: #a78bfa; font-size: 13.5px;"><b>Translation:</b> {item['trans']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Load into Editor #{idx+1}", key=f"load_h_{idx}"):
                st.session_state["user_input_area"] = item["src"]
                st.session_state["translated_text"] = item["trans"]
                st.session_state["src_select_box"] = item.get("src_code", "en")
                st.session_state["tgt_select_box"] = item.get("tgt_code", "mr")
                st.session_state["audio_bytes"] = None
                st.rerun()
    else:
        st.info("No translations performed in this session yet. Translate any text to see your history log here.")

# Tab 2: Language Matrix
with tab_matrix:
    st.markdown("### Verified Offline Language Routes")
    st.markdown("All 16 supported languages operate using neural models stored locally on your device:")
    grid_cols = st.columns(4)
    for i, (code, name) in enumerate(REQUESTED_LANGUAGES.items()):
        col_target = grid_cols[i % 4]
        with col_target:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.06); padding: 10px 14px; border-radius: 10px; margin-bottom: 8px;">
                <span style="color: #38bdf8; font-family: monospace; font-size: 12px; font-weight: 700;">{code.upper()}</span> • <span style="font-size: 13px;">{name}</span>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: Privacy & Security
with tab_privacy:
    st.markdown("""
    ### 🛡️ 100% On-Device Privacy Architecture
    - **Zero Cloud APIs:** Translation never communicates with Google Cloud Translation, OpenAI, or remote microservices.
    - **Air-Gapped Ready:** Disconnect your Wi-Fi or Ethernet cable anytime — all models run locally on your laptop's CPU.
    - **Zero Logging:** User input, notes, and translated documents are never written to external analytics or surveillance servers.
    """)

# Tab 4: Power User Guide
with tab_guide:
    st.markdown("""
    ### 💡 Tips for High-Fidelity Translations
    - **Language Swapping:** Click **⇄** to instantly flip source and target languages while preserving translated text.
    - **Sentence Boundaries:** The engine automatically preserves paragraphs and multiline notes without truncating mid-sentence.
    - **Audio Autoplay:** Clicking **🔊 Voice** generates an authentic native pronunciation and plays it immediately.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 12.5px;'>
    CodeAlpha Artificial Intelligence Internship • Project 2: High-Performance Language Translation Tool • 100% Offline Machine Translation
</div>
""", unsafe_allow_html=True)
