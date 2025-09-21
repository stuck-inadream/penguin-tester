import pathlib

def test_readme_exists():
    assert (pathlib.Path(__file__).parents[1] / "README.md").exists()

def test_gradio_demo_import():
    # Import directly without using importlib to dodge local shadowing
    __import__("gradio_demo")
