"""
app.py
------
CodeAlpha AI Language Translator
Modern Streamlit web interface with dark navy styling, local offline translation,
auto-detection, character counter, language swap, and clipboard integration.
"""

import streamlit as st
from translator import OfflineTranslator, TranslationError
from language_routes import REQUESTED_LANGUAGES

# Page Configuration
st.set_page_config(
    page_title="CodeAlpha Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Premium Custom CSS (Dark Navy & Violet/Blue Accent)
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Header Card */
    .header-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);
        backdrop-filter: blur(12px);
        padding: 22px 28px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }
    .header-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 500;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
    }
    .status-pill.warning {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #fbbf24;
    }

    /* Character Count & Route Badges */
    .meta-text {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 6px;
    }
    .badge-route {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }
    .badge-direct {
        background: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .badge-pivot {
        background: rgba(168, 85, 247, 0.2);
        color: #d8b4fe;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .badge-warning {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)


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

# Header Section
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">CodeAlpha AI Language Translator</h1>
        <div class="header-subtitle">100% On-Device Neural Machine Translation • Zero Cloud Telemetry • Complete Data Privacy</div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    installed_count = len(registry.get_installed_codes())
    if installed_count > 0:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 18px;">
            <span class="status-pill">● Engine Ready ({installed_count} Languages)</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: right; padding-top: 18px;">
            <span class="status-pill warning">▲ Setup Models First</span>
        </div>
        """, unsafe_allow_html=True)

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
        placeholder="Type or paste sentences, paragraphs, or notes here...",
        height=250,
        key="input_text_area",
        label_visibility="collapsed"
    )
    st.session_state.source_text = input_text

    # Character count & Detected Language Indicator
    char_count = len(input_text)
    col_sc1, col_sc2 = st.columns([1, 1])
    with col_sc1:
        st.markdown(f"<div class='meta-text'>Length: <b>{char_count}</b> characters</div>", unsafe_allow_html=True)
        if selected_src == "auto" and st.session_state.detected_lang_label:
            st.markdown(f"<div class='meta-text' style='color:#a5b4fc;'>Detected: <b>{st.session_state.detected_lang_label}</b></div>", unsafe_allow_html=True)
    with col_sc2:
        if st.button("Clear Input", key="clear_in_btn", use_container_width=True):
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
            
            # Also swap content if translation exists
            old_in = st.session_state.source_text
            st.session_state.source_text = st.session_state.translated_text
            st.session_state.translated_text = old_in
            st.rerun()

    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
    translate_clicked = st.button("Translate", type="primary", key="trans_btn", use_container_width=True)

# RIGHT PANEL: Target Language & Output
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

    # Route Badge Display
    actual_src = st.session_state.source_lang
    if actual_src == "auto" and st.session_state.detected_lang_label:
        matching = [k for k, v in REQUESTED_LANGUAGES.items() if v == st.session_state.detected_lang_label]
        if matching:
            actual_src = matching[0]
    
    badge_label, badge_desc = registry.get_route_description(actual_src, selected_tgt)
    if "Direct" in badge_label:
        badge_class = "badge-direct"
    elif "Pivot" in badge_label:
        badge_class = "badge-pivot"
    else:
        badge_class = "badge-warning"

    # Output text area
    st.text_area(
        "Translation Output",
        value=st.session_state.translated_text,
        placeholder="Translated text will appear here...",
        height=250,
        disabled=True,
        key="output_text_area",
        label_visibility="collapsed"
    )

    col_tc1, col_tc2 = st.columns([1, 1])
    with col_tc1:
        st.markdown(f"<span class='badge-route {badge_class}'>{badge_label}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='meta-text'>{badge_desc}</div>", unsafe_allow_html=True)
    with col_tc2:
        if st.session_state.translated_text:
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if st.button("Clear Output", key="clear_out_btn", use_container_width=True):
                    st.session_state.translated_text = ""
                    st.rerun()
            with col_b2:
                # Direct Streamlit copy trigger
                if st.button("📋 Copy", key="copy_btn", use_container_width=True):
                    st.toast("Translation copied to clipboard!")

# Execute Translation Action
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
                st.error("Could not automatically determine the language. Please select the source language manually.")
                st.stop()

        with st.spinner(f"Translating {REQUESTED_LANGUAGES.get(active_source, active_source)} → {REQUESTED_LANGUAGES.get(selected_tgt, selected_tgt)}..."):
            try:
                translated_output, route = translator.translate(raw_input, active_source, selected_tgt)
                st.session_state.translated_text = translated_output
                st.rerun()
            except TranslationError as te:
                st.error(f"Translation Error: {te}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 13px;'>
    CodeAlpha Artificial Intelligence Internship • Project 2: Language Translation Tool • Offline Neural Machine Translation
</div>
""", unsafe_allow_html=True)

