import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "update_live_consensus.py"
SPEC = importlib.util.spec_from_file_location("update_live_consensus", MODULE_PATH)
update_live_consensus = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(update_live_consensus)


def test_main_leaves_file_unchanged_when_no_target_events(monkeypatch, tmp_path, capsys):
    out = tmp_path / "live-consensus.json"
    out.write_text("{\"keep\": true}\n", encoding="utf-8")

    xml = b"""
<weeklyevents>
  <event>
    <country>USD</country>
    <title>Retail Sales m/m</title>
    <date>09-14-2026</date>
    <forecast>0.3%</forecast>
    <previous>0.1%</previous>
  </event>
</weeklyevents>
"""

    monkeypatch.setattr(update_live_consensus, "fetch_calendar_xml", lambda: xml)
    monkeypatch.setattr(update_live_consensus, "OUT", out)

    assert update_live_consensus.main() == 0
    assert out.read_text(encoding="utf-8") == "{\"keep\": true}\n"
    assert "leaving current feed unchanged" in capsys.readouterr().out


def test_main_writes_payload_when_target_event_is_present(monkeypatch, tmp_path):
    out = tmp_path / "live-consensus.json"
    xml = b"""
<weeklyevents>
  <event>
    <country>USD</country>
    <title>CPI y/y</title>
    <date>09-14-2026</date>
    <forecast>2.9%</forecast>
    <previous>2.8%</previous>
  </event>
</weeklyevents>
"""

    monkeypatch.setattr(update_live_consensus, "fetch_calendar_xml", lambda: xml)
    monkeypatch.setattr(update_live_consensus, "OUT", out)

    assert update_live_consensus.main() == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["events"] == [
        {
            "currency": "USD",
            "type": "CPI",
            "title": "CPI y/y",
            "date": "2026-09-14",
            "forecast": 2.9,
            "previous": 2.8,
        }
    ]
