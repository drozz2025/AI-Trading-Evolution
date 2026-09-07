# BLS Test API

API de simulação para testar o EA com eventos económicos em datas/horas controladas.

O objetivo é permitir testes em conta demo sem depender do calendário real.

## Formato do evento

```json
{
  "id": "TEST-PPI-001",
  "event": "PPI",
  "country": "USD",
  "scheduled_time": "2026-09-07T23:00:00+01:00",
  "forecast": 0.2,
  "actual": 0.5,
  "previous": 0.1,
  "status": "scheduled"
}
```

## Como testar

Os eventos ficam em `bls-test/events.json`. Altera `scheduled_time`, `forecast`, `actual` e `previous` para criar quantos cenários quiseres.

A API de produção do EA deverá apontar para o endpoint de teste quando estiveres a fazer estas simulações.
