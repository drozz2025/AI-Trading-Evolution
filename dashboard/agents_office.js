const $=s=>document.querySelector(s);
async function loadViveiro(){
 try{
  const r=await fetch('./viveiro_status.json?ts='+Date.now(),{cache:'no-store'}); if(!r.ok) throw Error(r.status);
  const d=await r.json();
  document.querySelectorAll('[data-v]').forEach(el=>{const k=el.dataset.v;if(k in d)el.textContent=d[k]});
  const live=$('#live-state'); if(live) live.textContent=d.live_trading_enabled?'LIVE ATIVO':'LAB / LIVE BLOQUEADO';
  const list=$('#task-list'); if(list){list.innerHTML=(d.tasks||[]).slice().reverse().map(t=>`<button class="task" data-task="${t.id}"><b>${t.agent_id||'SYSTEM'}</b><span>${t.type}</span><small>${t.status}</small></button>`).join('')||'<p>Sem tarefas persistidas.</p>';}
  const stamp=$('#updated'); if(stamp) stamp.textContent=d.updated_at?new Date(d.updated_at).toLocaleString('pt-PT'):'A aguardar primeiro ciclo';
 }catch(e){const s=$('#feed-state');if(s)s.textContent='Feed ainda não disponível';}
}
document.addEventListener('click',e=>{
 const nav=e.target.closest('[data-page]'); if(nav){document.querySelectorAll('[data-page]').forEach(x=>x.classList.remove('active'));nav.classList.add('active');document.querySelectorAll('.page').forEach(x=>x.hidden=true);const p=$('#page-'+nav.dataset.page);if(p)p.hidden=false;}
 const hub=e.target.closest('[data-hub]'); if(hub){const modal=$('#modal');modal.querySelector('h2').textContent=hub.dataset.hub;modal.querySelector('p').textContent='Departamento ligado ao Viveiro. Os dados serão atualizados pelo ciclo autónomo.';modal.showModal();}
});
loadViveiro();setInterval(loadViveiro,30000);
