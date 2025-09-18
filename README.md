---
title: Penguin Distortion Tester
sdk: gradio
app_file: gradio_demo.py
pinned: false
license: mit
---

Penguin Distortion Tester (v560L • CKMM • Disclose)

Quickstart
1) python3.11 -m venv .venv
2) source .venv/bin/activate
3) python -m pip install --upgrade pip
4) pip install -r requirements.txt
5) python gradio_demo.py --summary --ckmm-iterations 100000 --server_port 7860

Open http://127.0.0.1:7860
For a public link add: --share
Tested on macOS with Python 3.11

### Public share
Run with `--share` to get a temporary gradio.live URL.

---

### Penguin Distortion Tester — how to run

[![HF Space](https://img.shields.io/badge/%F0%9F%A4%97%20Spaces-Penguin%20Distortion%20Tester-blue)](https://huggingface.co/spaces/stuck-inadream/penguin-distortion-tester)

#### Local quickstart
```bash
# from repo root
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# run (auto-summarize UI, 100k iterations, choose a port)
env PYTHONUNBUFFERED=1 python gradio_demo.py --summary --ckmm-iterations 100000 --server_port 7860

md

---

### Penguin Distortion Tester — how to run

[![HF Space](https://img.shields.io/badge/%F0%9F%A4%97%20Spaces-Penguin%20Distortion%20Tester-blue)](https://huggingface.co/spaces/stuck-inadream/penguin-distortion-tester)

#### Local quickstart
```bash
# from repo root
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# run (auto-summarize UI, 100k iterations, choose a port)
env PYTHONUNBUFFERED=1 python gradio_demo.py --summary --ckmm-iterations 100000 --server_port 7860

```          ← closes the code block (type three backticks)
MD            ← closes the heredoc

```
