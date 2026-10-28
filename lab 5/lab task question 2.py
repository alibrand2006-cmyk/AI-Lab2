import math
import random
 
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
 
def compare(name, scores):
    d = int(math.log2(len(scores)))
    c1 = {"leaves": 0}; c2 = {"leaves": 0}
    v1 = minimax(0, 0, True, scores, d, c1)
    v2 = alphabeta(0, 0, True, scores, d, float('-inf'), float('inf'), c2)
    print(f"{name}")
    print(f"  scores     : {scores}")
    print(f"  Minimax    : value = {v1}, leaves evaluated = {c1['leaves']}")
    print(f"  Alpha-Beta : value = {v2}, leaves evaluated = {c2['leaves']}")
    print(f"  Same value : {v1 == v2} | Pruned leaves: {c1['leaves'] - c2['leaves']}\n")
    return v1, v2, c1["leaves"], c2["leaves"]
 
compare("Test 1: Tree from 5.1 (padded)", [3, 5, 2, 9, 0, 7, 0, 0])
compare("Test 2: Tree from 5.2",          [3, 5, 2, 9, 3, 5, 2, 9])
compare("Test 3: All equal leaves",       [4, 4, 4, 4, 4, 4, 4, 4])
compare("Test 4: Single leaf",            [7])
 
random.seed(42)
bad = 0; worse = 0; saved = 0; total = 0
for _ in range(2000):
    n = 2 ** random.randint(1, 5)
    s = [random.randint(-20, 20) for _ in range(n)]
    d = int(math.log2(n))
    c1 = {"leaves": 0}; c2 = {"leaves": 0}
    v1 = minimax(0, 0, True, s, d, c1)
    v2 = alphabeta(0, 0, True, s, d, float('-inf'), float('inf'), c2)
    bad   += (v1 != v2)
    worse += (c2["leaves"] > c1["leaves"])
    saved += c1["leaves"] - c2["leaves"]
    total += c1["leaves"]
print("Stress test (2000 random trees):")
print("  Value mismatches        :", bad)
print("  Cases AB > Minimax leaves:", worse)
print(f"  Total leaves saved      : {saved} of {total} ({100*saved/total:.1f}%)")
 