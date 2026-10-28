import heapq
 
# graph and heuristic given in the lab manual
graph = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
h = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}
h_zero = {n: 0 for n in h}      # all zeros = UCS control run
 
 
def search(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]      # (f, g, node, path)
    best = {start: 0}
    processed = []     # every valid pop, in order: (node, g, f)
    expanded = []      # nodes whose successors were examined
    stale = 0          # old queue entries that were skipped
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if g != best[node]:        # old entry, a better g is already known
            stale += 1
            continue
        processed.append((node, g, f))
        if node == goal:           # goal is logged but not counted as expanded
            return g, path, processed, expanded, stale
        expanded.append(node)
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))
    return None, None, processed, expanded, stale
 
 
def path_cost(graph, path):
    # adds up the edge weights separately from the search
    total = 0
    for u, v in zip(path, path[1:]):
        for nxt, w in graph[u]:
            if nxt == v:
                total += w
    return total
 
 
def run(name, heuristic):
    g, path, processed, expanded, stale = search(graph, heuristic, "S", "G")
    print("=== " + name + " ===")
    print("Path returned        :", " -> ".join(path))
    print("Cost returned        :", g)
    print("Cost summed by hand  :", path_cost(graph, path))
    print("Processed-node trace :")
    for node, gv, fv in processed:
        tag = "  (goal, not counted)" if node == "G" else ""
        print("   %s  g=%d  f=%d%s" % (node, gv, fv, tag))
    print("Expanded nodes       :", expanded)
    print("Expansion count      :", len(expanded))
    print("Stale entries skipped:", stale)
    print()
 
 
run("A* (supplied heuristic)", h)
run("UCS (h = 0 for every node)", h_zero)
 
 
# ---- Task 3: overestimate test ----
h_bad = dict(h)
h_bad["C"] = 10                          # original value was 2
true_c = path_cost(graph, ["C", "G"])    # true remaining cost of C
 
print("h(C) original          :", h["C"])
print("h(C) modified          :", h_bad["C"])
print("True remaining cost(C) :", true_c)
print("Overestimate by        :", h_bad["C"] - true_c)
print()
run("A* with h(C) = 10", h_bad)
 
# extra check: some other overestimates of C
for value in [4, 6, 7]:
    h_test = dict(h)
    h_test["C"] = value
    g, path, processed, expanded, stale = search(graph, h_test, "S", "G")
    print("h(C) =", value, "->", " -> ".join(path))
    print("   cost", g, "| expansions", len(expanded))
 