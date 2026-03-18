"""
Indian MSME Compliance & Legal Bot — Streamlit Frontend
A premium chat interface for querying Indian MSME compliance regulations.
"""

import streamlit as st
import requests
import time

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="MSME Compliance Bot 🇮🇳",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── API Configuration ──────────────────────────────────────
import os
# Use 127.0.0.1 to prevent IPv6 Docker resolution bugs, or allow external URL via env var
API_BASE = os.getenv("API_URL", "http://127.0.0.1:8000")

# ─── Custom CSS for Premium Look ────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
    }
    
    /* Centralize layout like ChatGPT */
    .block-container {
        max-width: 900px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }

    /* ── Header Banner ──────────────────────────────────── */
    .hero-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        border-radius: 12px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner h1 {
        color: #F8FAFC;
        font-size: 1.7rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: #94A3B8;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }

    /* ── Chat Messages ──────────────────────────────────── */
    .user-message {
        background: #4F46E5;
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 16px 16px 4px 16px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .bot-message {
        background: transparent;
        color: #E2E8F0;
        padding: 0.5rem 0;
        border-radius: 0;
        margin: 0.5rem 0;
        max-width: 100%;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    .bot-message strong {
        color: #818CF8;
    }

    /* ── Source Citation Cards ───────────────────────────── */
    .source-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.85rem;
        border-left: 3px solid #6366F1;
    }
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.82rem;
        transition: all 0.3s ease;
    }
    .source-card:hover {
        background: rgba(108, 99, 255, 0.15);
        border-color: rgba(108, 99, 255, 0.4);
        transform: translateY(-1px);
    }
    .source-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .source-name {
        color: #A78BFA;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .source-badge {
        background: rgba(108, 99, 255, 0.2);
        color: #A78BFA;
        padding: 0.15rem 0.5rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .source-content {
        color: rgba(224, 224, 224, 0.7);
        font-size: 0.78rem;
        line-height: 1.5;
    }

    /* ── Sidebar Styling ────────────────────────────────── */
    .sidebar-section {
        background: rgba(108, 99, 255, 0.05);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    .sidebar-section h4 {
        color: #A78BFA;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Quick Question Chips ───────────────────────────── */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .chip {
        background: rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.3);
        color: #A78BFA;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.82rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
    }
    .chip:hover {
        background: rgba(108, 99, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(108, 99, 255, 0.2);
    }

    /* ── Status Badges ──────────────────────────────────── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-success {
        background: rgba(34, 197, 94, 0.15);
        color: #22C55E;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .status-error {
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .status-info {
        background: rgba(59, 130, 246, 0.15);
        color: #3B82F6;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    /* ── Animated Typing Indicator ──────────────────────── */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 0.75rem 1rem;
        background: rgba(26, 29, 41, 0.8);
        border-radius: 18px 18px 18px 4px;
        width: fit-content;
        border: 1px solid rgba(108, 99, 255, 0.2);
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #6C63FF;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
    }
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* ── Stats Cards ────────────────────────────────────── */
    .stat-card {
        background: rgba(108, 99, 255, 0.08);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #6C63FF;
    }
    .stat-label {
        font-size: 0.75rem;
        color: rgba(224, 224, 224, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Hide Streamlit default elements ────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Clean up chat input area padding */
    .stChatInputContainer {
        padding-bottom: 2rem !important;
    }

    /* ── Smooth scrollbar ───────────────────────────────── */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(108, 99, 255, 0.3);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(108, 99, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "seeded" not in st.session_state:
    st.session_state.seeded = False


# ─── Helper Functions ────────────────────────────────────────
def check_api_health() -> bool:
    """Check if the FastAPI backend is running."""
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def query_bot(question: str) -> dict:
    """Send a question to the RAG API."""
    response = requests.post(
        f"{API_BASE}/api/query",
        json={"question": question},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def seed_knowledge_base() -> dict:
    """Trigger knowledge base seeding."""
    response = requests.post(f"{API_BASE}/api/seed", timeout=120)
    response.raise_for_status()
    return response.json()


def upload_pdf(file) -> dict:
    """Upload a PDF for ingestion."""
    response = requests.post(
        f"{API_BASE}/api/ingest/pdf",
        files={"file": (file.name, file.getvalue(), "application/pdf")},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def render_sources(sources: list[dict]):
    """Render source citation cards."""
    if not sources:
        return

    st.markdown("##### 📚 Sources")
    for i, src in enumerate(sources, 1):
        st.markdown(f"""
        <div class="source-card">
            <div class="source-header">
                <span class="source-name">📄 {src.get('source', 'Unknown')}</span>
                <span class="source-badge">{src.get('similarity', 'N/A')} match</span>
            </div>
            <div class="source-content">{src.get('content', '')}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <span style="font-size: 2.5rem;">⚖️</span>
        <h2 style="
            background: linear-gradient(135deg, #6C63FF, #A78BFA);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            margin: 0.5rem 0 0;
            font-size: 1.3rem;
        ">MSME Compliance Bot</h2>
        <p style="color: rgba(224,224,224,0.5); font-size: 0.8rem; margin-top: 0.25rem;">
            Your AI Legal Assistant for Indian MSMEs
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── API Status ──
    api_ok = check_api_health()
    if api_ok:
        st.markdown('<span class="status-badge status-success">✅ API Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-error">❌ API Offline</span>', unsafe_allow_html=True)
        st.caption("Start the backend: `uvicorn app.main:app --reload`")

    st.divider()

    # ── Knowledge Base ──
    st.markdown('<div class="sidebar-section"><h4>📦 Knowledge Base</h4></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌱 Seed Data", use_container_width=True, disabled=not api_ok):
            with st.spinner("Seeding knowledge base..."):
                try:
                    result = seed_knowledge_base()
                    st.session_state.seeded = True
                    st.success(f"✅ {result['chunks_ingested']} chunks loaded!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # ── PDF Upload ──
    st.markdown('<div class="sidebar-section"><h4>📄 Upload PDF</h4></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload compliance documents",
        type=["pdf"],
        label_visibility="collapsed",
    )
    if uploaded_file and api_ok:
        if st.button("📤 Ingest PDF", use_container_width=True):
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    result = upload_pdf(uploaded_file)
                    st.success(f"✅ {result['chunks_ingested']} chunks ingested!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()

    # ── Topic Categories ──
    st.markdown('<div class="sidebar-section"><h4>📋 Quick Topics</h4></div>', unsafe_allow_html=True)

    topics = {
        "🏷️ GST Rules": "What are the GST registration requirements and composition scheme for MSMEs?",
        "👷 Labor Laws": "What are the key labor law compliance requirements for MSMEs in India?",
        "📝 MSME Registration": "How do I register for Udyam MSME registration and what are the benefits?",
        "💰 Tax Exemptions": "What tax exemptions are available for manufacturing startups in India?",
        "🏭 Gujarat Textiles": "What are the specific incentives and subsidies for textile startups in Gujarat?",
        "📅 Compliance Calendar": "What are the important annual compliance deadlines for Indian MSMEs?",
        "🌍 Export Incentives": "What export incentives are available for textile MSMEs?",
        "♻️ Environmental": "What environmental compliance is needed for textile manufacturing in Gujarat?",
    }

    for label, question in topics.items():
        if st.button(label, use_container_width=True, disabled=not api_ok):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner(""):
                try:
                    result = query_bot(question)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result.get("sources", []),
                    })
                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"❌ Error: {str(e)}",
                        "sources": [],
                    })
            st.rerun()

    st.divider()
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem;">
        <p style="color: rgba(224,224,224,0.3); font-size: 0.7rem;">
            Powered by Gemini 2.0 Flash + Supabase pgvector<br>
            Built with LangChain 🦜
            Authors: Hussain / Yash
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─── Main Chat Area ──────────────────────────────────────────
# Hero Banner
st.markdown("""
<div class="hero-banner">
    <h1>⚖️ Indian MSME Compliance Assistant</h1>
    <p>Navigate GST, labor laws, tax exemptions & state policies with AI-powered precision</p>
</div>
""", unsafe_allow_html=True)

# Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="⚖️"):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📚 View Sources", expanded=False):
                    render_sources(msg["sources"])

# Welcome Message if empty
if not st.session_state.messages:
    st.markdown("---")

    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h3 style="color: #A78BFA; font-weight: 600; margin: 0.5rem 0;">
            Welcome! Ask me anything about Indian MSME compliance.
        </h3>
        <p style="color: rgba(224,224,224,0.5); max-width: 500px; margin: 0 auto;">
            I can help with GST rules, labor laws, MSME registration, tax exemptions,
            and state-specific policies — all in plain English.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggested Questions
    st.markdown("#### 💡 Try asking:")

    suggestions = [
        "What are the specific tax exemptions for a textile startup in Gujarat?",
        "How does the GST Composition Scheme work for small manufacturers?",
        "What are the EPF and ESI requirements for a new MSME?",
        "What subsidies does the Gujarat Textile Policy 2024 offer?",
    ]

    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(
                f"💬 {suggestion}",
                key=f"suggest_{i}",
                use_container_width=True,
                disabled=not api_ok,
            ):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                with st.spinner(""):
                    try:
                        result = query_bot(suggestion)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result["answer"],
                            "sources": result.get("sources", []),
                        })
                    except Exception as e:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"❌ Error: {str(e)}",
                            "sources": [],
                        })
                st.rerun()

# ─── Chat Input ──────────────────────────────────────────────
if prompt := st.chat_input("Ask about Indian MSME compliance...", disabled=not api_ok):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("🔍 Searching compliance documents..."):
            try:
                result = query_bot(prompt)
                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("📚 View Sources", expanded=False):
                        render_sources(sources)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except requests.exceptions.ConnectionError:
                error_msg = "❌ Cannot connect to the API. Please make sure the backend is running."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": [],
                })
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": [],
                })
