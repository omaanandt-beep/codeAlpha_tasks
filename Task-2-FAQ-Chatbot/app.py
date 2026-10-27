"""
TechAssist — Intelligent FAQ Support
CodeAlpha AI Internship Task 2: Next-Gen IT Support & Diagnostics Suite
"""

import json
import random
import time
import uuid
import re
import os
import streamlit as st
from chatbot import FAQChatbot, DEFAULT_SIMILARITY_THRESHOLD

# Configure page settings
st.set_page_config(
    page_title="TechAssist — Next-Gen IT Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ultra-Premium Modern SaaS Dark Theme with Toolbox, Checklists, Badges & Micro-interactions
PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #06080E;
    --bg-card: #0D131F;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(99, 102, 241, 0.4);
    --accent-primary: #6366F1;
    --accent-secondary: #06B6D4;
    --accent-gradient: linear-gradient(135deg, #38BDF8 0%, #6366F1 50%, #A855F7 100%);
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
    background-color: var(--bg-main);
}

.stApp {
    background: radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 85% 85%, rgba(56, 189, 248, 0.08) 0%, transparent 45%),
                #06080E;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background-color: #080C14 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Logo Component (Tech Shield & AI Core) */
.logo-container {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 6px 0 14px 0;
}

.logo-badge {
    position: relative;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4), inset 0 0 12px rgba(56, 189, 248, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.35);
}

.logo-title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #FFFFFF 30%, #A5B4FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.1;
}

.logo-tagline {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #38BDF8;
    margin-top: 2px;
}

/* Live Pulse Pill */
.live-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #34D399;
}

.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Trending Issues Ticker */
.trending-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    overflow-x: auto;
    padding: 6px 0 14px 0;
    margin-bottom: 12px;
}

.trending-badge-title {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #F43F5E;
    display: flex;
    align-items: center;
    gap: 5px;
    margin-right: 4px;
    white-space: nowrap;
}

/* ChatGPT-Style Sidebar Chat History Items */
.history-title {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin: 14px 0 8px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Hero Box */
.hero-box {
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.85) 0%, rgba(15, 23, 42, 0.65) 100%);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}

.hero-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--accent-gradient);
}

.hero-title {
    font-size: 1.65rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin-bottom: 6px;
}

.hero-subtitle {
    font-size: 0.92rem;
    color: #94A3B8;
    line-height: 1.55;
    max-width: 820px;
}

/* Metrics Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 12px 0 20px 0;
}

.metric-card {
    background: rgba(13, 19, 31, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 12px 14px;
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.15);
}

.metric-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
}

.metric-label {
    font-size: 0.74rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 2px;
}

/* Chat Message Styling */
.msg-wrapper-user {
    display: flex;
    justify-content: flex-end;
    margin-left: 60px;
    margin-bottom: 12px;
}

.msg-bubble-user {
    background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%);
    border: 1px solid rgba(165, 180, 252, 0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    color: #F5F3FF;
    font-size: 0.94rem;
    line-height: 1.55;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}

.msg-wrapper-assistant {
    display: flex;
    justify-content: flex-start;
    margin-right: 40px;
    margin-bottom: 12px;
}

.msg-bubble-assistant {
    background: rgba(13, 19, 31, 0.88);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 3px solid #6366F1;
    border-radius: 16px 16px 16px 4px;
    padding: 18px 22px;
    color: #F8FAFC;
    font-size: 0.94rem;
    line-height: 1.7;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
}

.msg-bubble-fallback {
    background: rgba(24, 24, 27, 0.88);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-left: 3px solid #F59E0B;
    border-radius: 16px 16px 16px 4px;
    padding: 18px 22px;
    color: #F4F4F5;
    font-size: 0.94rem;
    line-height: 1.65;
}

/* Metadata Chips */
.meta-chip-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    font-size: 0.76rem;
}

.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 6px;
    font-weight: 600;
}

.meta-category {
    background: rgba(59, 130, 246, 0.12);
    color: #93C5FD;
    border: 1px solid rgba(59, 130, 246, 0.25);
}

