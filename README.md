# 🔬 Multi-Agent AI Research System

> An autonomous research assistant where **four specialized AI agents collaborate** like a real research team — searching, reading, writing, and self-critiquing — to turn any topic into a reviewed report.

Built with **LangChain**, multi-agent orchestration, and tool calling. Runs from the terminal *or* a clean **Streamlit** web UI.

---

## ✨ What it does

Give it a topic. The system runs a 4-stage pipeline, fully autonomously:

| Stage | Agent | Job |
|-------|-------|-----|
| 1 | 🔍 **Search Agent** | Finds recent, reliable sources on the topic |
| 2 | 📖 **Reader Agent** | Picks the most relevant source and scrapes it for deeper content |
| 3 | ✍️ **Writer** | Drafts a structured report from the combined research |
| 4 | 🧐 **Critic** | Reviews the draft and returns feedback, like a human editor |

The output is a researched, written, and reviewed report — plus the critic's notes on how to improve it.

---

## 🧠 How it works

```
          ┌──────────────┐
 topic ─▶ │ Search Agent │ ─▶ search_results
          └──────────────┘
                  │
                  ▼
          ┌──────────────┐
          │ Reader Agent │ ─▶ scraped_content
          └──────────────┘
                  │
                  ▼
          ┌──────────────┐
          │    Writer    │ ─▶ report
          └──────────────┘
                  │
                  ▼
          ┌──────────────┐
          │    Critic    │ ─▶ feedback
          └──────────────┘
```

Each stage passes its output forward as context for the next — the core challenge (and fun) of agentic design is in this handoff.

---

## 🛠️ Tech Stack

- **Python**
- **LangChain** — agent & chain orchestration
- **Tool calling** — search + web scraping tools (see `tools.py`)
- **Streamlit** — web UI
- An LLM provider (e.g. OpenAI / Groq / Gemini — whatever your `agents.py` is wired to)

---

## 📁 Project Structure

```
Multi-Agent-AI-Research/
├── agents.py            # Builds the agents + chains (search, reader, writer, critic)
├── tools.py             # Tools the agents use (web search, scraping, etc.)
├── pipeline.py          # Core pipeline — runs the full flow in the terminal
├── streamlit_app.py     # Streamlit UI wrapper around the pipeline
├── requirements.txt     # Python dependencies
├── .env                 # API keys (NOT committed — see below)
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/shikeb1/Multi-Agent-AI-Research.git
cd Multi-Agent-AI-Research
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file in the project root:

```env
# 🔑 Adjust these to match the keys your agents.py / tools.py actually use
OPENAI_API_KEY=your_llm_api_key_here
TAVILY_API_KEY=your_search_api_key_here
```

> **Note:** Make sure `.env` is listed in your `.gitignore` so your keys are never pushed to GitHub.

---

## 💻 Usage

### Option A — Run in the terminal

```bash
python3 pipeline.py
```

You'll be prompted to enter a research topic, and each stage prints its progress and output as it runs.

### Option B — Run the Streamlit UI

```bash
streamlit run streamlit_app.py
```

Then open **http://localhost:8501** in your browser. Enter a topic, hit **Run research**, and watch each agent work — the final report, critic feedback, search results, and scraped content all appear in clean tabs, with a one-click report download.

---

## 🗺️ Roadmap

- [x] Core multi-agent pipeline (search → read → write → critique)
- [x] Streamlit UI
- [ ] **Live deployment** (in progress — target: within 2 days)
- [ ] Add report export (PDF / Markdown)
- [ ] Support multiple LLM providers via config
- [ ] Add a feedback loop (writer revises based on critic's notes)

---

## 🤝 Contributing

Issues, ideas, and pull requests are welcome. If you've built agentic systems and have thoughts on orchestration or context handoff between agents, I'd love to hear them.

---

## 📄 License

This project is open-source. *(Add your preferred license — e.g. MIT — and include a `LICENSE` file in the repo.)*

---

> Built by [@shikeb1](https://github.com/shikeb1) 🚀
