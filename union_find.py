"""General-purpose Union-Find (disjoint-set) data structure.

Supports path compression and union by rank for near-constant
amortized time per operation.
"""


class UnionFind:
    """Disjoint-set data structure with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        """Initialize n singleton sets (elements 0 to n-1).

        Args:
            n: Number of elements.
        """
        raise NotImplementedError

    def find(self, x: int) -> int:
        """Return the root of x with path compression.

        All nodes on the path from x to root are pointed directly to root.

        Args:
            x: Element to find the root of.

        Returns:
            Root representative of the set containing x.
        """
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        """Merge the sets containing x and y using union by rank.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if a merge occurred, False if x and y were already connected.
        """
        raise NotImplementedError

    def connected(self, x: int, y: int) -> bool:
        """Return whether x and y belong to the same set.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if x and y share the same root.
        """
        raise NotImplementedError

    def get_groups(self) -> list[list[int]]:
        """Return all connected components as sorted lists.

        Returns:
            List of groups, each group is a sorted list of element IDs.
        """
        raise NotImplementedError

    @property
    def component_count(self) -> int:
        """Return the number of distinct components."""
        raise NotImplementedError