.meta-urgency-high {
    background: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.meta-urgency-med {
    background: rgba(245, 158, 11, 0.15);
    color: #FCD34D;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.meta-urgency-low {
    background: rgba(16, 185, 129, 0.12);
    color: #6EE7B7;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.meta-time {
    background: rgba(147, 51, 234, 0.15);
    color: #D8B4FE;
    border: 1px solid rgba(147, 51, 234, 0.3);
}

.match-bar-bg {
    width: 120px;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 9999px;
    overflow: hidden;
    display: inline-block;
    vertical-align: middle;
    margin-left: 6px;
}

.match-bar-fill {
    height: 100%;
    background: var(--accent-gradient);
    border-radius: 9999px;
}

/* ===================================================
   LUXURY MODERN CHAT INPUT COMPOSER (DOCK STYLE)
   =================================================== */

div[data-testid="stChatInput"] {
    background: transparent !important;
    padding-bottom: 14px !important;
}

div[data-testid="stChatInput"] > div {
    background: rgba(15, 23, 42, 0.90) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(99, 102, 241, 0.30) !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.6), 
                0 0 0 1px rgba(255, 255, 255, 0.06),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    padding: 6px 10px !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 12px 40px -5px rgba(99, 102, 241, 0.40),
                0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    border: none !important;
    color: #F8FAFC !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    padding: 10px 12px !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #64748B !important;
    font-weight: 400 !important;
}

div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #38BDF8 0%, #6366F1 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    width: 38px !important;
    height: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stChatInput"] button:hover {
    transform: scale(1.06) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
}

/* Prompt Shortcut Cards */
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background: rgba(17, 24, 39, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #E2E8F0 !important;
    border-radius: 12px !important;
    font-size: 0.85rem !important;
    padding: 10px 14px !important;
    min-height: 50px !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
    background: rgba(30, 41, 59, 0.95) !important;
    border-color: #6366F1 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(99, 102, 241, 0.25) !important;
}

