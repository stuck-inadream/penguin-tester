import importlib.util
import pathlib

def test_readme_exists():
    assert (pathlib.Path(__file__).parents[1] / "README.md").exists()

def test_demo_imports():
    # Should import without importing gradio (UI import is lazy)
    spec = importlib.util.find_spec("gradio_demo")
    assert spec is not None
