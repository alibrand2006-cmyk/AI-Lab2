
import math, random, itertools
from collections import Counter

def minimax(depth, index, maxTurn, scores, target, counter):
    if depth == target:
        counter["leaves"] += 1
        return scores[index]
    if maxTurn:
        return max(minimax(depth+1, index*2,   False, scores, target, counter),
                   minimax(depth+1, index*2+1, False, scores, target, counter))
    else:
        return min(minimax(depth+1, index*2,   True,  scores, target, counter),
                   minimax(depth+1, index*2+1, True,  scores, target, counter))
 
def alphabeta(depth, index, maxTurn, scores, target, alpha, beta, counter):
    if depth == target:
        counter["leaves"] += 1
        return scores[index]
    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth+1, index*2+i, False, scores, target, alpha, beta, counter))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta(depth+1, index*2+i, True, scores, target, alpha, beta, counter))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
 
def run_ab(scores):
    d = int(math.log2(len(scores)))
    c = {"leaves": 0}
    v = alphabeta(0, 0, True, scores, d, float('-inf'), float('inf'), c)
    return v, c["leaves"]
 
def run_mm(scores):
    d = int(math.log2(len(scores)))
    c = {"leaves": 0}
    v = minimax(0, 0, True, scores, d, c)
    return v, c["leaves"]
 
def to_tree(s):
    if len(s) == 1: return s[0]
    h = len(s)//2
    return [to_tree(s[:h]), to_tree(s[h:])]
 
def flat(t):
    return [t] if not isinstance(t, list) else flat(t[0]) + flat(t[1])
 
def variants(t):
    if not isinstance(t, list):
        yield t; return
    for a in variants(t[0]):
        for b in variants(t[1]):
            yield [a, b]
            yield [b, a]
 
def value(t, maxTurn):
    if not isinstance(t, list): return t
    vs = [value(t[0], not maxTurn), value(t[1], not maxTurn)]
    return max(vs) if maxTurn else min(vs)
 
def ordered(t, maxTurn, best=True):
    if not isinstance(t, list): return t
    kids = [ordered(t[0], not maxTurn, best), ordered(t[1], not maxTurn, best)]
    v = [value(k, not maxTurn) for k in kids]
    good_first = (v[0] >= v[1]) if maxTurn else (v[0] <= v[1])
    if good_first != best: kids.reverse()
    return kids
 
def experiment(name, scores):
    base_v, base_leaves = run_ab(scores)
    mm_v, mm_leaves = run_mm(scores)
    res = []
    for t in variants(to_tree(scores)):
        s = flat(t)
        v, n = run_ab(s)
        res.append((v, n, s))
    vals = {r[0] for r in res}
    dist = Counter(r[1] for r in res)
    best = min(res, key=lambda r: r[1]); worst = max(res, key=lambda r: r[1])
    print(name, scores)
    print(f"  Minimax value / leaves        : {mm_v} / {mm_leaves}")
    print(f"  Original order (Alpha-Beta)   : value {base_v}, leaves {base_leaves}")
    print(f"  Orderings tried               : {len(res)}")
    print(f"  Distinct root values          : {sorted(vals)}")
    print(f"  Leaves  min / max             : {best[1]} / {worst[1]}")
    print(f"  Distribution (leaves: count)  : {dict(sorted(dist.items()))}")
    print(f"  Best  order {best[2]} -> {best[1]} leaves")
    print(f"  Worst order {worst[2]} -> {worst[1]} leaves")
    t = to_tree(scores)
    b = flat(ordered(t, True, True)); w = flat(ordered(t, True, False))
    print(f"  Oracle-best order {b} -> {run_ab(b)[1]} leaves (value {run_ab(b)[0]})")
    print(f"  Oracle-worst order {w} -> {run_ab(w)[1]} leaves (value {run_ab(w)[0]})\n")
 
experiment("Tree A (5.1):", [3, 5, 2, 9, 0, 7, 0, 0])
experiment("Tree B (5.2):", [3, 5, 2, 9, 3, 5, 2, 9])
experiment("Edge: all equal:", [4]*8)
 
random.seed(7)
big = [random.randint(-20, 20) for _ in range(16)]
tb = to_tree(big)
rs = []
for t in itertools.islice(variants(tb), 0, None, 1):   # all 2^15 = 32768 orderings
    rs.append(run_ab(flat(t)))
print("Depth-4 tree:", big)
print("  Orderings tried :", len(rs))
print("  Root values     :", sorted({r[0] for r in rs}))
print("  Leaves min/max  :", min(r[1] for r in rs), "/", max(r[1] for r in rs), "(Minimax always 16)")
print(f"  Leaves average  : {sum(r[1] for r in rs)/len(rs):.2f}")
print("  Oracle-best     :", run_ab(flat(ordered(tb, True, True)))[1], "leaves")
print("  Oracle-worst    :", run_ab(flat(ordered(tb, True, False)))[1], "leaves")