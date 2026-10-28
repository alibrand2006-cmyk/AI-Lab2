import math

def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth, trace=None):
    if curDepth == targetDepth:
        if trace is not None:
            trace.append(f"{'  '*curDepth}Leaf[{nodeIndex}] = {scores[nodeIndex]}")
        return scores[nodeIndex]
    left  = minimax(curDepth+1, nodeIndex*2,   not maxTurn, scores, targetDepth, trace)
    right = minimax(curDepth+1, nodeIndex*2+1, not maxTurn, scores, targetDepth, trace)
    val = max(left, right) if maxTurn else min(left, right)
    if trace is not None:
        t = "MAX" if maxTurn else "MIN"
        fn = "max" if maxTurn else "min"
        trace.append(f"{'  '*curDepth}{t} node (depth {curDepth}, idx {nodeIndex}): {fn}({left}, {right}) = {val}")
    return val

def run(scores):
    scores = list(scores)
    d = math.ceil(math.log2(len(scores)))
    scores += [0]*(2**d - len(scores))
    trace = []
    r = minimax(0, 0, True, scores, d, trace)
    print("Padded scores:", scores, "| depth:", d)
    print("\n".join(trace))
    print("The optimal value is:", r, "\n")

run([3, 5, 2, 9, 0, 7])         
run([-4, -2, -8, -6, -1, -9])    
run([7])                         