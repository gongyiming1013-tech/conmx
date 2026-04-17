"""Tests for DeliveryGrouper domain class."""

import pytest

from delivery_grouper import DeliveryGrouper


# ---------------------------------------------------------------------------
# Core functionality
# ---------------------------------------------------------------------------

class TestCoreFunctionality:
    """Basic grouping behavior — same expected output as V0."""

    def test_given_example(self) -> None:
        """n=5, [(0,1),(1,2),(3,4)] => 2 groups: [0,1,2] and [3,4]."""
        dg = DeliveryGrouper(5, [(0, 1), (1, 2), (3, 4)])
        count, groups = dg.max_groups()
        assert count == 2
        sorted_groups = sorted(groups, key=lambda g: g[0])
        assert sorted_groups[0] == [0, 1, 2]
        assert sorted_groups[1] == [3, 4]

    def test_no_constraints(self) -> None:
        """No pairs => every package is its own group."""
        dg = DeliveryGrouper(4, [])
        count, groups = dg.max_groups()
        assert count == 4
        for g in groups:
            assert len(g) == 1

    def test_all_connected(self) -> None:
        """All packages linked => one group."""
        dg = DeliveryGrouper(3, [(0, 1), (1, 2)])
        count, groups = dg.max_groups()
        assert count == 1
        assert sorted(groups[0]) == [0, 1, 2]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Boundary conditions."""

    def test_n_zero_no_pairs(self) -> None:
        """n=0 with no pairs => (0, [])."""
        dg = DeliveryGrouper(0, [])
        count, groups = dg.max_groups()
        assert count == 0
        assert groups == []

    def test_n_one(self) -> None:
        """n=1 => one singleton group."""
        dg = DeliveryGrouper(1, [])
        count, groups = dg.max_groups()
        assert count == 1
        assert groups == [[0]]

    def test_single_pair(self) -> None:
        """Single pair merges two packages."""
        dg = DeliveryGrouper(3, [(0, 2)])
        count, groups = dg.max_groups()
        assert count == 2
        sorted_groups = sorted(groups, key=lambda g: g[0])
        assert sorted_groups[0] == [0, 2]
        assert sorted_groups[1] == [1]


# ---------------------------------------------------------------------------
# Duplicate handling
# ---------------------------------------------------------------------------

class TestDuplicateHandling:
    """Repeated constraints should not change the result."""

    def test_duplicate_pair(self) -> None:
        """Same pair twice behaves as single pair."""
        dg = DeliveryGrouper(3, [(0, 1), (0, 1)])
        count, groups = dg.max_groups()
        assert count == 2
        sorted_groups = sorted(groups, key=lambda g: g[0])
        assert sorted_groups[0] == [0, 1]
        assert sorted_groups[1] == [2]


# ---------------------------------------------------------------------------
# Transitivity
# ---------------------------------------------------------------------------

class TestTransitivity:
    """Indirect connections must be honored."""

    def test_chain(self) -> None:
        """Chain: 0-1-2-3 => one group."""
        dg = DeliveryGrouper(4, [(0, 1), (1, 2), (2, 3)])
        count, groups = dg.max_groups()
        assert count == 1
        assert sorted(groups[0]) == [0, 1, 2, 3]

    def test_bridge_merge(self) -> None:
        """Two separate groups bridged into one."""
        dg = DeliveryGrouper(4, [(0, 1), (2, 3), (1, 2)])
        count, groups = dg.max_groups()
        assert count == 1
        assert sorted(groups[0]) == [0, 1, 2, 3]


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

class TestInputValidation:
    """Illegal inputs must raise ValueError."""

    def test_n_zero_with_pairs(self) -> None:
        """n=0 but pairs provided => ValueError."""
        with pytest.raises(ValueError):
            DeliveryGrouper(0, [(0, 1)])

    def test_out_of_range_id(self) -> None:
        """Package ID >= n => ValueError."""
        with pytest.raises(ValueError):
            DeliveryGrouper(3, [(0, 5)])

    def test_partially_out_of_range(self) -> None:
        """One ID valid, one out of range => ValueError."""
        with pytest.raises(ValueError):
            DeliveryGrouper(3, [(1, 3)])

    def test_negative_id(self) -> None:
        """Negative package ID => ValueError."""
        with pytest.raises(ValueError):
            DeliveryGrouper(3, [(-1, 0)])


# ---------------------------------------------------------------------------
# min_trucks
# ---------------------------------------------------------------------------

class TestMinTrucks:
    """Truck capacity constraint logic — same scenarios as V0."""

    def test_given_example(self) -> None:
        """Groups [0,1,2] and [3,4] with weights that fit."""
        dg = DeliveryGrouper(5, [(0, 1), (1, 2), (3, 4)])
        result = dg.min_trucks([1, 2, 3, 4, 5], 10)
        assert result == 2

    def test_single_group(self) -> None:
        """All in one group, fits in one truck."""
        dg = DeliveryGrouper(3, [(0, 1), (1, 2)])
        result = dg.min_trucks([1, 2, 3], 10)
        assert result == 1

    def test_all_independent(self) -> None:
        """No pairs => each package is a truck."""
        dg = DeliveryGrouper(3, [])
        result = dg.min_trucks([1, 2, 3], 10)
        assert result == 3

    def test_empty_groups(self) -> None:
        """n=0, no packages => 0 trucks."""
        dg = DeliveryGrouper(0, [])
        result = dg.min_trucks([], 10)
        assert result == 0

    def test_single_package(self) -> None:
        """One package, one truck."""
        dg = DeliveryGrouper(1, [])
        result = dg.min_trucks([5], 10)
        assert result == 1

    def test_exact_capacity(self) -> None:
        """Group weight == capacity => fits."""
        dg = DeliveryGrouper(2, [(0, 1)])
        result = dg.min_trucks([5, 5], 10)
        assert result == 1

    def test_one_group_overweight(self) -> None:
        """One group exceeds capacity => -1."""
        dg = DeliveryGrouper(2, [(0, 1)])
        result = dg.min_trucks([6, 6], 10)
        assert result == -1

    def test_all_groups_overweight(self) -> None:
        """All groups exceed capacity => -1."""
        dg = DeliveryGrouper(3, [(0, 1)])
        result = dg.min_trucks([6, 6, 11], 10)
        assert result == -1

    def test_second_group_overweight(self) -> None:
        """First group fits, second does not => -1."""
        dg = DeliveryGrouper(4, [(0, 1), (2, 3)])
        result = dg.min_trucks([1, 2, 6, 6], 10)
        assert result == -1

    def test_zero_capacity_raises(self) -> None:
        """capacity=0 => ValueError."""
        dg = DeliveryGrouper(2, [(0, 1)])
        with pytest.raises(ValueError):
            dg.min_trucks([1, 2], 0)

    def test_negative_capacity_raises(self) -> None:
        """Negative capacity => ValueError."""
        dg = DeliveryGrouper(2, [(0, 1)])
        with pytest.raises(ValueError):
            dg.min_trucks([1, 2], -5)

    def test_negative_weight_raises(self) -> None:
        """Negative weight => ValueError."""
        dg = DeliveryGrouper(2, [(0, 1)])
        with pytest.raises(ValueError):
            dg.min_trucks([-1, 2], 10)

    def test_weight_count_mismatch_raises(self) -> None:
        """Weight list length != total packages => ValueError."""
        dg = DeliveryGrouper(3, [(0, 1)])
        with pytest.raises(ValueError):
            dg.min_trucks([1, 2], 10)
