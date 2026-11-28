"""12월 곡 공통: 줄 시각(썸네일에서도 맞게 ctx["lines"]만 씀)으로 지금 줄과 지나간 줄을 찾는다."""
from kids.engine import section_at

def cur(ctx, t):
    L = ctx["lines"]
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx = max([i for i, l in enumerate(L) if l["start"] <= t], default=-1)
    dt = t - L[idx]["start"] if idx >= 0 else t
    line = L[idx]["text"] if idx >= 0 else ""
    return sec, s0, idx, dt, line

def count(ctx, t, word):
    """지금까지 word가 든 줄이 몇 번 불렸나"""
    return sum(1 for l in ctx["lines"] if l["start"] <= t and word in l["text"])

def since(ctx, t, word, nth=1):
    """word가 든 nth번째 줄이 시작된 뒤 몇 초 지났나 (아직이면 None)"""
    k = 0
    for l in ctx["lines"]:
        if word in l["text"]:
            k += 1
            if k == nth: return t - l["start"] if l["start"] <= t else None
    return None
