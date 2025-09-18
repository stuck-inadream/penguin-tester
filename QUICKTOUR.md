# Quick Tour

```bash
# 1. Demo with summary
python gradio_demo.py --summary

# 2. See JSON details
python gradio_demo.py --json

# 3. Adaptive repair
python gradio_demo.py --summary --adaptive --adaptive-eta 0.15

# 4. Real data stubs with seed
python gradio_demo.py --summary --real-data --seed 7

# 5. Generate a synthetic pack and run
python tools/synth_corpus.py
python gradio_demo.py --summary --real-data --seed 11

# 6. Challenge scorer (adaptive EMA)
echo '{"myth_yes_bias":0.7,"exception_no_bias":0.6,"empty_yes_bias":0.9,"divergence":0.3}' | python challenges/leaderboard.py --adaptive
```
