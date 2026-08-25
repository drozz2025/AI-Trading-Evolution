from app.behaviour import detect_behaviour

def test_revenge_risk():
    signals = detect_behaviour(2, 2, 0.1, 0.1)
    assert any(s.code == "revenge_risk" for s in signals)

def test_size_jump():
    signals = detect_behaviour(1, 0, 0.3, 0.1)
    assert any(s.code == "size_jump" for s in signals)

def test_overtrading():
    signals = detect_behaviour(5, 0, 0.1, 0.1)
    assert any(s.code == "overtrading_risk" for s in signals)
