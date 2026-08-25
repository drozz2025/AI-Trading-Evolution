const screens = ['welcome','dashboard','risk','positions','profile'];
function show(name){
  document.querySelectorAll('[data-screen]').forEach(e=>e.hidden=e.dataset.screen!==name);
  document.querySelectorAll('nav button').forEach(e=>e.classList.toggle('active',e.dataset.go===name));
}
async function load(){
 const [a,p]=await Promise.all([fetch('/api/v1/demo/account').then(r=>r.json()),fetch('/api/v1/demo/positions').then(r=>r.json())]);
 document.getElementById('balance').textContent=`€${a.account.balance.toFixed(2)}`;
 document.getElementById('equity').textContent=`€${a.account.equity.toFixed(2)}`;
 document.getElementById('pnl').textContent=`€${a.account.daily_pnl.toFixed(2)}`;
 document.getElementById('risk').textContent=a.account.daily_pnl < 0 ? 'ATENÇÃO' : 'OK';
 document.getElementById('positions').innerHTML=p.positions.map(x=>`<div class="position"><b>${x.symbol} ${x.side}</b><span>${x.volume} lot</span><strong>€${x.profit.toFixed(2)}</strong></div>`).join('');
 document.getElementById('alerts').innerHTML=(a.behaviour||[]).map(x=>`<div class="alert"><b>${x.code}</b><br>${x.message}</div>`).join('')||'<div class="safe">Nenhum alerta</div>';
}
document.addEventListener('click',e=>{if(e.target.dataset.go)show(e.target.dataset.go);if(e.target.id==='demo')show('dashboard')});
load();show('welcome');
