import base64
import json
import os
from urllib.request import Request, urlopen
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from .auth import user_id_from_token

router = APIRouter(prefix="/api/v1/vision", tags=["vision"])

class ChartImageRequest(BaseModel):
    image_data_url: str = Field(min_length=100, max_length=15_000_000)
    symbol: str = Field(default="XAUUSD", max_length=30)
    timeframe: str = Field(default="M5", max_length=10)


def _require_user(authorization: str | None) -> int:
    token = authorization.removeprefix("Bearer ").strip() if authorization else ""
    uid = user_id_from_token(token)
    if not uid:
        raise HTTPException(401, "Authentication required")
    return uid


def _call_openai(payload: ChartImageRequest) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    model = os.getenv("OPENAI_VISION_MODEL", "gpt-5.6-luna")
    instructions = (
        "You are the Trading Guard chart-analysis engine. Analyze the supplied TradingView screenshot. "
        "Focus on visible market structure, HH/HL/LH/LL, liquidity sweeps, FVG/IFVG, VWAP if visible, "
        "momentum and obvious invalidation. Do not invent indicators that are not visible. "
        "Return ONLY valid JSON with keys: signal, confidence, summary, reasons, invalidation. "
        "signal must be BUY, SELL, or WAIT. confidence is an integer 0-100. "
        "This is analysis, not a guarantee or an instruction to execute a trade."
    )
    body = {
        "model": model,
        "input": [{
            "role": "user",
            "content": [
                {"type": "input_text", "text": f"Symbol: {payload.symbol}. Timeframe: {payload.timeframe}. {instructions}"},
                {"type": "input_image", "image_url": payload.image_data_url},
            ],
        }],
    }
    request = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode())
    text = result.get("output_text", "").strip()
    if not text:
        raise RuntimeError("Vision model returned no text")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise RuntimeError("Vision model returned invalid JSON")
        parsed = json.loads(text[start:end + 1])
    signal = str(parsed.get("signal", "WAIT")).upper()
    if signal not in {"BUY", "SELL", "WAIT"}:
        signal = "WAIT"
    return {
        "signal": signal,
        "confidence": max(0, min(100, int(parsed.get("confidence", 0)))),
        "summary": str(parsed.get("summary", "")),
        "reasons": parsed.get("reasons", []) if isinstance(parsed.get("reasons", []), list) else [],
        "invalidation": str(parsed.get("invalidation", "")),
        "model": model,
    }


@router.post("/chart")
def analyze_chart(payload: ChartImageRequest, authorization: str | None = Header(default=None)):
    _require_user(authorization)
    if not payload.image_data_url.startswith("data:image/"):
        raise HTTPException(400, "image_data_url must be a data:image/... URL")
    try:
        base64.b64decode(payload.image_data_url.split(",", 1)[1], validate=True)
        return _call_openai(payload)
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(502, "Unable to analyze chart image") from exc
