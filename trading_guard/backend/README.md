# Trading Guard API

Cloud API for Trading Guard. The current release is intentionally **read-only**: it can monitor an MT5 account through MetaApi and calculate risk/behaviour signals, but it has no order-placement or order-closing endpoint.

## Environment

- `METAAPI_TOKEN` — server-side secret; never commit it.
- `METAAPI_PROVISIONING_URL` — MetaApi provisioning endpoint.
- `METAAPI_CLIENT_BASE_URL` — MetaApi client endpoint.

## Run locally

```bash
pip install -e '.[test]'
uvicorn app.main:app --reload --port 8000
pytest -q
```

## Cloud

The repository root `render.yaml` provisions the Docker service. Set `METAAPI_TOKEN` as a secret in the cloud provider. Do not place credentials in the frontend or GitHub source.

## Safety boundary

The API exposes account/position reads and risk assessment only. Live execution must be added as a separate, explicitly gated capability after DEMO validation, with authentication, audit logging, position limits, and a kill switch.
