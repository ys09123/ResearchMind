import streamlit as st
import time
import os
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# Check for required API key
if not os.getenv("GROQ_API_KEY"):
    st.error(
        "⚠️ **Missing GROQ_API_KEY**\n\n"
        "To use ResearchMind, you need to configure your Groq API key:\n\n"
        "**On Streamlit Cloud:**\n"
        "1. Go to your app settings (menu → Manage app)\n"
        "2. Click 'Secrets' in the left sidebar\n"
        "3. Add: `GROQ_API_KEY = your_groq_api_key_here`\n"
        "4. Save and redeploy your app\n\n"
        "**Locally:**\n"
        "Create a `.streamlit/secrets.toml` file with your key, or set the `GROQ_API_KEY` environment variable."
    )
    st.stop()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Deep Research Engine",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,300;1,9..144,400&family=Instrument+Sans:wght@400;500;600&family=Martian+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
    color: #1a1a2e !important;
}

/* ── Force dark text on all Streamlit markdown output ── */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown ol,
.stMarkdown ul, .stMarkdown blockquote, .stMarkdown td,
.stMarkdown th, .stMarkdown a, .stMarkdown strong, .stMarkdown em,
.element-container p, .element-container li, .element-container span,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] span,
div[data-testid="stMarkdownContainer"] strong,
div[data-testid="stMarkdownContainer"] em,
div[data-testid="stMarkdownContainer"] a {
    color: #1a1a2e !important;
}

div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    color: #1a1a2e !important;
    font-family: 'Fraunces', serif !important;
    letter-spacing: -0.02em;
}

div[data-testid="stMarkdownContainer"] code {
    color: #3a3060 !important;
    background: #eee9de !important;
}

