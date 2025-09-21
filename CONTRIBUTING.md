# Contributing

Thanks for helping improve Penguin Distortion Tester!

## Dev setup
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

Running locally
python gradio_demo.py --server_port 7860

Tests
pytest -q

Commit style
Small, focused commits.
Conventional messages if possible (feat:, fix:, docs:, ci:, chore:).
Pull requests
Fork and create a feature branch.
Add tests for new behavior when applicable.
Run pytest locally.
Open a PR; the CI must pass.
(Optional) add `CODE_OF_CONDUCT.md` later if you want.
# 5) Repository “About” → Website URL
Use your **Hugging Face Space** as the Website:
---

https://huggingface.co/spaces/stuck-inadream/penguin-distortion-tester

(If it’s sleeping, still fine; you can wake it later. Or use a GitHub Pages README anchor for now.)
---
# 6) Fast path to “10/10”
- **CI green** with the fix pack above.
- **README**: use the clean, badge-based header you drafted (good).
- **Screenshot**: keep the image (great for instant comprehension).
- **One runnable demo**: make sure `gradio_demo.py` imports and runs without optional flags.
- **At least one real test**: after smoke, add a tiny Z3 test:
  ```python
  from z3 import Solver, Bool, sat
  def test_z3_sat():
      s = Solver(); x = Bool('x'); s.add(x)
      assert s.check() == sat

Issues: open a few “good first issue” tickets (docs, small enhancements). This signals life.

7) If the run still fails
Click the failed job → “Run tests (verbose)” step → copy the error message.
Common culprits:
Wrong path: fixed by pytest.ini
Missing deps: fixed by pinned requirements.txt
Python not finding pytest: fixed by python -m pytest
A test import error: CI log will show the exact module name—add to requirements or fix the import.

