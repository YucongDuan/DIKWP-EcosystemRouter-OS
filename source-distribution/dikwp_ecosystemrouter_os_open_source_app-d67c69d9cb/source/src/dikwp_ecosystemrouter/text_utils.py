def norm(text: str) -> str:
    return " ".join((text or "").lower().strip().split())

def contains_any(text: str, terms) -> bool:
    t = norm(text)
    return any(term.lower() in t for term in terms)

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))
