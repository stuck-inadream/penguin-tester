from z3 import Solver, Bool, sat

def test_z3_sat():
    s = Solver()
    x = Bool('x')
    s.add(x)
    assert s.check() == sat
