"""Domain-specific delivery grouping using Union-Find.

Encapsulates input validation, group computation, and truck capacity
logic. Composes a UnionFind instance internally.
"""

from union_find import UnionFind


class DeliveryGrouper:
    """Solve package delivery grouping with pair constraints.

    Validates input at construction time and builds the internal
    Union-Find structure. Query methods are available immediately after.
    """

    def __init__(self, n: int, pairs: list[tuple[int, int]]) -> None:
        """Validate input and build the union-find for n packages.

        Args:
            n: Number of packages (0 to n-1).
            pairs: List of (a, b) constraints meaning a and b must be
                delivered together. Constraints are transitive.

        Raises:
            ValueError: If n=0 but pairs are provided, or if any package
                ID is out of range [0, n-1].
        """
        if n == 0 and pairs:
            raise ValueError("n=0 but pairs were provided")
        for a, b in pairs:
            if not (0 <= a < n) or not (0 <= b < n):
                raise ValueError(
                    f"package ID out of range [0, {n - 1}]: ({a}, {b})"
                )
        self._n: int = n
        self._uf: UnionFind = UnionFind(n)
        for a, b in pairs:
            self._uf.union(a, b)

    def max_groups(self) -> tuple[int, list[list[int]]]:
        """Return the maximum number of delivery groups and the groups.

        Returns:
            Tuple of (group_count, groups) where groups is a list of
            sorted lists of package IDs.
        """
        groups = self._uf.get_groups()
        return self._uf.component_count, groups

    def min_trucks(self, weights: list[int], capacity: int) -> int:
        """Return the minimum number of trucks needed.

        Each group must fit in a single truck. If any group exceeds
        the capacity, return -1.

        Args:
            weights: Weight of each package (indexed by package ID).
            capacity: Maximum weight a single truck can carry.

        Returns:
            Number of trucks needed, or -1 if any group exceeds capacity.

        Raises:
            ValueError: If capacity <= 0, any weight is negative, or
                weight list length does not match the number of packages.
        """
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        if len(weights) != self._n:
            raise ValueError(
                f"weights length {len(weights)} does not match n={self._n}"
            )
        for w in weights:
            if w < 0:
                raise ValueError(f"weight must be non-negative, got {w}")
        trucks = 0
        for group in self._uf.get_groups():
            total = sum(weights[i] for i in group)
            if total > capacity:
                return -1
            trucks += 1
        return trucks