.stApp {
    background: #f7f4ee;
    background-image:
        radial-gradient(ellipse 120% 60% at 100% 0%, rgba(21,52,84,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 80% 40% at 0% 100%, rgba(139,90,60,0.05) 0%, transparent 55%);
}

/* Subtle grid texture overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 40L40 0M-5 5L5 -5M35 45L45 35' stroke='%231a1a2e' stroke-width='0.3' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 3.5rem 5rem;
    max-width: 1280px;
    position: relative;
    z-index: 1;
}

/* ── Masthead ── */
.masthead {
    border-bottom: 2px solid #1a1a2e;
    padding: 1.5rem 0 1rem;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 0;
}
.masthead-left {
    display: flex;
    align-items: baseline;
    gap: 1.2rem;
}
.masthead-title {
    font-family: 'Fraunces', serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #1a1a2e;
    line-height: 1;
}
.masthead-vol {
    font-family: 'Martian Mono', monospace;
    font-size: 0.62rem;
    color: #8a7f6e;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border: 1px solid #c8bfaa;
    border-radius: 3px;
}
.masthead-right {
    font-family: 'Martian Mono', monospace;
    font-size: 0.6rem;
    color: #8a7f6e;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Hero band ── */
.hero-band {
    background: #1a1a2e;
    margin: 0 -3.5rem;
    padding: 3rem 3.5rem 2.8rem;
    position: relative;
    overflow: hidden;
}
.hero-band::after {
    content: 'RESEARCH';
    position: absolute;
    right: 3rem;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Fraunces', serif;
    font-size: 9rem;
    font-weight: 700;
    color: rgba(255,255,255,0.04);
    letter-spacing: -0.06em;
    line-height: 1;
    pointer-events: none;
    white-space: nowrap;
}
.hero-kicker {
    font-family: 'Martian Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c4a96a;
    margin-bottom: 0.8rem;
}
.hero-headline {
    font-family: 'Fraunces', serif;
    font-size: clamp(2.4rem, 4.5vw, 4rem);
    font-weight: 600;
    line-height: 1.08;
    letter-spacing: -0.03em;
    color: #f7f4ee;
    max-width: 640px;
    margin-bottom: 1rem;
}
.hero-headline em {
    font-style: italic;
    color: #c4a96a;
    font-weight: 300;
}
.hero-dek {
    font-size: 0.95rem;
    line-height: 1.7;
    color: #9b97a0;
    max-width: 500px;
    font-weight: 400;
}

/* ── Rule ── */
.rule-thick {
    height: 3px;
    background: #1a1a2e;
    margin: 1.5rem 0 0;
}
.rule-thin {
    height: 1px;
    background: #d5cebe;
    margin: 1.5rem 0;
}

.stTextInput input {
    background: #ffffff !important;
    border: 1.5px solid #c8bfaa !important;
    border-radius: 4px !important;
    color: #1a1a2e !important;
    caret-color: #000000 !important;

    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.1rem !important;

    transition: border-color 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1a1a2e !important;
    box-shadow: 0 0 0 3px rgba(26,26,46,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #a09884 !important; }
.stTextInput > label {
    font-family: 'Martian Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #6a6050 !important;
    font-weight: 400 !important;
    margin-bottom: 0.5rem !important;
}

/* ── Button ── */
div.stButton > button {
    background: #1a1a2e !important;
    color: white !important;
    border: none !important;

    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;

    border-radius: 4px !important;
    padding: 0.8rem 2rem !important;

    width: 100% !important;

    -webkit-text-fill-color: white !important;
    opacity: 1 !important;
}

/* target actual text container */
div.stButton > button p,
div.stButton > button span,
div.stButton > button div {
    color: white !important;
    -webkit-text-fill-color: white !important;
    opacity: 1 !important;
}

div.stButton > button:hover {
    background: #2d2d4e !important;
    color: white !important;
}

div.stButton > button:hover p,
div.stButton > button:hover span,
div.stButton > button:hover div {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

/* ── Pipeline ── */
.pipeline-header {
    font-family: 'Martian Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8a7f6e;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #1a1a2e;
}

.step-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #e0d9cc;
    position: relative;
    transition: background 0.2s;
}
.step-row.state-active {
    background: rgba(196,169,106,0.28);
    border: 1px solid rgba(196,169,106,0.35);

    margin: 0 -0.8rem;
    padding: 1rem 0.8rem;

    border-radius: 6px;
    border-bottom: 1px solid transparent;

    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.step-row.state-done .step-index { color: #2a7a4b; border-color: #2a7a4b; }
.step-row.state-active .step-index { color: #c4a96a; border-color: #c4a96a; }

.step-index {
    font-family: 'Martian Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #c8bfaa;
    border: 1px solid #c8bfaa;
    border-radius: 3px;
    padding: 0.15rem 0.45rem;
    min-width: 32px;
    text-align: center;
    transition: all 0.3s;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.step-body { flex: 1; }
.step-name {
    font-family: 'Fraunces', serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #1a1a2e;
    letter-spacing: -0.01em;
}
.step-desc {
    font-size: 0.77rem;
    color: #8a7f6e;
    margin-top: 0.15rem;
    line-height: 1.5;
}
.step-badge {
    font-family: 'Martian Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.5rem;
    border-radius: 3px;
    flex-shrink: 0;
    margin-top: 0.15rem;
}
.badge-waiting { color: #b0a898; background: #ede8de; }
.badge-running { color: #8a6020; background: rgba(196,169,106,0.18); }
.badge-done    { color: #2a7a4b; background: rgba(42,122,75,0.1); }

/* ── Input section card ── */
.input-section {
    background: #ffffff;
    border: 1.5px solid #ddd8cc;
    border-radius: 6px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

/* ── Examples ── */
.example-label {
    font-family: 'Martian Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a09884;
    margin-bottom: 0.6rem;
}
.example-chip {
    display: inline-block;
    background: #f0ebe0;
    border: 1px solid #d5cebe;
    border-radius: 3px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    color: #5a5040;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-family: 'Instrument Sans', sans-serif;
    cursor: default;
}

/* ── Result panels ── */
.result-block {
    margin-bottom: 2rem;
}
.result-label {
    font-family: 'Martian Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8a7f6e;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #1a1a2e;
}
.result-raw {
    background: #ffffff;
    border: 1px solid #ddd8cc;
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    font-size: 0.85rem;
    line-height: 1.8;
    color: #4a4540;
    white-space: pre-wrap;
    font-family: 'Instrument Sans', sans-serif;
    max-height: 320px;
    overflow-y: auto;
}

/* ── Report panel ── */
.report-wrap {
    background: #ffffff;
    border: 1.5px solid #1a1a2e;
    border-radius: 6px;
    padding: 2.5rem 3rem;
    box-shadow: 4px 4px 0 #1a1a2e;
    margin-bottom: 2rem;
}
.report-wrap h1,
.report-wrap h2,
.report-wrap h3 {
    font-family: 'Fraunces', serif !important;
    color: #1a1a2e !important;
    letter-spacing: -0.02em;
}

/* ── Critic panel ── */
.critic-wrap {
    background: #f0f7f2;
    border: 1.5px solid #2a7a4b;
    border-radius: 6px;
    padding: 2rem 2.5rem;
    box-shadow: 4px 4px 0 #2a7a4b;
    margin-bottom: 2rem;
}

/* ── Expander override ── */
details summary {
    font-family: 'Martian Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #8a7f6e !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #1a1a2e !important;
    border: 1.5px solid #1a1a2e !important;
    font-family: 'Martian Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 0.6rem 1.4rem !important;
    transition: background 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #1a1a2e !important;
    color: #f7f4ee !important;
}

/* ── Section title ── */
.section-title {
    font-family: 'Fraunces', serif;
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: -0.025em;
    color: #1a1a2e;
    margin: 2rem 0 1rem;
}

/* ── Footer ── */
.foot {
    font-family: 'Martian Mono', monospace;
    font-size: 0.58rem;
    color: #b0a898;
    text-align: center;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #d5cebe;
}

/* Spinner color */
.stSpinner > div { color: #1a1a2e !important; }

/* Warning */
.stWarning { border-left-color: #c4a96a !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper: step card ─────────────────────────────────────────────────────────
def step_card(num: str, title: str, desc: str, state: str):
    badge_map = {
        "waiting": ("Queued",  "badge-waiting"),
        "running": ("Running", "badge-running"),
        "done":    ("Done",    "badge-done"),
    }
    label, bcls = badge_map.get(state, ("", ""))
    row_cls = {"running": "state-active", "done": "state-done"}.get(state, "")
    st.markdown(f"""
    <div class="step-row {row_cls}">
        <div class="step-index">{num}</div>
        <div class="step-body">
            <div class="step-name">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        <div class="step-badge {bcls}">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-left">
        <span class="masthead-title">ResearchMind</span>
        <span class="masthead-vol">Multi-Agent Engine</span>
    </div>
    <span class="masthead-right">Powered by LangChain · AI Research Suite</span>
</div>
<div class="rule-thick"></div>
""", unsafe_allow_html=True)


# ── Hero band ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-band">
    <div class="hero-kicker">Deep Research · Four-Agent Pipeline</div>
    <div class="hero-headline">Intelligent research,<br><em>delivered in seconds.</em></div>
    <p class="hero-dek">
        Four specialized agents — search, extract, write, critique — collaborate
        to produce a polished, cited research report on any topic you choose.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
col_left, col_gap, col_right = st.columns([5, 0.4, 4])

with col_left:
    # Input card
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        key="topic_input",
    )
    run_btn = st.button("Run Research Pipeline →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Examples
    st.markdown('<div class="example-label">Suggested topics</div>', unsafe_allow_html=True)
    for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress", "Agentic AI workflows"]:
        st.markdown(f'<span class="example-chip">{ex}</span>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="pipeline-header">Agent Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  "Gathers recent web information",         s("search"))
    step_card("02", "Reader Agent",  "Scrapes & extracts deep content",        s("reader"))
    step_card("03", "Writer Chain",  "Drafts the full research report",        s("writer"))
    step_card("04", "Critic Chain",  "Reviews, scores & refines the report",   s("critic"))


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic before running the pipeline.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    try:
        with st.spinner("Search Agent is working…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)

        with st.spinner("Reader Agent is scraping top resources…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and use the scrape_url tool to get deeper content.\n\n"
                    f"Only use the scrape_url tool. If scraping fails, summarise what you know from the search results instead.\n\n"
                    f"Search Results:\n{results['search']}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)

        with st.spinner("Writer is drafting the report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = dict(results)

        with st.spinner("Critic is reviewing the report…"):
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
            st.session_state.results = dict(results)

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as e:
        st.session_state.running = False
        st.session_state.done = False
        error_msg = str(e)
        
        if "NotFoundError" in error_msg or "404" in error_msg or "not found" in error_msg.lower():
            st.error(
                f"❌ **Groq Model Not Found**\n\n"
                f"The configured model is not available or your API key doesn't have access.\n\n"
                f"**Solutions:**\n"
                f"1. Verify your `GROQ_API_KEY` is valid and active\n"
                f"2. Check available models at https://console.groq.com/docs/models\n"
                f"3. Update the model names in `agents.py` if needed\n\n"
                f"**Error details:** {error_msg[:200]}"
            )
        elif "401" in error_msg or "Unauthorized" in error_msg or "Authentication" in error_msg:
            st.error(
                f"❌ **Authentication Failed**\n\n"
                f"Your Groq API key is invalid or expired.\n\n"
                f"**On Streamlit Cloud:**\n"
                f"1. Go to Manage app → Secrets\n"
                f"2. Update `GROQ_API_KEY` with a valid key from https://console.groq.com\n"
                f"3. Save and redeploy\n\n"
                f"**Error:** {error_msg[:200]}"
            )
        else:
            st.error(f"❌ **Error Running Pipeline**\n\n{error_msg}")


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="rule-thin"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("01 · Search Agent Output", expanded=False):
            st.markdown(f'<div class="result-raw">{r["search"]}</div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("02 · Reader Agent Output", expanded=False):
            st.markdown(f'<div class="result-raw">{r["reader"]}</div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown('<div class="result-label">03 · Final Research Report</div>', unsafe_allow_html=True)
        st.markdown('<div class="report-wrap">', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            label="↓  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown('<div class="result-label" style="color:#2a7a4b;border-bottom-color:#2a7a4b;">04 · Critic Feedback</div>', unsafe_allow_html=True)
        st.markdown('<div class="critic-wrap">', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="foot">
    ResearchMind · Multi-Agent Research Engine · Built with LangChain &amp; Streamlit
</div>
""", unsafe_allow_html=True)