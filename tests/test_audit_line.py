from gradio_demo import audit

def test_audit_first_line_only():
    first = audit("penguin on ice").splitlines()[0]
    assert first == "Result: sat"
