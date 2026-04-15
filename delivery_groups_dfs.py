def build_graph(n: int, pairs: list[tuple[int, int]]) -> list[list[int]]:
    """Build an adjacency list from pair constraints."""
    graph = [[] for _ in range(n)]
    for a, b in pairs:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def dfs(graph: list[list[int]], node: int, visited: list[bool], component: list[int]) -> None:
    """Recursively visit all nodes in a connected component."""
    visited[node] = True
    component.append(node)
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, component)


def max_groups_dfs(n: int, pairs: list[tuple[int, int]]) -> tuple[int, list[list[int]]]:
    """Return (group_count, groups) using DFS to find connected components.

    Raises ValueError on invalid input (out-of-range IDs, n=0 with pairs).
    """
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
            component = []
            dfs(graph, i, visited, component)
            groups.append(component)

    return len(groups), groups