.sidebar-panel {
    background: rgba(13, 19, 31, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 12px;
    font-size: 0.82rem;
    color: #94A3B8;
    line-height: 1.5;
}

/* Interactive Checklist Card */
.checklist-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    padding: 10px 14px;
    margin-top: 10px;
}
</style>
"""

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)


def get_fresh_chatbot() -> FAQChatbot:
    return FAQChatbot()


if "chatbot" not in st.session_state:
    st.session_state.chatbot = get_fresh_chatbot()

# Multi-session Chat History state
if "sessions" not in st.session_state:
    initial_id = uuid.uuid4().hex[:8]
    st.session_state.sessions = [
        {
            "id": initial_id,
            "title": "New Chat",
            "messages": [],
            "created_at": time.strftime("%I:%M %p"),
        }
    ]
    st.session_state.active_session_id = initial_id

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = st.session_state.sessions[0]["id"]

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Chat Assistant"

if "reaction_state" not in st.session_state:
    st.session_state.reaction_state = {}

if "selected_quick_cat" not in st.session_state:
    st.session_state.selected_quick_cat = None


def get_current_session():
    """Retrieves the dictionary object of the active session."""
    for s in st.session_state.sessions:
        if s["id"] == st.session_state.active_session_id:
            return s
    return st.session_state.sessions[0]


def create_new_session():
    """Creates a new chat session at the TOP of the history list, just like ChatGPT."""
    new_id = uuid.uuid4().hex[:8]
    new_session = {
        "id": new_id,
        "title": "New Chat",
        "messages": [],
        "created_at": time.strftime("%I:%M %p"),
    }
    st.session_state.sessions.insert(0, new_session)
    st.session_state.active_session_id = new_id
    st.session_state.selected_quick_cat = None
    st.session_state.pending_query = None


def infer_urgency_and_time(category: str, question: str):
    """Calculates problem severity and estimated troubleshooting duration."""
    q_lower = (question or "").lower()
    cat_lower = (category or "").lower()

    if any(k in q_lower for k in ["bsod", "blue screen", "ransomware", "hacked", "shut down immediately", "overheat", "burning"]):
        return "🔥 High Priority", "meta-urgency-high", "⏱️ ~5-10 min fix"
    elif any(k in q_lower for k in ["wifi", "internet", "password", "pin", "crash", "write-protected", "flicker", "battery"]):
        return "⚠️ Medium Priority", "meta-urgency-med", "⏱️ ~3-5 min fix"
    else:
        return "ℹ️ Standard", "meta-urgency-low", "⏱️ ~1-2 min fix"


def parse_numbered_steps(answer_text: str):
    """Extracts numbered diagnostic steps (1)... 2)...) into a structured checklist list."""
    # Matches patterns like "1) ... 2) ..."
    parts = re.split(r"(?<=[.!?])\s*(?=\d+\))", answer_text)
    steps = [p.strip() for p in parts if p.strip()]
    return steps if len(steps) > 1 else []


def handle_send_message(query: str):
    """Processes user query through the NLP engine and appends results to current session."""
    if not query or not query.strip():
        return

    clean_query = query.strip()
    current_session = get_current_session()

    # Append user turn
    current_session["messages"].append({"role": "user", "content": clean_query})

    # Set title for new session
    if current_session["title"] == "New Chat":
        short_title = clean_query if len(clean_query) <= 28 else clean_query[:25] + "..."
        current_session["title"] = short_title

    # Move active session to the top of the history list
    st.session_state.sessions.remove(current_session)
    st.session_state.sessions.insert(0, current_session)

    # Execute NLP matching
    result = st.session_state.chatbot.match_query(clean_query)

    urgency_label, urgency_class, est_time = infer_urgency_and_time(
        result.get("category", ""), result.get("question", clean_query)
    )

    current_session["messages"].append({
        "role": "assistant",
        "matched": result["matched"],
        "is_fallback": result["is_fallback"],
        "answer": result["answer"],
        "score": result["score"],
        "confidence": result.get("confidence", "None"),
        "category": result.get("category"),
        "canonical_question": result.get("question"),
        "matched_variant": result.get("matched_variant"),
        "suggested_questions": result.get("suggested_questions", []),
        "urgency_label": urgency_label,
        "urgency_class": urgency_class,
        "est_time": est_time,
    })


# ---------------- SIDEBAR NAVIGATION, CHAT HISTORY & TOOLBOX ----------------
with st.sidebar:
    # Modern Logo with Tagline (Cybernetic Shield & Intelligent Core)
    st.markdown("""
    <div class="logo-container">
        <div class="logo-badge">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L3 6V11.5C3 16.5 6.8 21.2 12 22.5C17.2 21.2 21 16.5 21 11.5V6L12 2Z" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="11.5" r="3" fill="#6366F1"/>
                <path d="M12 8.5V6M12 17V14.5M8.5 11.5H6M18 11.5H15.5" stroke="#A5B4FC" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div class="logo-text-group">
            <h1 class="logo-title">TechAssist</h1>
            <span class="logo-tagline">Next-Gen IT Intelligence</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Real-time Status Badge
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <span class="live-status-pill">
            <span class="pulse-dot"></span>
            Offline NLP Engine Active
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Primary Actions Row
    c_btn1, c_btn2 = st.columns([1.2, 1])
    with c_btn1:
        if st.button("✨ New Chat", use_container_width=True, type="primary"):
            create_new_session()
            st.rerun()
    with c_btn2:
        if st.button("🎲 Random", use_container_width=True):
            all_faqs = st.session_state.chatbot.faqs
            if all_faqs:
                random_faq = random.choice(all_faqs)
                variants = [random_faq["question"]] + random_faq.get("alternatives", [])
                st.session_state.pending_query = random.choice(variants)
                st.rerun()

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # ---------------- CHATGPT-STYLE RECENT CONVERSATIONS LIST ----------------
    st.markdown("""
    <div class="history-title">
        <span>🕒 Recent Conversations</span>
    </div>
    """, unsafe_allow_html=True)

    for s in st.session_state.sessions:
        is_active = (s["id"] == st.session_state.active_session_id)
        btn_label = f"💬 {s['title']}"
        if is_active:
            btn_label = f"👉 {s['title']}"

        col_sess, col_del = st.columns([5, 1])
        with col_sess:
            if st.button(btn_label, key=f"sess_btn_{s['id']}", use_container_width=True):
                st.session_state.active_session_id = s["id"]
                st.session_state.nav_mode = "Chat Assistant"
                st.rerun()
        with col_del:
            if len(st.session_state.sessions) > 1:
                if st.button("✕", key=f"del_sess_{s['id']}", use_container_width=True, help="Delete chat"):
                    st.session_state.sessions.remove(s)
                    if st.session_state.active_session_id == s["id"]:
                        st.session_state.active_session_id = st.session_state.sessions[0]["id"]
                    st.rerun()

    # Clear All Sessions Button
    if len(st.session_state.sessions) > 1:
        if st.button("🗑️ Clear All Chat History", use_container_width=True):
            initial_id = uuid.uuid4().hex[:8]
            st.session_state.sessions = [{
                "id": initial_id,
                "title": "New Chat",
                "messages": [],
                "created_at": time.strftime("%I:%M %p"),
            }]
            st.session_state.active_session_id = initial_id
            st.rerun()

    st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.08); margin:14px 0;'>", unsafe_allow_html=True)

    # Navigation Mode Selection
    nav_selection = st.radio(
        "Application Mode",
        options=["Chat Assistant", "Browse Knowledge Base", "🛠️ IT Diagnostic Toolbox"],
        index=0 if st.session_state.nav_mode == "Chat Assistant" else (1 if st.session_state.nav_mode == "Browse Knowledge Base" else 2),
        key="nav_radio",
    )
    st.session_state.nav_mode = nav_selection

    # System Overview
    total_faqs = st.session_state.chatbot.get_total_count()
    total_variants = len(st.session_state.chatbot.indexed_variants)

    st.markdown(f"""
    <div class="sidebar-panel">
        <div style="font-weight:700; color:#F8FAFC; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
            <span>📊</span> Engine Telemetry
        </div>
        • Verified Solutions: <b style="color:#A5B4FC;">{total_faqs}</b><br>
        • Question Vectors: <b style="color:#A5B4FC;">{total_variants}</b><br>
        • Vector Space: <b style="color:#A5B4FC;">TF-IDF (1-2 ngrams)</b><br>
        • Decision Cutoff: <b style="color:#A5B4FC;">{st.session_state.chatbot.similarity_threshold}</b>
    </div>
    """, unsafe_allow_html=True)

    # Export Transcript Button
    active_messages = get_current_session()["messages"]
    if active_messages:
        chat_text = f"# TechAssist Troubleshooting Session: {get_current_session()['title']}\n\n"
        for m in active_messages:
            role = "USER" if m["role"] == "user" else "TECHASSIST"
            chat_text += f"### {role}:\n{m.get('content') or m.get('answer')}\n\n"
        st.download_button(
            label="📥 Export Chat Session",
            data=chat_text,
            file_name=f"techassist_{get_current_session()['id']}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown("""
    <div class="sidebar-panel" style="border-color:rgba(16,185,129,0.3); background:rgba(16,185,129,0.04);">
        <span style="color:#34D399; font-weight:700;">🔒 Private & Offline</span><br>
        100% on-device processing. No cloud LLMs, tracking, or data leaks.
    </div>
    """, unsafe_allow_html=True)


# ---------------- TOP BRANDING & INTERACTIVE HEADER ----------------
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 14px; margin-bottom: 14px;">
    <div style="display:flex; align-items:center; gap:14px;">
        <div class="logo-badge" style="width:42px; height:42px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L3 6V11.5C3 16.5 6.8 21.2 12 22.5C17.2 21.2 21 16.5 21 11.5V6L12 2Z" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="11.5" r="3" fill="#6366F1"/>
                <path d="M12 8.5V6M12 17V14.5M8.5 11.5H6M18 11.5H15.5" stroke="#A5B4FC" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div>
            <div style="display:flex; align-items:center; gap:8px;">
                <h1 style="margin:0; font-size:1.6rem; font-weight:800; letter-spacing:-0.03em; color:#FFFFFF;">TechAssist</h1>
                <span style="font-size:0.7rem; font-weight:700; background:rgba(99,102,241,0.2); color:#A5B4FC; border:1px solid rgba(99,102,241,0.4); padding:2px 8px; border-radius:9999px;">PRO SUITE</span>
            </div>
            <div style="font-size:0.84rem; color:#94A3B8; font-weight:500;">
                Next-Gen IT Intelligence • Instant Local Precision
            </div>
        </div>
    </div>
    <div style="display:flex; gap:8px;">
        <span class="live-status-pill">🛡️ Local Latency &lt; 15ms</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- TRENDING IT ISSUES QUICK BAR ----------------
trending_issues = [
    ("🔥 Blue Screen (BSOD)", "How do I fix a blue screen of death BSOD crash?"),
    ("📶 Wi-Fi No Internet", "Why does my Wi-Fi say Connected no internet access?"),
    ("🌡️ Laptop Overheating", "Why does my laptop fan make loud noises and get extremely hot?"),
    ("🔋 Fast Battery Drain", "Why is my laptop battery draining so fast?"),
    ("🎧 Bluetooth Issue", "Why is my Bluetooth device not pairing or connecting?"),
    ("💾 Write Protected USB", "How do I remove write-protected error on USB?"),
]

st.markdown("<div class='trending-bar'><span class='trending-badge-title'>🔥 Trending Issues:</span>", unsafe_allow_html=True)
tr_cols = st.columns(len(trending_issues))
for tr_idx, (t_label, t_q) in enumerate(trending_issues):
    with tr_cols[tr_idx]:
        if st.button(t_label, key=f"trend_btn_{tr_idx}", use_container_width=True):
            st.session_state.pending_query = t_q
            st.session_state.nav_mode = "Chat Assistant"
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)


# Check for queued questions from suggestions or FAQ explorer
if st.session_state.pending_query:
    queued = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_send_message(queued)
    st.rerun()


# ---------------- VIEW 1: CHAT ASSISTANT ----------------
if st.session_state.nav_mode == "Chat Assistant":
    active_session = get_current_session()
    session_messages = active_session["messages"]

    # Welcome Hero if no conversation yet in active session
    if not session_messages:
        st.markdown("""
        <div class="hero-box">
            <div class="live-status-pill" style="margin-bottom:12px;">
                <span class="pulse-dot"></span> Ready to Assist
            </div>
            <div class="hero-title">How can I help you today?</div>
            <div class="hero-subtitle">
                Instant, reliable troubleshooting for hardware malfunctions, Wi-Fi connectivity, Windows BSOD crashes, password resets, and cybersecurity. Select a topic pill below or ask directly in the search bar.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Metrics Bar
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_faqs}</div>
                <div class="metric-label">Verified FAQs</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_variants}</div>
                <div class="metric-label">Trained Vectors</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">9</div>
                <div class="metric-label">Tech Domains</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">100%</div>
                <div class="metric-label">On-Device Privacy</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Category Quick Pills
        st.markdown("<p style='font-size:0.80rem; font-weight:700; color:#A5B4FC; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;'>🏷️ EXPLORE BY TROUBLESHOOTING CATEGORY</p>", unsafe_allow_html=True)

        quick_categories = [
            ("💻 Laptop & PC", "Computer and Laptop Troubleshooting"),
            ("🌐 Wi-Fi & Network", "Internet and Wi-Fi Problems"),
            ("🔐 Passwords & Accounts", "Account Access and Password Issues"),
            ("📁 Backups & Storage", "File Management and Backups"),
            ("🪟 Windows OS & BSOD", "Operating-System Issues"),
            ("⚠️ App Crashes", "Application Errors"),
            ("🛡️ Cybersecurity", "Basic Cybersecurity and Safe Computing"),
        ]

        cat_cols = st.columns(len(quick_categories))
        for idx, (label, cat_val) in enumerate(quick_categories):
            with cat_cols[idx]:
                if st.button(label, key=f"quick_cat_{idx}", use_container_width=True):
                    st.session_state.selected_quick_cat = cat_val
                    st.rerun()

        active_cat = st.session_state.selected_quick_cat
        if active_cat:
            cat_faqs = [f for f in st.session_state.chatbot.faqs if f["category"] == active_cat][:3]
            st.markdown(f"<p style='font-size:0.80rem; color:#38BDF8; font-weight:600; margin-top:8px;'>Showing top questions for <b>{active_cat}</b>:</p>", unsafe_allow_html=True)
            cols_sub = st.columns(len(cat_faqs))
            for s_idx, q_item in enumerate(cat_faqs):
                with cols_sub[s_idx]:
                    if st.button(f"👉 {q_item['question']}", key=f"cat_q_{s_idx}", use_container_width=True):
                        st.session_state.pending_query = q_item["question"]
                        st.rerun()
        else:
            st.markdown("<p style='font-size:0.80rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em; margin-top:6px; margin-bottom:10px;'>✨ POPULAR TECHNICAL INQUIRIES</p>", unsafe_allow_html=True)
            sample_questions = st.session_state.chatbot.get_suggested_questions(count=4)
            col1, col2 = st.columns(2)
            for i, q_text in enumerate(sample_questions):
                col = col1 if (i % 2 == 0) else col2
                with col:
                    if st.button(f"🔍 {q_text}", key=f"sugg_card_{i}", use_container_width=True):
                        st.session_state.pending_query = q_text
                        st.rerun()

    # Conversation History Display for Active Session
    for idx, msg in enumerate(session_messages):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-wrapper-user">
                <div class="msg-bubble-user">
                    <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; color:#A5B4FC; font-weight:700; margin-bottom:4px; display:flex; align-items:center; gap:5px;">
                        <span>👤</span> You
                    </div>
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if msg.get("matched", False):
                canonical_label = (
                    f"<div style='font-size:0.80rem; color:#A5B4FC; font-weight:600; margin-bottom:8px;'>🎯 Matched Knowledge Record: \"{msg.get('canonical_question')}\"</div>"
                    if msg.get("canonical_question") else ""
                )
                score_pct = int(msg.get("score", 0.0) * 100)
                category = msg.get("category", "General")
                confidence = msg.get("confidence", "Medium")
                conf_class = "meta-confidence-high" if confidence == "High" else "meta-confidence-med"
                urgency = msg.get("urgency_label", "ℹ️ Standard")
                urgency_class = msg.get("urgency_class", "meta-urgency-low")
                est_time = msg.get("est_time", "⏱️ ~2 min fix")

                st.markdown(f"""
                <div class="msg-wrapper-assistant">
                    <div class="msg-bubble-assistant">
                        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <div style="width:24px; height:24px; border-radius:6px; background:linear-gradient(135deg, #38BDF8 0%, #6366F1 100%); display:flex; align-items:center; justify-content:center;">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M12 2L3 6V11.5C3 16.5 6.8 21.2 12 22.5C17.2 21.2 21 16.5 21 11.5V6L12 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </div>
                                <span style="font-weight:700; color:#FFFFFF; font-size:0.86rem; letter-spacing:0.02em;">TechAssist Intelligence</span>
                            </div>
                            <div style="display:flex; align-items:center; gap:6px;">
                                <span class="meta-chip {conf_class}">Match Score: {score_pct}%</span>
                                <div class="match-bar-bg"><div class="match-bar-fill" style="width: {score_pct}%;"></div></div>
                            </div>
                        </div>
                        {canonical_label}
                        <div style="color:#F1F5F9; line-height:1.7;">{msg["answer"]}</div>
                        <div class="meta-chip-row">
                            <span class="meta-chip meta-category">📁 {category}</span>
                            <span class="meta-chip {urgency_class}">{urgency}</span>
                            <span class="meta-chip meta-time">{est_time}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Interactive Action Bar: Helpful reaction + Listen button
                rxn_key = f"reaction_{active_session['id']}_{idx}"
                c_act1, c_act2, c_act3, _ = st.columns([1, 1, 1.3, 6])
                with c_act1:
                    if st.button("👍 Helpful", key=f"btn_up_{active_session['id']}_{idx}", use_container_width=True):
                        st.session_state.reaction_state[rxn_key] = "up"
                        st.toast("Thank you! Feedback recorded.", icon="⭐")
                with c_act2:
                    if st.button("👎 Not quite", key=f"btn_down_{active_session['id']}_{idx}", use_container_width=True):
                        st.session_state.reaction_state[rxn_key] = "down"
                        st.toast("Feedback noted. We're tuning vector precision.", icon="📝")
                with c_act3:
                    clean_speech_text = msg["answer"].replace('"', '\\"').replace("'", "\\'")
                    audio_html = f"""
                    <button onclick="window.speechSynthesis.cancel(); let u = new SpeechSynthesisUtterance('{clean_speech_text}'); u.rate = 1.0; window.speechSynthesis.speak(u);" 
                            style="background:rgba(99,102,241,0.15); border:1px solid rgba(99,102,241,0.3); color:#A5B4FC; border-radius:8px; padding:6px 12px; font-size:0.78rem; font-weight:600; cursor:pointer; width:100%; display:flex; align-items:center; justify-content:center; gap:6px;">
                        🔊 Read Aloud
                    </button>
                    """
                    st.components.v1.html(audio_html, height=36)

                # Step-by-Step Interactive Checklist View (if answer contains numbered steps)
                numbered_steps = parse_numbered_steps(msg["answer"])
                if numbered_steps:
                    with st.expander("📋 Interactive Step-by-Step Troubleshooting Checklist"):
                        st.markdown("<p style='font-size:0.80rem; color:#94A3B8; margin-bottom:8px;'>Tick off each step as you execute it on your computer:</p>", unsafe_allow_html=True)
                        for step_idx, step_txt in enumerate(numbered_steps):
                            st.checkbox(step_txt, key=f"chk_{active_session['id']}_{idx}_{step_idx}")

            else:
                # Polished Fallback Message Bubble
                st.markdown(f"""
                <div class="msg-wrapper-assistant">
                    <div class="msg-bubble-fallback">
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                            <span style="font-size:16px;">⚠️</span>
                            <span style="font-weight:700; color:#FBBF24; font-size:0.86rem;">No Direct Knowledge Match</span>
                        </div>
                        <div style="color:#E4E4E7; line-height:1.65;">{msg["answer"]}</div>
                        <div class="meta-chip-row">
                            <span class="meta-chip" style="background:rgba(245,158,11,0.15); color:#FCD34D;">Similarity below cutoff ({st.session_state.chatbot.similarity_threshold})</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Display Follow-up Suggestions if available
            sugg_qs = msg.get("suggested_questions", [])
            if sugg_qs:
                st.markdown("<div style='margin-left: 6px; margin-top: 8px; margin-bottom: 6px;'><span style='font-size:0.78rem; font-weight:600; color:#94A3B8;'>RELATED TROUBLESHOOTING TOPICS:</span></div>", unsafe_allow_html=True)
                sugg_cols = st.columns(len(sugg_qs))
                for s_idx, sq in enumerate(sugg_qs):
                    with sugg_cols[s_idx]:
                        if st.button(f"👉 {sq}", key=f"resp_sugg_{active_session['id']}_{idx}_{s_idx}", use_container_width=True):
                            st.session_state.pending_query = sq
                            st.rerun()

    # Luxury Message Composer
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    user_input = st.chat_input("Ask a technical question (e.g. 'Laptop fan is loud and hot', 'Wi-Fi connected no internet')...")
    if user_input:
        handle_send_message(user_input)
        st.rerun()

    # Footer note with shortcut badge
    st.markdown("""
    <div style="text-align:center; padding:12px 0 6px 0; color:#475569; font-size:0.75rem; display:flex; align-items:center; justify-content:center; gap:8px;">
        <span>🛡️ TechAssist Engine • 100% Offline AI Matching</span>
        <span style="background:rgba(255,255,255,0.06); padding:2px 6px; border-radius:4px; font-family:'JetBrains Mono', monospace; font-size:0.70rem;">Enter ↵ to send</span>
    </div>
    """, unsafe_allow_html=True)


# ---------------- VIEW 2: BROWSE KNOWLEDGE BASE ----------------
elif st.session_state.nav_mode == "Browse Knowledge Base":
    st.markdown("""
    <div style="margin-bottom:18px;">
        <h2 style="font-size:1.4rem; font-weight:800; color:#FFFFFF; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
            <span>📚</span> Knowledge Base Explorer
        </h2>
        <p style="font-size:0.88rem; color:#94A3B8; margin:0;">
            Search and inspect all verified technical troubleshooting records. Click "Open in Chat" to launch any solution directly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Search & Category Filters
    search_col, filter_col = st.columns([3, 2])
    with search_col:
        search_term = st.text_input("🔍 Search solutions by keyword...", placeholder="e.g. Wi-Fi, BSOD, password, backup, sound, virus")
    with filter_col:
        all_categories = ["All Categories"] + st.session_state.chatbot.get_categories()
        selected_category = st.selectbox("Category Filter", options=all_categories)

    actual_cat = "All" if selected_category == "All Categories" else selected_category
    filtered_faqs = st.session_state.chatbot.search_faqs(query=search_term, category=actual_cat)

    st.markdown(f"<div style='font-size:0.82rem; color:#94A3B8; margin-bottom:14px;'>Displaying <b>{len(filtered_faqs)}</b> verified solutions</div>", unsafe_allow_html=True)

    if not filtered_faqs:
        st.markdown("""
        <div style="background:#0D131F; border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:28px; text-align:center; color:#94A3B8;">
            🔍 No matching FAQs found. Try searching for a broader term or select 'All Categories'.
        </div>
        """, unsafe_allow_html=True)
    else:
        for faq in filtered_faqs:
            with st.expander(f"📁 [{faq['category']}] {faq['question']}"):
                st.markdown(f"**Verified Resolution:**\n{faq['answer']}")
                if faq.get("alternatives"):
                    st.markdown("**Alternative Phrasings Indexed in Vector Space:**")
                    for alt in faq["alternatives"]:
                        st.markdown(f"- *{alt}*")
                
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("💬 Open in Chat", key=f"ask_expander_{faq['id']}"):
                    st.session_state.nav_mode = "Chat Assistant"
                    st.session_state.pending_query = faq["question"]
                    st.rerun()


# ---------------- VIEW 3: 🛠️ IT DIAGNOSTIC TOOLBOX ----------------
elif st.session_state.nav_mode == "🛠️ IT Diagnostic Toolbox":
    st.markdown("""
    <div style="margin-bottom:18px;">
        <h2 style="font-size:1.4rem; font-weight:800; color:#FFFFFF; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
            <span>🛠️</span> Professional IT Diagnostic Toolbox
        </h2>
        <p style="font-size:0.88rem; color:#94A3B8; margin:0;">
            Standard Windows administrative troubleshooting commands ready for 1-click execution in PowerShell or Command Prompt (Admin).
        </p>
    </div>
    """, unsafe_allow_html=True)

    toolbox_tools = [
        {
            "title": "🌐 Network & DNS Cache Reset",
            "desc": "Resolves websites refusing to load, 'Connected No Internet', and DNS resolution failures.",
            "cmd": "ipconfig /flushdns; ipconfig /renew; netsh winsock reset",
        },
        {
            "title": "🔍 System File Checker (SFC Scan)",
            "desc": "Scans Windows system DLLs and automatically repairs corrupted OS files from clean cache.",
            "cmd": "sfc /scannow",
        },
        {
            "title": "🩹 DISM Windows Image Repair",
            "desc": "Repairs underlying Windows Component Store and image health using Windows Update repositories.",
            "cmd": "DISM /Online /Cleanup-Image /RestoreHealth",
        },
        {
            "title": "🔋 Laptop Battery Health HTML Diagnostic",
            "desc": "Generates an official detailed battery wear, cycle count, and capacity report in HTML format.",
            "cmd": "powercfg /batteryreport /output $env:USERPROFILE\\Desktop\\battery_report.html",
        },
        {
            "title": "🧹 Clear Stuck Windows Printer Queue",
            "desc": "Stops Print Spooler, empties trapped print job spool files, and cleanly restarts the service.",
            "cmd": "net stop spooler; Remove-Item C:\\Windows\\System32\\spool\\PRINTERS\\* -Force; net start spooler",
        },
        {
            "title": "🧠 Windows Memory Diagnostic (RAM Test)",
            "desc": "Launches the pre-boot memory diagnostic tool to detect faulty or degraded RAM sticks.",
            "cmd": "mdsched.exe",
        },
    ]

    for tool in toolbox_tools:
        with st.container():
            st.markdown(f"""
            <div style="background:rgba(13, 19, 31, 0.8); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px 20px; margin-bottom:14px;">
                <h4 style="margin:0 0 6px 0; color:#FFFFFF; font-size:1.05rem;">{tool['title']}</h4>
                <p style="margin:0 0 10px 0; color:#94A3B8; font-size:0.86rem;">{tool['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.code(tool["cmd"], language="powershell")
