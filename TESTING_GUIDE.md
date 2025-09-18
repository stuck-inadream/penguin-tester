# Testing Guide (v5.6.0L-CKMM-D)

## Objectives
- Confirm demo runs across OSes (Windows/macOS/Linux)
- Validate summary output, notebooks, and tests
- Assess performance & GPU status if available

## Steps
1) `pip install -r requirements.txt`
2) `python gradio_demo.py --summary`
3) Open `examples/*.ipynb` in Jupyter and run all cells
4) `pytest -q`
5) Optional: `python challenges/leaderboard.py --adaptive <<< '{"myth_yes_bias":0.7,"exception_no_bias":0.6,"empty_yes_bias":0.9,"divergence":0.3}'`

## Report
- OS / Python / GPU
- What worked / What confused you
- Attach errors/logs if any
