"""V0B BFS-based connected components for delivery grouping.

Uses a deque for iterative breadth-first traversal. Group-internal order is
**undefined**.
"""

from collections import deque


def build_graph(n: int, pairs: list[tuple[int, int]]) -> list[list[int]]:
    """Build an adjacency list from pair constraints."""
    graph = [[] for _ in range(n)]
    for a, b in pairs:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def bfs(graph: list[list[int]], start: int, visited: list[bool]) -> list[int]:
    """BFS from start node, return all nodes in the connected component."""
    queue = deque([start])
    visited[start] = True
    component = []
    while queue:
        node = queue.popleft()
        component.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return component


def max_groups_bfs(n: int, pairs: list[tuple[int, int]]) -> tuple[int, list[list[int]]]:
    """Return (group_count, groups) using BFS to find connected components.

    Group-internal order is undefined. Self-loop pairs ``(a, a)`` are accepted
    and do not change the grouping.

    Raises ValueError on invalid input (n<0, out-of-range IDs, n=0 with pairs).
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n == 0:
        if pairs:
            raise ValueError("n is 0 but pairs were provided")
        return 0, []

    for a, b in pairs:
        if a < 0 or a >= n or b < 0 or b >= n:
            raise ValueError(f"package ID out of range [0, {n - 1}]: ({a}, {b})")

    graph = build_graph(n, pairs)
    visited = [False] * n
    groups = []

    for i in range(n):
        if not visited[i]:
            component = bfs(graph, i, visited)
            groups.append(component)

    return len(groups), groups
