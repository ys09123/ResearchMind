# Researcher — Multi-Agent AI Research Engine

A Streamlit application that orchestrates four specialized AI agents to search, extract, write, and critique a polished research report on any topic — in seconds.

---

## Overview

Researcher chains four LangChain-powered agents into a sequential pipeline. You provide a topic; the pipeline handles everything from raw web search to a reviewed, downloadable report.

```
Search Agent → Reader Agent → Writer Chain → Critic Chain
```

Each stage feeds its output into the next, so the final report is grounded in real, freshly-scraped sources and then independently reviewed for accuracy and quality.

---

## Features

- **Four-agent pipeline** — search, scrape, write, and critique run automatically in sequence
- **Live pipeline status** — each agent step shows Queued / Running / Done in real time
- **Downloadable report** — export the final report as a `.md` file
- **Critic feedback** — a separate review agent scores and comments on the report
- **Editorial UI** — clean, paper-toned interface with serif typography; easy to read and present

---

## Tech Stack

| Layer | Library / Service |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| Agent framework | [LangChain](https://python.langchain.com) |
| LLM | [Groq](https://groq.com) (via `langchain-groq`) |
| Search | [Tavily](https://tavily.com) (via `langchain-tavily`) |
| Scraping | LangChain Reader / web scraper tool |

---

## Project Structure

```
├── app.py          # Streamlit UI — layout, styling, pipeline orchestration
├── agents.py       # Agent and chain definitions
│   ├── build_search_agent()
│   ├── build_reader_agent()
│   ├── writer_chain
│   └── critic_chain
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/researcher.git
cd researcher
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the project root:

```env
# Groq — LLM provider
GROQ_API_KEY=your_groq_api_key

# Tavily — web search
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

### Stage 1 — Search Agent
Queries the web using **Tavily Search** for recent, reliable information on the given topic. Tavily is optimized for LLM-based research — it returns clean, structured results with summaries and source URLs rather than raw HTML.

### Stage 2 — Reader Agent
Takes the top search results, picks the most relevant URL, and scrapes the full page content for deeper context beyond the snippet.

### Stage 3 — Writer Chain
Combines the search results and scraped content, then prompts a **Groq-hosted LLM** to produce a comprehensive, well-structured research report in Markdown format. Groq's inference speed makes this step near-instant even for long reports.

### Stage 4 — Critic Chain
Independently reviews the written report using **Groq**, returning qualitative feedback — assessing accuracy, coverage, clarity, and suggesting improvements.

---

## Configuration

Agent behaviour and prompts are defined in `agents.py`. Common things to customize:

- **Groq model** — swap the model name in the chain definitions (e.g. `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`, `gemma2-9b-it`)
- **Tavily search depth** — set `search_depth="advanced"` in the Tavily tool for more thorough results
- **Prompt templates** — adjust writer and critic prompts to change report style, length, or focus
- **Max tokens** — tune per chain to control output length

---

## Requirements

```
streamlit>=1.35.0
langchain>=0.2.0
langchain-groq>=0.1.0
langchain-community>=0.2.0
langchain-tavily>=0.1.0
python-dotenv>=1.0.0
```

---

## License

MIT — free to use, modify, and distribute.

---

Build with ❤️ by Yash.
