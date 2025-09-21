import gradio_demo as gd

def test_audit_first_line_only():
    first = gd.audit("penguin on ice").splitlines()[0]
    assert first == "Result: sat"
