from evolution.hypothesis_engine import HypothesisEngine
from evolution.research_roles import ResearchRole


def test_engine_generates_and_mutates_hypotheses():
    engine = HypothesisEngine(seed=1)
    parent = engine.generate("R-0001", ResearchRole.REGIME)
    child = engine.mutate(parent, "R-0002")

    assert parent.hypothesis_id != child.hypothesis_id
    assert parent.role == child.role
    assert child.name != parent.name
    assert len(engine.archive.seen) == 2
