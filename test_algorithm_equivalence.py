"""Cross-algorithm equivalence tests (V1.1).

V0 (Union-Find), V0A (DFS), V0B (BFS) and V1 (DeliveryGrouper) must produce
the same grouping for any valid input. Each implementation serves as an oracle
for the others, catching algorithm-specific bugs that single-implementation
tests cannot.
"""

import pytest

from delivery_groups import max_groups
from delivery_groups_bfs import max_groups_bfs
from delivery_groups_dfs import max_groups_dfs
from delivery_grouper import DeliveryGrouper


def _canonical(result):
    """Normalize (count, groups) for order-independent comparison."""
    count, groups = result
    return count, sorted(sorted(g) for g in groups)


@pytest.mark.parametrize(
    "n,pairs",
    [
        (0, []),                                           # empty
        (1, []),                                           # singleton
        (5, []),                                           # all isolated
        (5, [(0, 1), (1, 2), (2, 3), (3, 4)]),             # full chain
        (6, [(0, 1), (2, 3), (4, 5)]),                     # three disjoint pairs
        (5, [(0, 1), (0, 1), (1, 0)]),                     # duplicates
        (3, [(2, 2)]),                                     # self-loop
        (10, [(4, 0), (3, 1), (2, 0), (8, 9), (7, 6)]),    # out-of-order pairs
        (7, [(0, 1), (1, 2), (3, 4), (5, 5), (4, 2)]),     # mix: chain + self-loop + bridge
    ],
)
def test_all_algorithms_produce_same_result(n, pairs):
    """V0, V0A, V0B, V1 must return equivalent groupings."""
    r_uf = _canonical(max_groups(n, pairs))
    r_bfs = _canonical(max_groups_bfs(n, pairs))
    r_dfs = _canonical(max_groups_dfs(n, pairs))
    r_v1 = _canonical(DeliveryGrouper(n, pairs).max_groups())

    assert r_uf == r_bfs == r_dfs == r_v1
