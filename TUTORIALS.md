# Tutorials

## Add a custom constraint
1. Open `config/constraints.sample.yaml` and append:
   ```yaml
   - name: no_profanity
     pattern: "(?i)\bdarn\b"
     penalty: 2
   ```
2. Run:
   ```bash
   python gradio_demo.py --summary --ckmm-thresholds '{"ethics":{"max_penalty":0}}'
   ```
3. Enter a prompt containing `darn` and observe `penalty > 0` in the summary.

## Try DuPO + Aggregation
```python
from src.reward_cvr import CVRReward, DuPOSelfVerifier
from src.aggregator_policy import AggregatorPolicy
cvr = CVRReward.load("configs/cvr_dopo.yaml")
dupo = DuPOSelfVerifier()
cands = ["yes","no","yes","yes"]
rewards = [cvr.score("do penguins fly?", a) for a in cands]
print("dupo:", dupo.dual_check("q", cands))
print("agg:", AggregatorPolicy().aggregate(cands, rewards, {}))
```

## Generate a synth pack
```bash
python tools/synth_corpus.py --seed 13 --outdir data/synth
cat data/synth/rules.yaml | head
```
