"""V0 functional Union-Find for delivery grouping.

Group-internal order: **undefined**. Callers that need a deterministic
order must sort the returned groups themselves. See V1 ``UnionFind.get_groups``
for a variant with a guaranteed ascending-order contract.
"""


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
    """Return the minimum number of trucks that can deliver all packages.

    All guards run before any truck arithmetic so invalid input surfaces as
    ``ValueError`` rather than downstream ``IndexError``.

    Raises ValueError on:
        - capacity <= 0
        - any negative weight
        - an empty sub-group in ``group_list``
        - a package ID outside ``[0, len(weights))``
        - the same package ID appearing in more than one sub-group
        - weights length not equal to the total package count across sub-groups
    """
    if capacity <= 0:
        raise ValueError("capacity must be a positive integer")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative integers")

    seen: set[int] = set()
    n = len(weights)
    for group in group_list:
        if not group:
            raise ValueError("group_list must not contain empty sub-groups")
        for i in group:
            if not (0 <= i < n):
                raise ValueError(
                    f"package ID out of range [0, {n - 1}]: {i}"
                )
            if i in seen:
                raise ValueError(f"duplicate package ID across groups: {i}")
            seen.add(i)

    if len(seen) != n:
        raise ValueError("weight list length does not match the number of packages")

    for group in group_list:
        group_weight = sum(weights[i] for i in group)
        if group_weight > capacity:
            return -1
    return len(group_list)
