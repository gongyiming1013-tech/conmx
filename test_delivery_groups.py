import pytest
from delivery_groups import max_groups


# ---------- Core functionality ----------

def test_given_example():
    """n=5, [(0,1),(1,2),(3,4)] -> 2 groups: [0,1,2] and [3,4]"""
    count, groups = max_groups(5, [(0, 1), (1, 2), (3, 4)])
    assert count == 2
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0, 1, 2], [3, 4]]


def test_no_constraints():
    """Every package is its own group."""
    count, groups = max_groups(4, [])
    assert count == 4
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0], [1], [2], [3]]


def test_all_connected():
    """All packages end up in one group."""
    count, groups = max_groups(3, [(0, 1), (1, 2)])
    assert count == 1
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0, 1, 2]]


# ---------- Edge cases ----------

def test_n_zero():
    """n=0, no packages, no groups."""
    count, groups = max_groups(0, [])
    assert count == 0
    assert groups == []


def test_n_one():
    """Single package, one group."""
    count, groups = max_groups(1, [])
    assert count == 1
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0]]


def test_single_pair():
    """n=2, one constraint merges them."""
    count, groups = max_groups(2, [(0, 1)])
    assert count == 1
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0, 1]]


# ---------- Duplicate handling ----------

def test_duplicate_pairs():
    """Duplicate constraints should not affect the result."""
    count, groups = max_groups(3, [(0, 1), (0, 1)])
    assert count == 2
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0, 1], [2]]


# ---------- Transitivity ----------

def test_chain_transitivity():
    """Chain: 0-1-2-3 all connected transitively."""
    count, groups = max_groups(4, [(0, 1), (1, 2), (2, 3)])
    assert count == 1
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0, 1, 2, 3]]


def test_bridge_merge():
    """Two separate groups merged by a bridge constraint."""
    count, groups = max_groups(4, [(0, 1), (2, 3), (1, 2)])
    assert count == 1
    groups_sorted = sorted(sorted(g) for g in groups)
    assert groups_sorted == [[0, 1, 2, 3]]


# ---------- Input validation ----------

def test_n_zero_with_pairs():
    """n=0 but pairs provided — should raise ValueError."""
    with pytest.raises(ValueError):
        max_groups(0, [(0, 1)])


def test_pair_out_of_range():
    """Package ID exceeds n-1 — should raise ValueError."""
    with pytest.raises(ValueError):
        max_groups(2, [(2, 3)])


def test_pair_partially_out_of_range():
    """One valid ID, one out of range — should raise ValueError."""
    with pytest.raises(ValueError):
        max_groups(3, [(0, 1), (1, 5)])


def test_negative_id():
    """Negative package ID — should raise ValueError."""
    with pytest.raises(ValueError):
        max_groups(3, [(0, -1)])
