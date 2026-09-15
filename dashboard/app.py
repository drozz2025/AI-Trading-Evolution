import streamlit as st

from evolution.population import create_initial_population, population_summary

st.set_page_config(page_title="AI Trading Evolution", page_icon="◈", layout="wide")

agents = create_initial_population(size=20, capital=50.0)
summary = population_summary(agents)

st.markdown("""
<style>
.stApp {background: #06101d; color: #eef7ff;}
[data-testid="stMetric"] {background:#0a1b2c;border:1px solid #21435e;padding:14px;border-radius:12px;}
.office {position:relative;min-height:560px;border:1px solid #183d5b;border-radius:18px;padding:22px;background:radial-gradient(circle at 50% 48%,#0b4160 0,#09192a 34%,#06111e 75%);}
.brain {margin:55px auto 25px;width:220px;padding:28px;text-align:center;border:2px solid #21bfff;border-radius:22px;background:#092a40;box-shadow:0 0 35px #19baff;font-size:20px;font-weight:800;}
.hubs {display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.hub {background:#0b1a2ce8;border:1px solid #1d9ddd;border-radius:14px;padding:18px;min-height:130px;box-shadow:0 0 18px #071b2b;}
.hub.green{border-color:#12e69a}.hub.purple{border-color:#c85cff}.hub.red{border-color:#ff5c68}.hub.gold{border-color:#ffb429}
.hub b{font-size:16px}.hub small{color:#9fb5c8;line-height:1.7}.online{color:#4cffb4;font-weight:700}.caption{color:#9db1c7}
</style>
""", unsafe_allow_html=True)

st.markdown('<span class="online">● SISTEMA ONLINE</span>', unsafe_allow_html=True)
st.title("AGENTS OFFICE")
st.markdown('<div class="caption">AI Trading Evolution · Viveiro autónomo · Pesquisa → Backtest → Validação → Arena → Evolução</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Agentes", summary["total"])
c2.metric("Vivos", summary["alive"])
c3.metric("Capital Virtual", f"€{summary['capital']:.2f}")
c4.metric("Geração", f"#{summary['generations']}")
c5.metric("Promovidos", summary["promoted"])

st.markdown(f'''<div class="office">
<div class="brain">◉<br>THE BRAIN<br><small>Coordenação & Decisões</small></div>
<div class="hubs">
<div class="hub gold"><b>◉ RESEARCH & DATA</b><br><small>Agentes disponíveis: {summary['alive']}<br>Researching: {summary['researching']}<br>Criação de hipóteses e recolha de dados</small></div>
<div class="hub green"><b>✦ RESEARCH HUB</b><br><small>População: {summary['total']}<br>Capital: €{summary['capital']:.2f}<br>Pesquisa de novas estratégias</small></div>
<div class="hub"><b>⌘ DEVELOPMENT</b><br><small>Transforma hipóteses em estratégias testáveis<br>Preparado para geração de EAs</small></div>
<div class="hub purple"><b>⬡ RISK & COMPLIANCE</b><br><small>Retirados: {summary['retired']}<br>Penalização de drawdown<br>Gates de segurança</small></div>
<div class="hub red"><b>▥ BACKTEST ARENA</b><br><small>Backtesting: {summary['backtesting']}<br>Arena: {summary['arena']}<br>Sobrevivência por desempenho</small></div>
<div class="hub"><b>⚙ EVOLUTION LAB</b><br><small>Validação: {summary['validating']}<br>Promovidos: {summary['promoted']}<br>Reprodução e mutação dos sobreviventes</small></div>
</div></div>''', unsafe_allow_html=True)

st.subheader("Estado real da população")
st.dataframe([
    {"Agente": a.agent_id, "Geração": a.generation, "Estado": a.status.value,
     "Capital": f"€{a.balance:.2f}", "Estratégia": a.strategy_id or "Researching",
     "Pai": getattr(a, "parent_id", None) or "CEO Seed"}
    for a in agents
], use_container_width=True, hide_index=True)

st.subheader("Pipeline do Viveiro")
p1,p2,p3,p4,p5 = st.columns(5)
p1.metric("Research", summary["researching"])
p2.metric("Backtest", summary["backtesting"])
p3.metric("Validation", summary["validating"])
p4.metric("Arena", summary["arena"])
p5.metric("Promoted", summary["promoted"])

st.info("LABORATORY MODE — sem ordens live. Os números desta página são calculados pelo motor de população do Viveiro; resultados de backtest/evolução só aparecem quando os ciclos são executados e persistidos.")
