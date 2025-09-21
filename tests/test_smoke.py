import importlib.util
import pathlib

def test_readme_exists():
    assert (pathlib.Path(__file__).parents[1] / "README.md").exists()

def test_gradio_demo_module_is_present():
    # this does not import the module, so it will not run code or need deps
    spec = importlib.util.find_spec("gradio_demo")
    assert spec is not None
