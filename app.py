import os
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from serpapi import GoogleSearch

# Load .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# ─────────────────────────────────────────
# CONFIG HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAI Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# CUSTOM CSS — tema dark industrial
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0A0A0A;
    color: #E8E8E0;
}

/* Background grid pattern */
.stApp {
    background-color: #0A0A0A;
    background-image: 
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* Header utama */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.2rem;
    letter-spacing: -2px;
    line-height: 1;
    color: #E8E8E0;
    margin: 0;
}

.hero-title span {
    color: #C8F135;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #555;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 12px;
}

/* Badge status */
.badge {
    display: inline-block;
    background: #C8F135;
    color: #0A0A0A;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 4px 10px;
    text-transform: uppercase;
    margin-bottom: 24px;
}

/* Input area */
.stTextInput > div > div > input {
    background: #111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 0 !important;
    color: #E8E8E0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 16px 20px !important;
    transition: border-color 0.2s;
}

.stTextInput > div > div > input:focus {
    border-color: #C8F135 !important;
    box-shadow: 0 0 0 1px #C8F135 !important;
}

.stTextInput > div > div > input::placeholder {
    color: #3A3A3A !important;
}

/* Tombol utama */
.stButton > button {
    background: #C8F135 !important;
    color: #0A0A0A !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 14px 32px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}

.stButton > button:hover {
    background: #D9FF50 !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Card hasil */
.result-card {
    background: #111;
    border: 1px solid #1E1E1E;
    border-left: 3px solid #C8F135;
    padding: 24px 28px;
    margin-bottom: 16px;
    position: relative;
}

.result-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C8F135;
    margin-bottom: 12px;
}

.result-card-content {
    font-size: 0.9rem;
    line-height: 1.8;
    color: #B8B8B0;
}

/* Search result item */
.search-item {
    border-bottom: 1px solid #1A1A1A;
    padding: 14px 0;
}

.search-item:last-child {
    border-bottom: none;
}

.search-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #C8F135;
    letter-spacing: 2px;
}

.search-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: #E8E8E0;
    margin: 4px 0;
}

.search-url {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #444;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.search-snippet {
    font-size: 0.82rem;
    color: #777;
    line-height: 1.6;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1A1A1A;
    margin: 32px 0;
}

/* Stats row */
.stat-box {
    background: #111;
    border: 1px solid #1E1E1E;
    padding: 16px 20px;
    text-align: center;
}

.stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #C8F135;
    line-height: 1;
}

.stat-label {
    font-size: 0.7rem;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 900px; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0A0A0A; }
::-webkit-scrollbar-thumb { background: #2A2A2A; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# FUNGSI AGENT (dari project kamu)
# ─────────────────────────────────────────
def ask_llm(pertanyaan: str) -> str:
    """Kirim pertanyaan ke Groq LLM, dapat ringkasan."""
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten riset profesional. "
                    "Berikan analisis yang terstruktur, akurat, dan mudah dipahami. "
                    "Gunakan format: ringkasan → poin penting → kesimpulan."
                )
            },
            {"role": "user", "content": pertanyaan}
        ],
        temperature=0.6,
        max_tokens=1200
    )
    return response.choices[0].message.content


def search_web(query: str) -> list:
    """Cari di Google via SerpAPI, return list artikel."""
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 5,
        "hl": "id",
        "gl": "id"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])

    articles = []
    for r in organic[:5]:
        articles.append({
            "title": r.get("title", "Tanpa judul"),
            "link": r.get("link", "#"),
            "snippet": r.get("snippet", "Tidak ada cuplikan")
        })
    return articles


# ─────────────────────────────────────────
# LAYOUT UTAMA
# ─────────────────────────────────────────

# Header
st.markdown('<span class="badge">● Live · AI Research Agent v1.0</span>', unsafe_allow_html=True)
st.markdown("""
<h1 class="hero-title">RESEARCH<br><span>AGENT.</span></h1>
<p class="hero-sub">Powered by Groq LLM · SerpAPI · Built by you</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Input area
col_input, col_btn = st.columns([4, 1])

with col_input:
    query = st.text_input(
        label="Topik Riset",
        placeholder="Ketik topik riset kamu... (contoh: tren AI Indonesia 2025)",
    )

with col_btn:
    st.markdown("<div style='padding-top: 0px'>", unsafe_allow_html=True)
    run = st.button("→ RISET")
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
# PROSES & TAMPILKAN HASIL
# ─────────────────────────────────────────
if run and query.strip():
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # --- STEP 1: Search web ---
    with st.spinner(""):
        st.markdown("""
        <div style='font-family: Space Mono, monospace; font-size:0.7rem; 
                    color:#C8F135; letter-spacing:3px; margin-bottom:8px'>
            ○ STEP 01 — SEARCHING WEB...
        </div>
        """, unsafe_allow_html=True)
        
        t_start = time.time()
        articles = search_web(query)
        t_search = round(time.time() - t_start, 2)

    # Tampilkan hasil search
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-title">● Search Results — {len(articles)} sumber ditemukan</div>
    """, unsafe_allow_html=True)

    for i, article in enumerate(articles, 1):
        st.markdown(f"""
        <div class="search-item">
            <div class="search-num">[ {i:02d} ]</div>
            <div class="search-title">{article['title']}</div>
            <div class="search-url">{article['link']}</div>
            <div class="search-snippet">{article['snippet']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # --- STEP 2: Analisis LLM ---
    # Gabungkan konteks untuk LLM
    konteks = "\n\n".join(
        f"Sumber {i}: {a['title']}\n{a['snippet']}"
        for i, a in enumerate(articles, 1)
    )
    prompt_lengkap = (
        f"Topik riset: {query}\n\n"
        f"Data dari internet:\n{konteks}\n\n"
        f"Buat laporan riset komprehensif berdasarkan data di atas."
    )

    with st.spinner(""):
        st.markdown("""
        <div style='font-family: Space Mono, monospace; font-size:0.7rem; 
                    color:#C8F135; letter-spacing:3px; margin: 16px 0 8px'>
            ○ STEP 02 — ANALYZING WITH LLM...
        </div>
        """, unsafe_allow_html=True)

        t_llm = time.time()
        analisis = ask_llm(prompt_lengkap)
        t_llm = round(time.time() - t_llm, 2)

    # Tampilkan analisis LLM
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-title">● AI Analysis — Generated by Groq LLaMA 3.3</div>
        <div class="result-card-content">{analisis.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Stats row ---
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{len(articles)}</div>
            <div class="stat-label">Sumber</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{t_search}s</div>
            <div class="stat-label">Search time</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{t_llm}s</div>
            <div class="stat-label">LLM time</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        word_count = len(analisis.split())
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{word_count}</div>
            <div class="stat-label">Kata output</div>
        </div>""", unsafe_allow_html=True)

    # --- Download hasil ---
    st.markdown("<div style='margin-top: 24px'>", unsafe_allow_html=True)
    laporan_md = f"# Laporan Riset: {query}\n\n## Sumber\n"
    for i, a in enumerate(articles, 1):
        laporan_md += f"\n{i}. [{a['title']}]({a['link']})\n   {a['snippet']}\n"
    laporan_md += f"\n\n## Analisis AI\n\n{analisis}"

    st.download_button(
        label="↓ DOWNLOAD LAPORAN (.MD)",
        data=laporan_md,
        file_name=f"riset_{query[:30].replace(' ', '_')}.md",
        mime="text/markdown"
    )
    st.markdown("</div>", unsafe_allow_html=True)

elif run and not query.strip():
    st.warning("Masukkan topik riset dulu ya!")