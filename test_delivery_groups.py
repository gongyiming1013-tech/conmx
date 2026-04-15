import pytest
from delivery_groups import max_groups, min_trucks


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


# ========== min_trucks tests ==========

# ---------- Core functionality ----------

def test_trucks_given_example():
    """groups=[0,1,2] weight=6, [3,4] weight=9, capacity=10 -> 2 trucks."""
    result = min_trucks([2, 3, 1, 4, 5], [[0, 1, 2], [3, 4]], 10)
    assert result == 2


def test_trucks_single_group():
    """One group, fits in one truck."""
    result = min_trucks([1, 1, 1], [[0, 1, 2]], 5)
    assert result == 1


def test_trucks_all_independent():
    """Every package is its own group."""
    result = min_trucks([1, 2, 3, 4], [[0], [1], [2], [3]], 5)
    assert result == 4


# ---------- Edge cases ----------

def test_trucks_empty_groups():
    """No groups, no trucks needed."""
    result = min_trucks([], [], 10)
    assert result == 0


def test_trucks_single_package():
    """One package, one truck."""
    result = min_trucks([5], [[0]], 5)
    assert result == 1


def test_trucks_exact_capacity():
    """Group weight exactly equals capacity."""
    result = min_trucks([5, 5], [[0, 1]], 10)
    assert result == 1


# ---------- Overweight ----------

def test_trucks_one_group_overweight():
    """One group exceeds capacity -> -1."""
    result = min_trucks([5, 5, 5, 1, 1], [[0, 1, 2], [3, 4]], 10)
    assert result == -1


def test_trucks_all_groups_overweight():
    """All groups exceed capacity -> -1."""
    result = min_trucks([6, 6, 6, 6], [[0, 1], [2, 3]], 10)
    assert result == -1


def test_trucks_second_group_overweight():
    """First group fits, second doesn't -> -1."""
    result = min_trucks([1, 1, 8, 8], [[0, 1], [2, 3]], 10)
    assert result == -1


# ---------- Input validation ----------

def test_trucks_capacity_zero():
    """capacity=0 should raise ValueError."""
    with pytest.raises(ValueError):
        min_trucks([1], [[0]], 0)


def test_trucks_capacity_negative():
    """Negative capacity should raise ValueError."""
    with pytest.raises(ValueError):
        min_trucks([1], [[0]], -5)


def test_trucks_negative_weight():
    """Negative weight should raise ValueError."""
    with pytest.raises(ValueError):
        min_trucks([1, -2], [[0, 1]], 10)


def test_trucks_weight_length_mismatch():
    """weights length doesn't match total packages in groups."""
    with pytest.raises(ValueError):
        min_trucks([1], [[0, 1]], 10)
