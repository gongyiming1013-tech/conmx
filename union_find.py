"""General-purpose Union-Find (disjoint-set) data structure.

Supports path compression and union by rank for near-constant
amortized time per operation.
"""


class UnionFind:
    """Disjoint-set data structure with path compression and union by rank.

    Contract notes:
        - ``get_groups`` returns each inner group as an **ascending-ordered**
          list of element IDs. The outer list order is unspecified. This is
          a stronger contract than the V0/V0A/V0B functional implementations,
          which leave group-internal order undefined.
        - Not thread-safe: ``find`` mutates internal ``_parent`` via path
          compression, so even concurrent reads via ``get_groups`` are unsafe.
    """

    def __init__(self, n: int) -> None:
        """Initialize n singleton sets (elements 0 to n-1).

        Args:
            n: Number of elements.
        """
        self._parent: list[int] = list(range(n))
        self._rank: list[int] = [0] * n
        self._count: int = n

    def find(self, x: int) -> int:
        """Return the root of x with path compression.

        All nodes on the path from x to root are pointed directly to root.

        Args:
            x: Element to find the root of.

        Returns:
            Root representative of the set containing x.
        """
        # Iterative two-pass: first locate root, then flatten path.
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        node = x
        while self._parent[node] != root:
            nxt = self._parent[node]
            self._parent[node] = root
            node = nxt
        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the sets containing x and y using union by rank.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if a merge occurred, False if x and y were already connected.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        rank_x = self._rank[root_x]
        rank_y = self._rank[root_y]
        if rank_x < rank_y:
            self._parent[root_x] = root_y
        elif rank_x > rank_y:
            self._parent[root_y] = root_x
        else:
            self._parent[root_y] = root_x
            self._rank[root_x] = rank_x + 1
        self._count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Return whether x and y belong to the same set.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if x and y share the same root.
        """
        return self.find(x) == self.find(y)

    def get_groups(self) -> list[list[int]]:
        """Return all connected components as sorted lists.

        Returns:
            List of groups, each group is a sorted list of element IDs.
        """
        buckets: dict[int, list[int]] = {}
        for i in range(len(self._parent)):
            root = self.find(i)
            buckets.setdefault(root, []).append(i)
        return [sorted(g) for g in buckets.values()]

    @property
    def component_count(self) -> int:
        """Return the number of distinct components."""
        return self._count
