import platform, sys, os, re
HINT_RE = re.compile(r"^[A-Za-z0-9_.:/ ]{0,64}$")

class SubstrateInfo:
    def capture(self):
        raw = os.getenv("SUBSTRATE_HINT", "unspecified")
        hint = raw if HINT_RE.match(raw or "") else "unspecified"
        return {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": sys.version.split()[0],
            "hint": hint
        }
