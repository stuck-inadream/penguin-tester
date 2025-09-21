from z3 import Solver, Bool, sat
import gradio_demo as gd


def test_z3_basic():
    s = Solver()
    x = Bool("x")
    s.add(x == True)
    assert s.check() == sat


def test_audit_text_paths():
    text_sat = "penguin on ice"
    text_unsat = "penguin on sand"
    out_sat = gd.audit(text_sat)
    out_unsat = gd.audit(text_unsat)
    assert "Result: sat" in out_sat
    assert "Result: unsat" in out_unsat
