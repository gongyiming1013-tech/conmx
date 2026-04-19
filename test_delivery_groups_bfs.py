import pytest
from delivery_groups_bfs import max_groups_bfs


# ---------- Core functionality ----------

def test_given_example():
    count, groups = max_groups_bfs(5, [(0, 1), (1, 2), (3, 4)])
    assert count == 2
    assert sorted(sorted(g) for g in groups) == [[0, 1, 2], [3, 4]]


def test_no_constraints():
    count, groups = max_groups_bfs(4, [])
    assert count == 4
    assert sorted(sorted(g) for g in groups) == [[0], [1], [2], [3]]


def test_all_connected():
    count, groups = max_groups_bfs(3, [(0, 1), (1, 2)])
    assert count == 1
    assert sorted(sorted(g) for g in groups) == [[0, 1, 2]]


# ---------- Edge cases ----------

def test_n_zero():
    count, groups = max_groups_bfs(0, [])
    assert count == 0
    assert groups == []


def test_n_one():
    count, groups = max_groups_bfs(1, [])
    assert count == 1
    assert sorted(sorted(g) for g in groups) == [[0]]


def test_single_pair():
    count, groups = max_groups_bfs(2, [(0, 1)])
    assert count == 1
    assert sorted(sorted(g) for g in groups) == [[0, 1]]


# ---------- Duplicate handling ----------

def test_duplicate_pairs():
    count, groups = max_groups_bfs(3, [(0, 1), (0, 1)])
    assert count == 2
    assert sorted(sorted(g) for g in groups) == [[0, 1], [2]]


# ---------- Transitivity ----------

def test_chain_transitivity():
    count, groups = max_groups_bfs(4, [(0, 1), (1, 2), (2, 3)])
    assert count == 1
    assert sorted(sorted(g) for g in groups) == [[0, 1, 2, 3]]


def test_bridge_merge():
    count, groups = max_groups_bfs(4, [(0, 1), (2, 3), (1, 2)])
    assert count == 1
    assert sorted(sorted(g) for g in groups) == [[0, 1, 2, 3]]


# ---------- Input validation ----------

def test_n_zero_with_pairs():
    with pytest.raises(ValueError):
        max_groups_bfs(0, [(0, 1)])


def test_pair_out_of_range():
    with pytest.raises(ValueError):
        max_groups_bfs(2, [(2, 3)])


def test_pair_partially_out_of_range():
    with pytest.raises(ValueError):
        max_groups_bfs(3, [(0, 1), (1, 5)])


def test_negative_id():
    with pytest.raises(ValueError):
        max_groups_bfs(3, [(0, -1)])


# ---------- V1.1 additions ----------

def test_negative_n_raises():
    """n<0 must raise ValueError explicitly."""
    with pytest.raises(ValueError):
        max_groups_bfs(-1, [])


def test_self_loop_pair_is_accepted():
    """(a, a) self-loop is allowed and does not change the grouping."""
    count, groups = max_groups_bfs(3, [(2, 2)])
    assert count == 3
    assert sorted(sorted(g) for g in groups) == [[0], [1], [2]]
