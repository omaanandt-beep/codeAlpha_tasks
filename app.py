"""
app.py
------
CodeAlpha AI Language Translator (Premium Edition)
Features:
- Offline Neural Machine Translation (Argos Translate + Opus-MT for Marathi)
- 16 Supported Languages (including Marathi, Hindi, English, Spanish, etc.)
- Voice Audio Speech Synthesis (Web Speech API)
- Real-time Word, Character & Reading-Time Analytics
- One-Click Sample Templates & Preset Prompts
- Instant File Download (.txt) & Clipboard Integration
- Local Session History Tracker
"""

import time
import streamlit as st
import streamlit.components.v1 as components
from translator import OfflineTranslator, TranslationError
from language_routes import REQUESTED_LANGUAGES

# Page Configuration
st.set_page_config(
    page_title="CodeAlpha Language Translator Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Premium Modern Glassmorphism Styling
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #111827 0%, #030712 100%);
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Sleek Glow Header Card */
    .header-card {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(75, 85, 99, 0.3);
        backdrop-filter: blur(16px);
        padding: 22px 30px;
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .header-subtitle {
        color: #9ca3af;
        font-size: 13px;
        margin-top: 4px;
        font-weight: 400;
    }

    /* Live Engine Status Badge */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #34d399;
        box-shadow: 0 0 8px #34d399;
    }

    /* Metrics Bar */
    .metric-badge {
        display: inline-block;
        padding: 3px 8px;
        background: rgba(31, 41, 55, 0.7);
        border: 1px solid rgba(75, 85, 99, 0.4);
        border-radius: 6px;
        font-size: 12px;
        color: #cbd5e1;
        margin-right: 6px;
    }

    /* Route Badges */
    .badge-route {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }
    .badge-direct {
        background: rgba(37, 99, 235, 0.25);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }
    .badge-pivot {
        background: rgba(147, 51, 234, 0.25);
        color: #d8b4fe;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }

    /* Streamlit Widget Polishing */
    div.stTextArea textarea {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid rgba(75, 85, 99, 0.4) !important;
        border-radius: 12px !important;
        color: #f9fafb !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    div.stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25) !important;
    }
    div.stSelectbox > div > div {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid rgba(75, 85, 99, 0.4) !important;
        border-radius: 10px !important;
        color: #f3f4f6 !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
    }
</style>
""", unsafe_allow_html=True)


def play_speech_js(text: str, lang_code: str):
    """Executes offline Web Speech API directly in the user's browser."""
    lang_map = {
        "en": "en-US", "hi": "hi-IN", "mr": "mr-IN", "es": "es-ES",
        "fr": "fr-FR", "de": "de-DE", "it": "it-IT", "pt": "pt-BR",
        "ru": "ru-RU", "ar": "ar-SA", "zh": "zh-CN", "ja": "ja-JP",
        "ko": "ko-KR", "bn": "bn-IN", "ur": "ur-PK", "tr": "tr-TR"
    }
    voice_locale = lang_map.get(lang_code, "en-US")
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance('{clean_text}');
            utterance.lang = '{voice_locale}';
            utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """
    components.html(js_code, height=0)


@st.cache_resource
def get_translator():
    """Initializes and caches the local translation engine."""
    return OfflineTranslator()


translator = get_translator()
registry = translator.registry

# Initialize Session State
if "source_text" not in st.session_state:
    st.session_state.source_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "en"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "hi"
if "detected_lang_label" not in st.session_state:
    st.session_state.detected_lang_label = None
if "history" not in st.session_state:
    st.session_state.history = []
if "play_audio" not in st.session_state:
    st.session_state.play_audio = None

# Trigger Audio Playback if requested
if st.session_state.play_audio:
    play_text, play_lang = st.session_state.play_audio
    play_speech_js(play_text, play_lang)
    st.session_state.play_audio = None

# Header Section
installed_count = len(registry.get_installed_codes())
st.markdown(f"""
<div class="header-card">
    <div>
        <h1 class="header-title">CodeAlpha AI Language Translator Pro</h1>
        <div class="header-subtitle">100% On-Device Neural Machine Translation • Marathi & Indic Support • Air-Gapped Privacy</div>
    </div>
    <div>
        <span class="status-pill">
            <span class="status-dot"></span>
            Engine Ready ({installed_count} Languages)
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Preset Sample Chips
st.markdown("<div style='font-size: 13px; color: #94a3b8; margin-bottom: 8px;'>✨ <b>Quick Test Presets:</b></div>", unsafe_allow_html=True)
chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
with chip_col1:
    if st.button("💡 Formal Greeting", use_container_width=True):
        st.session_state.source_text = "Good morning! It is a true pleasure to meet you today."
        st.session_state.source_lang = "en"
        st.rerun()
with chip_col2:
    if st.button("🚩 Marathi Test", use_container_width=True):
        st.session_state.source_text = "महाराष्ट्र आणि मुंबई हे भारताचे प्रमुख औद्योगिक केंद्र आहेत."
        st.session_state.source_lang = "mr"
        st.session_state.target_lang = "hi"
        st.rerun()
with chip_col3:
    if st.button("🤖 AI Innovation", use_container_width=True):
        st.session_state.source_text = "Artificial intelligence and neural machine translation are advancing rapidly."
        st.session_state.source_lang = "en"
        st.session_state.target_lang = "mr"
        st.rerun()
with chip_col4:
    if st.button("🚆 Travel Query", use_container_width=True):
        st.session_state.source_text = "Where is the nearest railway station and how can I get a ticket?"
        st.session_state.source_lang = "en"
        st.session_state.target_lang = "hi"
        st.rerun()

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Main Translation Grid
col_src, col_mid, col_tgt = st.columns([5, 1, 5])

# LEFT PANEL: Source Language & Input
with col_src:
    st.markdown("##### Source Language")
    src_options = {"auto": "Detect Language (Auto)"}
    src_options.update(REQUESTED_LANGUAGES)

    current_src = st.session_state.source_lang
    src_keys = list(src_options.keys())
    src_idx = src_keys.index(current_src) if current_src in src_keys else 0

    selected_src = st.selectbox(
        "Select Source",
        options=src_keys,
        format_func=lambda x: src_options[x],
        index=src_idx,
        key="src_select_box",
        label_visibility="collapsed"
    )
    st.session_state.source_lang = selected_src

    input_text = st.text_area(
        "Input Text",
        value=st.session_state.source_text,
        placeholder="Type or paste sentences, notes, paragraphs, or messages here...",
        height=240,
        key="input_text_widget",
        label_visibility="collapsed"
    )
    st.session_state.source_text = input_text

    # Metrics & Character Analytics
    char_count = len(input_text)
    word_count = len(input_text.split()) if input_text.strip() else 0
    reading_seconds = max(1, round(word_count / 3)) if word_count > 0 else 0

    col_sc1, col_sc2 = st.columns([2, 1])
    with col_sc1:
        st.markdown(f"""
        <div style="margin-top: 6px;">
            <span class="metric-badge">Chars: <b>{char_count}</b></span>
            <span class="metric-badge">Words: <b>{word_count}</b></span>
            <span class="metric-badge">Read: <b>~{reading_seconds}s</b></span>
        </div>
        """, unsafe_allow_html=True)
        if selected_src == "auto" and st.session_state.detected_lang_label:
            st.markdown(f"<div style='font-size:12px; color:#a5b4fc; margin-top:4px;'>Detected: <b>{st.session_state.detected_lang_label}</b></div>", unsafe_allow_html=True)
    with col_sc2:
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            if st.button("🔊 Listen", key="listen_src_btn", use_container_width=True):
                if input_text.strip():
                    src_code = selected_src if selected_src != "auto" else "en"
                    st.session_state.play_audio = (input_text, src_code)
                    st.rerun()
        with col_c2:
            if st.button("Clear", key="clear_in_btn", use_container_width=True):
                st.session_state.source_text = ""
                st.session_state.translated_text = ""
                st.session_state.detected_lang_label = None
                st.rerun()

# CENTER PANEL: Controls
with col_mid:
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    
    # Swap Button
    if st.button("⇄", help="Swap languages", key="swap_btn", use_container_width=True):
        if selected_src != "auto":
            old_src = st.session_state.source_lang
            old_tgt = st.session_state.target_lang
            st.session_state.source_lang = old_tgt
            st.session_state.target_lang = old_src
            
            # Swap input and translated text
            old_in = st.session_state.source_text
            st.session_state.source_text = st.session_state.translated_text
            st.session_state.translated_text = old_in
            st.rerun()

    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
    translate_clicked = st.button("Translate", type="primary", key="trans_btn", use_container_width=True)

# TARGET LANGUAGE SELECTION
with col_tgt:
    st.markdown("##### Target Language")
    tgt_options = {k: v for k, v in REQUESTED_LANGUAGES.items() if k != selected_src}
    
    tgt_keys = list(tgt_options.keys())
    current_tgt = st.session_state.target_lang
    tgt_idx = tgt_keys.index(current_tgt) if current_tgt in tgt_keys else 0

    selected_tgt = st.selectbox(
        "Select Target",
        options=tgt_keys,
        format_func=lambda x: tgt_options[x],
        index=tgt_idx,
        key="tgt_select_box",
        label_visibility="collapsed"
    )
    st.session_state.target_lang = selected_tgt

# TRANSLATION PROCESSING
if translate_clicked:
    raw_input = st.session_state.source_text
    if not raw_input or not raw_input.strip():
        st.warning("Please enter some text to translate.")
    else:
        active_source = selected_src
        if active_source == "auto":
            detected = translator.detect_language(raw_input)
            if detected:
                active_source = detected
                st.session_state.detected_lang_label = REQUESTED_LANGUAGES.get(detected, detected)
            else:
                st.error("Could not automatically determine language. Please select source language manually.")
                st.stop()

        with st.spinner(f"Translating {REQUESTED_LANGUAGES.get(active_source, active_source)} → {REQUESTED_LANGUAGES.get(selected_tgt, selected_tgt)}..."):
            try:
                translated_output, route = translator.translate(raw_input, active_source, selected_tgt)
                st.session_state.translated_text = translated_output
                
                # Append to history
                st.session_state.history.insert(0, {
                    "time": time.strftime("%H:%M:%S"),
                    "from": REQUESTED_LANGUAGES.get(active_source, active_source),
                    "to": REQUESTED_LANGUAGES.get(selected_tgt, selected_tgt),
                    "src": raw_input,
                    "trans": translated_output
                })
                # Keep last 10
                st.session_state.history = st.session_state.history[:10]
            except TranslationError as te:
                st.error(f"Translation Error: {te}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")

# RIGHT PANEL: Output Rendering
with col_tgt:
    actual_src = st.session_state.source_lang
    if actual_src == "auto" and st.session_state.detected_lang_label:
        matching = [k for k, v in REQUESTED_LANGUAGES.items() if v == st.session_state.detected_lang_label]
        if matching:
            actual_src = matching[0]
    
    badge_label, badge_desc = registry.get_route_description(actual_src, selected_tgt)
    badge_class = "badge-direct" if "Direct" in badge_label else ("badge-pivot" if "Pivot" in badge_label else "badge-warning")

    # Display translated text area
    st.text_area(
        "Translation Output",
        value=st.session_state.translated_text,
        placeholder="Translated text will appear here...",
        height=240,
        label_visibility="collapsed"
    )

    col_tc1, col_tc2 = st.columns([1, 1])
    with col_tc1:
        st.markdown(f"<span class='badge-route {badge_class}'>{badge_label}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 11px; color: #94a3b8; margin-top: 4px;'>{badge_desc}</div>", unsafe_allow_html=True)
    with col_tc2:
        if st.session_state.translated_text:
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
            with btn_col1:
                if st.button("🔊 Listen", key="listen_tgt_btn", use_container_width=True):
                    st.session_state.play_audio = (st.session_state.translated_text, selected_tgt)
                    st.rerun()
            with btn_col2:
                # Direct download button
                st.download_button(
                    label="📥 Save",
                    data=st.session_state.translated_text,
                    file_name=f"translation_{actual_src}_{selected_tgt}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with btn_col3:
                if st.button("Clear", key="clear_out_btn", use_container_width=True):
                    st.session_state.translated_text = ""
                    st.rerun()

# Expandable Translation History Drawer
if st.session_state.history:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    with st.expander("🕒 Recent Translations History", expanded=False):
        for idx, item in enumerate(st.session_state.history):
            h_col1, h_col2, h_col3 = st.columns([2, 5, 1])
            with h_col1:
                st.markdown(f"**{item['from']} → {item['to']}**  \n<small style='color:#64748b;'>{item['time']}</small>", unsafe_allow_html=True)
            with h_col2:
                st.markdown(f"**Original:** {item['src'][:80]}{'...' if len(item['src']) > 80 else ''}")
                st.markdown(f"<span style='color:#38bdf8;'>**Result:** {item['trans'][:80]}{'...' if len(item['trans']) > 80 else ''}</span>", unsafe_allow_html=True)
            with h_col3:
                if st.button("Load", key=f"load_hist_{idx}", use_container_width=True):
                    st.session_state.source_text = item["src"]
                    st.session_state.translated_text = item["trans"]
                    st.rerun()
            st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 13px;'>
    CodeAlpha Artificial Intelligence Internship • Project 2: Premium Language Translation Tool • 100% Offline Neural Machine Translation
</div>
""", unsafe_allow_html=True)
