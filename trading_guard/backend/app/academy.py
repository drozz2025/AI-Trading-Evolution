from fastapi import APIRouter, Header, HTTPException
from .auth import user_id_from_token

router=APIRouter(prefix="/api/v1/academy",tags=["academy"])
LESSONS=[{"id":1,"title":"Fundamentos","topics":["velas","preço","tendência","contexto"]},{"id":2,"title":"Estrutura de mercado","topics":["HH","HL","LH","LL","mudança de estrutura"]},{"id":3,"title":"Liquidez","topics":["sweeps","máximos","mínimos"]},{"id":4,"title":"FVG / IFVG","topics":["identificação","validação","reteste"]},{"id":5,"title":"VWAP","topics":["posição relativa","contexto intraday"]},{"id":6,"title":"Confluências","topics":["estrutura","liquidez","IFVG","VWAP"]},{"id":7,"title":"Gestão de risco","topics":["risco por trade","drawdown","disciplina"]},{"id":8,"title":"Psicologia","topics":["impulsividade","revenge trading"]},{"id":9,"title":"Simulação","topics":["decisão","sem risco real"]},{"id":10,"title":"Trader autónomo","topics":["checklist","avaliação"]}]
def user(authorization):
 t=authorization.removeprefix('Bearer ').strip() if authorization else ''; uid=user_id_from_token(t)
 if not uid: raise HTTPException(401,'Authentication required')
 return uid
@router.get('/lessons')
def lessons(authorization:str|None=Header(default=None)):
 user(authorization); return {'lessons':LESSONS}
@router.get('/profile')
def profile(authorization:str|None=Header(default=None)):
 user(authorization); return {'scores':{'market_structure':86,'liquidity':71,'ifvg':63,'vwap':54,'risk_management':42},'progress':42,'recommended_lesson':{'id':2,'reason':'Confirmar estrutura antes de entrar num IFVG'}}
