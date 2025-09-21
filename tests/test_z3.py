from z3 import Solver, Bool, sat

def test_z3_basic_sat():
    s = Solver()
    x = Bool("x")
    s.add(x == True)
    assert s.check() == sat
