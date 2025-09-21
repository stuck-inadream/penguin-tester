# Penguin Distortion Tester (v560L • CKMM • Disclose)

[![CI](https://github.com/stuck-inadream/penguin-tester/actions/workflows/ci.yml/badge.svg)](https://github.com/stuck-inadream/penguin-tester/actions)
[![HF Space](https://img.shields.io/badge/%F0%9F%A4%97%20Spaces-Penguin%20Distortion%20Tester-blue)](https://huggingface.co/spaces/stuck-inadream/penguin-distortion-tester)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**What this is.** A minimal, public-safe harness to *audit symbolic distortion* on a toy “Penguin” task, show SAT/UNSAT behavior (via **Z3**), and report **CKMM-L** context metrics:

- **Fuel (Energy–Resource):** wall time + peak KiB (tracemalloc) + human-attention ticks  
- **Temporal Coherence:** replay stability ratio  
- **Relational Field:** council agreement vs. drift (majority vote placeholder)  
- **Ethical Constraints:** regex penalties + recovery flag  
- **Embodiment:** device/substrate capture with validated hint  

This repo is a **disclose build**: it lists exactly what a prior reviewer saw — **no more, no less** — and keeps proprietary weighting/heuristics private.

---

## Quickstart

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run: summary UI, 100k iterations, explicit port
PYTHONUNBUFFERED=1 python gradio_demo.py --summary --ckmm-iterations 100000 --server_port 7860
# Open http://127.0.0.1:7860  (use --share for a temporary public link)

⚠️ Heads-up: --share exposes a public URL. Treat it as untrusted. Do not upload sensitive data.

Features (public-safe)
“Penguin” symbolic check (baseline sat, forced unsat via contradiction trigger)
Distortion score toy formula: modal × diversity (toy numbers disclosed below)
CKMM-L interfaces only (no proprietary internals)
Configurable workload and thresholds:
--ckmm-iterations N (CPU loop; default documented below)
--ckmm-thresholds '{"fuel":{"max_time_s":2.0}}' (JSON Schema-validated)
--ckmm-verbose (pretty JSON)
Logging: rotating errors.log + console level via --log-level
CI: pytest via GitHub Actions

Public Disclosure Parity (Seen-by-Reviewer Appendix)
What’s explicitly disclosed here was previously visible to a reviewer:
Score formula modal × diversity; diversity = avg edit distance; toy values 0.33 × 2 = 0.66
Load fractions 1.0 / 0.6 / 0.7, divergence = 0.3
HSIL policy names: prefer_specific_over_general, safety_first, audit_bias
Z3 baseline sat; forced contradiction → unsat; heatmap.png modal plot
Gradio flags (server name/port), log level, rotating logs
CI + tests, CKMM-L interfaces (fuel / temporal / council / ethics / embodiment)
Not disclosed: proprietary weighting/aggregation schemes, true diversity/council math beyond placeholders, production energy models, or internal heuristics.

FAQ
Is this just a toy?
Yes — by design. It’s a teaching harness that’s easy to run, safe to share, and useful for audits.
Can I tune workloads?
Yes — use --ckmm-iterations (e.g., 5_000_000 for measurable fuel) and thresholds via --ckmm-thresholds JSON.
Does --share upload my data?
No uploads unless you explicitly make them; --share only exposes a temporary Gradio URL. Treat it as public.

Development & Tests
pip install -r requirements.txt
pytest -q

Roadmap & Contributions
Add screenshot(s) of the UI (docs/screenshot.png)
Pin dependencies in requirements.txt for CI stability (already pinned)
CI improvements: multi-stage (lint then test) with pip cache (already caching pip)
Optional: package-ready entry point (pyproject.toml) for pipx run penguin-tester
Contributions welcome! See CONTRIBUTING.md.

MIT © stuck-inadream

Screenshot
<img width="1234" height="750" alt="Screenshot 2025-09-21 at 9 28 02 AM" src="https://github.com/user-attachments/assets/3d0d0b21-539d-4f63-90b1-67b719130949" />
