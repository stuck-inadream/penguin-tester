import gradio as gr
from z3 import Solver, Bool, sat

def _toy_penguin_sat(prompt: str) -> str:
    s = Solver()
    x = Bool("penguin_on_ice")
    want = "penguin on ice" in (prompt or "").lower()
    s.add(x == want)
    return "sat" if s.check() == sat else "unsat"

def _ckmm_stub(prompt: str) -> dict:
    text = (prompt or "").strip()
    base = max(0.0, min(len(text) / 100.0, 1.0))
    return {
        "Fuel": round(0.6 + 0.4 * base, 2),
        "Temporal": round(0.5 + 0.3 * base, 2),
        "Relational": round(0.4 + 0.35 * base, 2),
        "Ethics": round(0.7 + 0.25 * base, 2),
        "Embodiment": round(0.3 + 0.5 * base, 2),
    }

def audit(prompt: str) -> str:
    result = _toy_penguin_sat(prompt)
    m = _ckmm_stub(prompt)
    return (
        f"Result: {result}\n"
        f"Fuel={m['Fuel']:.2f}  Temporal={m['Temporal']:.2f}  "
        f"Relational={m['Relational']:.2f}  Ethics={m['Ethics']:.2f}  "
        f"Embodiment={m['Embodiment']:.2f}"
    )

with gr.Blocks(title="Penguin Distortion Tester") as demo:
    gr.Markdown("# Penguin Distortion Tester")
    inp = gr.Textbox(label="Prompt", value="penguin on ice")
    out = gr.Textbox(label="Audit Output", lines=4)
    gr.Button("Run audit").click(fn=audit, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
