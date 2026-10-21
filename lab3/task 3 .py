
#  BFS and DFS 

from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}

def bfs(graph, start, goal):
    queue = deque([start])
    parent = {start: None}
    visited = []

    while queue:
        node = queue.popleft()
        visited.append(node)

        if node == goal:
            break

        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)

    if goal not in parent:
        return visited, None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return visited, path

order, path = bfs(graph, "A", "G")
print("BFS visit order:", order)
print("BFS final path:", " -> ".join(path) if path else "No path")




#  DLS and IDDFS 

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}

def dls(graph, node, goal, limit, path):
    path.append(node)

    if node == goal:
        return "FOUND", path.copy()

    if limit == 0:
        return "CUTOFF", None

    cutoff_found = False

    for child in graph[node]:
        if child not in path:
            status, result = dls(
                graph, child, goal, limit - 1, path
            )

            if status == "FOUND":
                return "FOUND", result

            if status == "CUTOFF":
                cutoff_found = True

    path.pop()

    if cutoff_found:
        return "CUTOFF", None

    return "FAILURE", None


for limit in [1, 2, 3, 4]:
    status, result = dls(graph, "A", "G", limit, [])

    print("Limit:", limit)
    print("Status:", status)
    print("Path:", result)
    print()




#UCS


import heapq
from collections import deque

graph = {
    "A": [("B", 1), ("C", 10)],
    "B": [("D", 2), ("E", 1)],
    "C": [("F", 3), ("G", 2)],
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": []
}

def ucs(graph, start, goal):
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        visited.add(node)

        if node == goal:
            return path, cost

        for next_node, weight in graph[node]:
            if next_node not in visited:
                heapq.heappush(
                    queue,
                    (cost + weight, next_node, path + [next_node])
                )

    return None, float("inf")


def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == goal:
            cost = 0

            for i in range(len(path) - 1):
                for neighbor, weight in graph[path[i]]:
                    if neighbor == path[i + 1]:
                        cost += weight

            return path, cost

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, float("inf")


ucs_path, ucs_cost = ucs(graph, "A", "G")
bfs_path, bfs_cost = bfs(graph, "A", "G")

print("UCS Path:", ucs_path)
print("UCS Cost:", ucs_cost)

print("BFS Path:", bfs_path)
print("BFS Cost:", bfs_cost)
