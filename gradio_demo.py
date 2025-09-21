from z3 import Solver, Bool, sat

def _toy_penguin_sat(prompt: str) -> str:
    s = Solver()
    x = Bool("penguin_on_ice")
    want = "penguin on ice" in (prompt or "").lower()
    s.add(x == want)
    return "sat" if s.check() == sat else "unsat"

def audit(prompt: str) -> str:
    result = _toy_penguin_sat(prompt)
    # fixed stable stub numbers
    line1 = f"Result: {result}"
    line2 = "Fuel=1.00  Temporal=0.80  Relational=0.75  Ethics=0.95  Embodiment=0.60"
    return f"{line1}\n{line2}"

def build_demo():
    import gradio as gr
    with gr.Blocks(title="Penguin Distortion Tester") as demo:
        inp = gr.Textbox(label="Prompt", value="penguin on ice")
        out = gr.Textbox(label="Audit Output", lines=4)
        gr.Button("Run audit").click(fn=audit, inputs=inp, outputs=out)
    return demo

if __name__ == "__main__":
    build_demo().launch(server_name="0.0.0.0", server_port=7860)
