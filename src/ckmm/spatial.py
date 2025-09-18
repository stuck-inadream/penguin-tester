# Thin shim to match external docs that mention `spatial`.
from .relational import CouncilRunner as SpatialCouncilRunner
__all__ = ["SpatialCouncilRunner"]
