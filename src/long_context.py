def streaming_context(tokens: int = 4096, window: int = 512):
    segs = []
    i = 0
    while i < tokens:
        segs.append((i, min(window, tokens - i)))
        i += max(1, window // 2)
    return segs
