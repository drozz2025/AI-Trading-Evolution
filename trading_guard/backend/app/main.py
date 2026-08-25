from fastapi import FastAPI

app = FastAPI(title="Trading Guard API", version="0.1.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "trading-guard-api"}

@app.get("/api/v1")
def api_root() -> dict[str, str]:
    return {"name": "Trading Guard", "mode": "read-only MVP"}
