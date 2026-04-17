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
        raise NotImplementedError

    def max_groups(self) -> tuple[int, list[list[int]]]:
        """Return the maximum number of delivery groups and the groups.

        Returns:
            Tuple of (group_count, groups) where groups is a list of
            sorted lists of package IDs.
        """
        raise NotImplementedError

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
        raise NotImplementedError
