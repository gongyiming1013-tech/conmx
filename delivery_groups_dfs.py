"""V0A DFS-based connected components for delivery grouping.

Uses an explicit-stack iterative DFS to avoid Python's default recursion
limit (1000) on long chain inputs. Group-internal order is **undefined**.
"""


def build_graph(n: int, pairs: list[tuple[int, int]]) -> list[list[int]]:
    """Build an adjacency list from pair constraints."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in pairs:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def dfs(graph: list[list[int]], start: int, visited: list[bool], component: list[int]) -> None:
    """Iteratively visit all nodes in a connected component starting from ``start``.

    Uses an explicit stack so traversal depth is bounded by available heap,
    not by Python's recursion limit.
    """
    stack: list[int] = [start]
    while stack:
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        component.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                stack.append(neighbor)


def max_groups_dfs(n: int, pairs: list[tuple[int, int]]) -> tuple[int, list[list[int]]]:
    """Return (group_count, groups) using DFS to find connected components.

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
    groups: list[list[int]] = []

    for i in range(n):
        if not visited[i]:
            component: list[int] = []
            dfs(graph, i, visited, component)
            groups.append(component)

    return len(groups), groups
