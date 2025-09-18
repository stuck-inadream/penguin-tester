import yaml, json, importlib

def validate_all_configs():
    try:
        jsonschema = importlib.import_module("jsonschema")
    except Exception:
        # If jsonschema is absent, skip strict validation
        return {"skip": True}
    schemas = {
        "configs/cvr_dopo.yaml": {"type": "object"},
        "configs/rlvr_dual.yaml": {"type": "object"},
        "configs/concise_gfpo.yaml": {"type": "object"},
        "configs/async_small.yaml": {"type": "object"},
    }
    out = {}
    for path, schema in schemas.items():
        try:
            data = yaml.safe_load(open(path, "r", encoding="utf-8"))
            jsonschema.validate(instance=data, schema=schema)
            out[path] = True
        except Exception:
            out[path] = False
    return out
