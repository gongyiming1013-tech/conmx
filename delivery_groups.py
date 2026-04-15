def find(parent: list[int], x: int) -> int:
    """Follow parent pointers to find the root of x."""
    while parent[x] != x:
        x = parent[x]
    return x


def union(parent: list[int], x: int, y: int) -> None:
    """Merge the group of x into the group of y."""
    parent[find(parent, x)] = find(parent, y)


def max_groups(n: int, pairs: list[tuple[int, int]]) -> tuple[int, list[list[int]]]:
    """Return (group_count, groups) for n packages (0 to n-1) with pair constraints.

    Raises ValueError on invalid input (out-of-range IDs, n=0 with pairs).
    """
    if n == 0:
        if pairs:
            raise ValueError("n is 0 but pairs were provided")
        return 0, []

    for a, b in pairs:
        if a < 0 or a >= n or b < 0 or b >= n:
            raise ValueError(f"package ID out of range [0, {n - 1}]: ({a}, {b})")

    parent = list(range(n))

    for a, b in pairs:
        union(parent, a, b)

    groups: dict[int, list[int]] = {}
    for i in range(n):
        root = find(parent, i)
        groups.setdefault(root, []).append(i)

    group_list = list(groups.values())
    return len(group_list), group_list
