"""
streamlit_app.py
----------------
A Streamlit UI for the Multi-Agent AI Research System.

The heavy lifting (search agent, reader agent, writer chain, critic chain)
already lives in your project. This file just imports those pieces and
re-runs the SAME 4-step flow that run_research_pipeline() does in
pipeline.py -- except instead of print()-ing to the terminal, it streams
each step's progress and results into a web UI.

HOW TO RUN
----------
1. Put this file in the SAME folder as agents.py / pipeline.py / tools.py
   (so the "from agents import ..." line resolves correctly).
2. Install streamlit inside your venv:
       pip install streamlit
3. Run it from the project folder (WSL terminal is fine):
       streamlit run streamlit_app.py
4. Your browser opens at http://localhost:8501
"""

import streamlit as st

# Same imports your pipeline.py already uses
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
)


# ----------------------------------------------------------------------
# Build the agents only ONCE per session (not on every Streamlit rerun).
# st.cache_resource is the right tool for non-serializable objects like
# LLM agents / clients / connections.
# ----------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_search_agent():
    return build_search_agent()


@st.cache_resource(show_spinner=False)
def get_reader_agent():
    return build_reader_agent()


# ----------------------------------------------------------------------
# The pipeline -- identical logic to run_research_pipeline() in pipeline.py,
# but each step reports its progress to the UI via st.status().
# ----------------------------------------------------------------------
def run_research_pipeline_ui(topic: str) -> dict:
    state = {}

    # ---- Step 1: Search agent ----
    with st.status("🔍  Step 1 — Search agent gathering sources…", expanded=False) as status:
        search_agent = get_search_agent()
        search_result = search_agent.invoke({
            "messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]
        })
        state["search_results"] = search_result["messages"][-1].content
        status.update(label="✅  Step 1 — Search complete", state="complete")

    # ---- Step 2: Reader agent ----
    with st.status("📖  Step 2 — Reader agent scraping top resources…", expanded=False) as status:
        reader_agent = get_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [
                ("user",
                 f"Based on the following search results about '{topic}', "
                 f"pick the most relevant URL and scrape it for deeper content.\n\n"
                 f"Search Results:\n{state['search_results'][:800]}")
            ]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
        status.update(label="✅  Step 2 — Scraping complete", state="complete")

    # ---- Step 3: Writer chain ----
    with st.status("✍️  Step 3 — Writer drafting the report…", expanded=False) as status:
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
        status.update(label="✅  Step 3 — Report drafted", state="complete")

    # ---- Step 4: Critic chain ----
    with st.status("🧐  Step 4 — Critic reviewing the report…", expanded=False) as status:
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })
        status.update(label="✅  Step 4 — Review complete", state="complete")

    return state


# ----------------------------------------------------------------------
# Sidebar — input controls
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("Run a research task")
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Latest advances in solid-state batteries",
    )
    run = st.button(
        "🚀  Run research",
        type="primary",
        use_container_width=True,
        disabled=not topic.strip(),
    )

    st.divider()
    st.markdown("**Pipeline stages**")
    st.markdown(
        "1. 🔍 Search agent\n"
        "2. 📖 Reader agent\n"
        "3. ✍️ Writer\n"
        "4. 🧐 Critic"
    )
    if st.button("🗑️  Clear results", use_container_width=True):
        st.session_state.pop("last_state", None)
        st.session_state.pop("last_topic", None)
        st.rerun()


# ----------------------------------------------------------------------
# Main area
# ----------------------------------------------------------------------
st.title("🔬 Multi-Agent AI Research System")
st.caption("Search → Read → Write → Critique · powered by your LangChain agents")

# Trigger a run
if run and topic.strip():
    try:
        state = run_research_pipeline_ui(topic.strip())
        st.session_state["last_state"] = state
        st.session_state["last_topic"] = topic.strip()
    except Exception as e:
        st.error(f"Something went wrong while running the pipeline:\n\n```\n{e}\n```")
        st.stop()

# Show results (persist across reruns via session_state)
if "last_state" in st.session_state:
    state = st.session_state["last_state"]
    done_topic = st.session_state.get("last_topic", "")
    st.success(f"Research complete for: **{done_topic}**")

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown(str(state.get("report", "_No report generated._")))
        st.download_button(
            "⬇️  Download report (.md)",
            data=str(state.get("report", "")),
            file_name=f"{done_topic.replace(' ', '_')[:40] or 'report'}_report.md",
            mime="text/markdown",
        )

    with tab_critic:
        st.markdown(str(state.get("feedback", "_No feedback generated._")))

    with tab_search:
        st.markdown(str(state.get("search_results", "_No search results._")))

    with tab_scraped:
        st.markdown(str(state.get("scraped_content", "_No scraped content._")))

else:
    st.info("Enter a topic in the sidebar and click **Run research** to begin.")