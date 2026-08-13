import streamlit as st

from evolution.population import create_initial_population, population_summary

st.set_page_config(page_title="AI Trading Evolution", page_icon="◈", layout="wide")
st.title("AI Trading Evolution")
st.caption("XAUUSD • Research Command Center • LABORATORY MODE")

agents = create_initial_population()
summary = population_summary(agents)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Agents", summary["total"])
c2.metric("Alive", summary["alive"])
c3.metric("Retired", summary["retired"])
c4.metric("Virtual Capital", f"€{summary['capital']:.2f}")
c5.metric("Promoted", 0)

st.divider()

left, right = st.columns([1, 1])
with left:
    st.subheader("Organization")
    st.markdown("**MASTER AI / CEO**")
    st.markdown("└── **RESEARCH DIRECTOR**")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;├── Market Structure Team", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;├── Regime Team", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;├── Volatility Team", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;├── Momentum Team", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;├── Cross-Asset Team", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;└── **RISK DIRECTOR**", unsafe_allow_html=True)
with right:
    st.subheader("Research Pipeline")
    pipeline = [
        {"Stage": "Researching", "Agents": summary["total"]},
        {"Stage": "Backtesting", "Agents": 0},
        {"Stage": "Adversarial", "Agents": 0},
        {"Stage": "Validating", "Agents": 0},
        {"Stage": "Arena", "Agents": 0},
        {"Stage": "Promoted", "Agents": 0},
    ]
    st.dataframe(pipeline, use_container_width=True, hide_index=True)

st.subheader("Agent Organization")
st.dataframe(
    [
        {
            "Agent": a.agent_id,
            "Generation": a.generation,
            "Status": a.status.value,
            "Balance": a.balance,
            "Strategy": a.strategy_id or "Researching",
            "Parent": getattr(a, "parent_id", None) or "CEO Seed",
        }
        for a in agents
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Research Arena")
st.info("No strategies promoted yet. This panel will populate when the historical backtest and validation pipeline produces candidates that survive every gate.")

st.subheader("Evolution Rules")
st.markdown("- Agents generate hypotheses rather than relying on RSI-only rules.")
st.markdown("- Survivors can reproduce and mutate controlled parameters.")
st.markdown("- Adversarial testing attempts to break promising candidates.")
st.markdown("- Validation must remain separated from research data.")
st.markdown("- Live trading is disabled in laboratory mode.")

st.info("Simulation only. No live orders are enabled in this prototype.")
