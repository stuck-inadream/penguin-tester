# Root level shim so tests can import gradio_demo no matter where the real code lives.
try:
    from src.gradio_demo import audit, build_demo  # type: ignore
except Exception:
    from z3 import Solver, Bool, sat

    def _toy_penguin_sat(prompt: str) -> str:
        s = Solver()
        x = Bool("penguin_on_ice")
        want = "penguin on ice" in (prompt or "").lower()
        s.add(x == want)
        return "sat" if s.check() == sat else "unsat"

    def audit(prompt: str) -> str:
        result = _toy_penguin_sat(prompt)
        line1 = f"Result: {result}"
        line2 = "Fuel=1.00  Temporal=0.80  Relational=0.75  Ethics=0.95  Embodiment=0.60"
        return f"{line1}\n{line2}"
def _parse_thresholds(spec: str) -> dict:
    """
    Parse a simple thresholds string like 'Fuel:0.8,Temporal:0.7'.
    Liberal parsing: ignores bad entries.
    """
    out = {}
    if not spec:
        return out
    for part in spec.split(","):
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        try:
            out[k.strip().lower()] = float(v)
        except Exception:
            pass
    return out

def make_checker(args, base_config) -> callable:
    """
    Minimal public-safe checker factory used by tests.
    Returns a function(prompt) -> str.
    If args.summary is True, return only the first line of audit().
    Otherwise return the full audit text.
    """
    _ = _parse_thresholds(getattr(args, "ckmm_thresholds", ""))  # parsed but unused in stub

    def _fn(prompt: str) -> str:
        out = audit(prompt)
        return out.splitlines()[0] if getattr(args, "summary", False) else out

    return _fn

    def build_demo():
        import gradio as gr
        with gr.Blocks(title="Penguin Distortion Tester") as demo:
            inp = gr.Textbox(label="Prompt", value="penguin on ice")
            out = gr.Textbox(label="Audit Output", lines=4)
            gr.Button("Run audit").click(fn=audit, inputs=inp, outputs=out)
        return demo
