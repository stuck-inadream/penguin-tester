def gpu_status_safe():
    """Return a tiny dict of GPU device count and utilization if available."""
    try:
        import pynvml
        pynvml.nvmlInit()
        n = pynvml.nvmlDeviceGetCount()
        utils = []
        for i in range(n):
            h = pynvml.nvmlDeviceGetHandleByIndex(i)
            u = pynvml.nvmlDeviceGetUtilizationRates(h)
            utils.append(int(u.gpu))
        pynvml.nvmlShutdown()
        return {"gpus": int(n), "util": utils}
    except Exception:
        return {"gpus": 0, "util": []}

def mscccl_backend_enabled() -> bool:
    """Optional comms toggle placeholder. Always False by default."""
    return False
