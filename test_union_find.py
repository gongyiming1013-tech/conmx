"""Tests for UnionFind data structure."""

import pytest

from union_find import UnionFind


# ---------------------------------------------------------------------------
# Core operations: find, union, connected
# ---------------------------------------------------------------------------

class TestCoreOperations:
    """Basic find, union, connected behavior."""

    def test_find_singleton(self) -> None:
        """Each element is its own root initially."""
        uf = UnionFind(5)
        for i in range(5):
            assert uf.find(i) == i

    def test_union_merges_two_elements(self) -> None:
        """After union(0, 1), both share the same root."""
        uf = UnionFind(5)
        assert uf.union(0, 1) is True
        assert uf.find(0) == uf.find(1)

    def test_union_returns_false_if_already_connected(self) -> None:
        """union returns False when elements are already in the same set."""
        uf = UnionFind(5)
        uf.union(0, 1)
        assert uf.union(0, 1) is False

    def test_self_union_returns_false(self) -> None:
        """union(x, x) is a no-op and returns False."""
        uf = UnionFind(3)
        assert uf.union(1, 1) is False

    def test_connected_after_union(self) -> None:
        """connected returns True after union."""
        uf = UnionFind(4)
        uf.union(0, 1)
        assert uf.connected(0, 1) is True

    def test_not_connected_without_union(self) -> None:
        """Distinct elements are not connected initially."""
        uf = UnionFind(4)
        assert uf.connected(0, 1) is False

    def test_connected_reflexive(self) -> None:
        """Every element is connected to itself."""
        uf = UnionFind(3)
        assert uf.connected(2, 2) is True

    def test_transitive_merge(self) -> None:
        """union(0,1) + union(1,2) => 0, 1, 2 all connected."""
        uf = UnionFind(4)
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.connected(0, 2) is True
        assert uf.connected(0, 3) is False


# ---------------------------------------------------------------------------
# Path compression
# ---------------------------------------------------------------------------

class TestPathCompression:
    """Verify that find flattens the parent chain."""

    def test_path_compression_flattens_chain(self) -> None:
        """After find on a deep chain, all nodes point directly to root."""
        uf = UnionFind(5)
        # Build chain: 0 <- 1 <- 2 <- 3 <- 4
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(2, 3)
        uf.union(3, 4)

        root = uf.find(0)
        # After find(0), every node on the path should point to root
        for i in range(5):
            assert uf._parent[i] == root

    def test_path_compression_does_not_change_root(self) -> None:
        """Root's parent stays as itself after compression."""
        uf = UnionFind(3)
        uf.union(0, 1)
        uf.union(1, 2)
        root = uf.find(0)
        assert uf._parent[root] == root


# ---------------------------------------------------------------------------
# Union by rank
# ---------------------------------------------------------------------------

class TestUnionByRank:
    """Verify rank-based merging strategy."""

    def test_equal_rank_increments(self) -> None:
        """Merging two rank-0 trees gives the new root rank 1."""
        uf = UnionFind(2)
        uf.union(0, 1)
        root = uf.find(0)
        assert uf._rank[root] == 1

    def test_unequal_rank_preserves_higher_root(self) -> None:
        """Lower-rank tree is attached under higher-rank root."""
        uf = UnionFind(4)
        # rank of root(0,1) becomes 1
        uf.union(0, 1)
        root_01 = uf.find(0)
        # 2 is still rank 0
        uf.union(2, 0)
        # root should still be root_01 (rank 1 > rank 0)
        assert uf.find(2) == root_01
        # rank should not change
        assert uf._rank[root_01] == 1

    def test_two_rank1_trees_merge_to_rank2(self) -> None:
        """Merging two rank-1 trees gives rank 2."""
        uf = UnionFind(4)
        uf.union(0, 1)  # rank 1
        uf.union(2, 3)  # rank 1
        uf.union(0, 2)  # rank 2
        root = uf.find(0)
        assert uf._rank[root] == 2


# ---------------------------------------------------------------------------
# Components: get_groups, component_count
# ---------------------------------------------------------------------------

class TestComponents:
    """Verify group collection and counting."""

    def test_all_singletons(self) -> None:
        """No unions => n singleton groups."""
        uf = UnionFind(4)
        groups = uf.get_groups()
        assert len(groups) == 4
        for g in groups:
            assert len(g) == 1

    def test_one_big_group(self) -> None:
        """All connected => one group containing all elements."""
        uf = UnionFind(3)
        uf.union(0, 1)
        uf.union(1, 2)
        groups = uf.get_groups()
        assert len(groups) == 1
        assert sorted(groups[0]) == [0, 1, 2]

    def test_mixed_groups(self) -> None:
        """Some connected, some not."""
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)
        groups = uf.get_groups()
        assert len(groups) == 2
        sorted_groups = sorted(groups, key=lambda g: g[0])
        assert sorted_groups[0] == [0, 1, 2]
        assert sorted_groups[1] == [3, 4]

    def test_groups_are_sorted(self) -> None:
        """Each group list is sorted by element ID."""
        uf = UnionFind(4)
        uf.union(3, 0)
        uf.union(2, 3)
        groups = uf.get_groups()
        for g in groups:
            assert g == sorted(g)

    def test_component_count_initial(self) -> None:
        """Initially, component_count == n."""
        uf = UnionFind(5)
        assert uf.component_count == 5

    def test_component_count_after_unions(self) -> None:
        """component_count decreases with each effective union."""
        uf = UnionFind(5)
        uf.union(0, 1)
        assert uf.component_count == 4
        uf.union(1, 2)
        assert uf.component_count == 3
        uf.union(3, 4)
        assert uf.component_count == 2

    def test_component_count_duplicate_union(self) -> None:
        """Duplicate union does not change component_count."""
        uf = UnionFind(3)
        uf.union(0, 1)
        assert uf.component_count == 2
        uf.union(0, 1)
        assert uf.component_count == 2


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Boundary conditions."""

    def test_single_element(self) -> None:
        """n=1 has one singleton group."""
        uf = UnionFind(1)
        assert uf.find(0) == 0
        assert uf.component_count == 1
        assert uf.get_groups() == [[0]]

    def test_empty(self) -> None:
        """n=0 has no groups."""
        uf = UnionFind(0)
        assert uf.component_count == 0
        assert uf.get_groups() == []

    def test_large_no_unions(self) -> None:
        """Large n with no unions => all singletons."""
        n = 1000
        uf = UnionFind(n)
        assert uf.component_count == n
        groups = uf.get_groups()
        assert len(groups) == n
