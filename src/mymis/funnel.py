def summarize_funnel(counts):
    if not counts:
        return []
    first = counts[0][1]
    out = []
    prev = None
    for step, value in counts:
        if value < 0:
            raise ValueError("funnel counts cannot be negative")
        out.append({
            "step": step,
            "users": value,
            "from_start": value / first if first else 0,
            "from_previous": None if prev is None else (value / prev if prev else 0),
            "dropoff_from_previous": None if prev is None else (1 - value / prev if prev else 0),
        })
        prev = value
    return out
