# Deployment

## Local
```bash
pip install -r requirements.txt
python gradio_demo.py --summary
```

## Server
```bash
python gradio_demo.py --server_name 0.0.0.0 --server_port 7860 --summary
```

## CI
GitHub Actions workflow at `.github/workflows/ci.yml` runs `pytest -q`.
