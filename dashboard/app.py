import streamlit as st

from evolution.population import create_initial_population, population_summary


st.set_page_config(page_title="AI Trading Evolution", page_icon="◈", layout="wide")
st.title("AI Trading Evolution")
st.caption("XAUUSD • Simulation Command Center")

agents = create_initial_population()
summary = population_summary(agents)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Agents", summary["total"])
c2.metric("Alive", summary["alive"])
c3.metric("Retired", summary["retired"])
c4.metric("Virtual Capital", f"€{summary['capital']:.2f}")

st.subheader("Organization")
st.markdown("**MASTER AI**")
st.markdown("└── **TRADING DIRECTOR**")
st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;├── Team A — 10 research traders", unsafe_allow_html=True)
st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;└── **RISK DIRECTOR** — deterministic risk controls", unsafe_allow_html=True)

st.subheader("Initial Population")
st.dataframe(
    [
        {
            "Agent": a.agent_id,
            "Generation": a.generation,
            "Status": a.status.value,
            "Balance": a.balance,
            "Strategy": a.strategy_id or "Researching",
        }
        for a in agents
    ],
    use_container_width=True,
    hide_index=True,
)

st.info("Simulation only. No live orders are enabled in this prototype.")
