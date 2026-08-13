from pathlib import Path
import json


def load_results(path: str = "artifacts/lab_results.json") -> list[dict]:
    file = Path(path)
    if not file.exists():
        return []
    return json.loads(file.read_text())
