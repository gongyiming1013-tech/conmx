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

def min_trucks(weights: list[int], group_list: list[list[int]], capacity: int) -> int:
    """Return the minimum number of trucks that can be used to deliver all packages given the constraints.

    Raises ValueError on invalid input (capacity <= 0, negative weights, weight list length not match number of package).
    """
    if capacity <= 0:
        raise ValueError("capacity must be a positive integer")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative integers")
    if len(weights) != sum(len(group) for group in group_list):
        raise ValueError("weight list length does not match the number of packages")

    for group in group_list:
        group_weight = sum(weights[i] for i in group)
        if group_weight > capacity:
            return -1  # Cannot deliver this group
    return len(group_list)  # Each group can be delivered in one truck