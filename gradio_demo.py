import gradio as gr
from z3 import Solver, Bool, sat


def toy_penguin_sat(prompt: str) -> str:
    """
    Tiny symbolic check.
    If the prompt contains the phrase 'penguin on ice' return sat.
    Else return unsat.
    """
    s = Solver()
    x = Bool("penguin_on_ice")
    want = "penguin on ice" in (prompt or "").lower()
    s.add(x == want)
    result = "sat" if s.check() == sat else "unsat"
    return result


def ckmm_l_metrics(prompt: str) -> dict:
    """
    Public safe stub numbers. These do not reveal any private method.
    They simply map string features to stable floats for a friendly readout.
    """
    text = (prompt or "").strip()
    base = len(text) / 100.0
    base = max(0.0, min(base, 1.0))
    return {
        "Fuel": round(0.6 + 0.4 * base, 2),
        "Temporal": round(0.5 + 0.3 * base, 2),
        "Relational": round(0.4 + 0.35 * base, 2),
        "Ethics": round(0.7 + 0.25 * base, 2),
        "Embodiment": round(0.3 + 0.5 * base, 2),
    }


def audit(prompt: str):
    result = toy_penguin_sat(prompt)
    m = ckmm_l_metrics(prompt)
    lines = [
        f"Result: {result}",
        f"Fuel={m['Fuel']:.2f}  Temporal={m['Temporal']:.2f}  "
        f"Relational={m['Relational']:.2f}  Ethics={m['Ethics']:.2f}  "
        f"Embodiment={m['Embodiment']:.2f}"
    ]
    return "\n".join(lines)


with gr.Blocks(title="Penguin Distortion Tester") as demo:
    gr.Markdown("# Penguin Distortion Tester")
    gr.Markdown(
        "Enter a short prompt such as **penguin on ice** and run the audit. "
        "Numbers are public safe placeholders."
    )
    inp = gr.Textbox(label="Prompt", value="penguin on ice")
    out = gr.Textbox(label="Audit Output", lines=4)
    btn = gr.Button("Run audit")
    btn.click(fn=audit, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
