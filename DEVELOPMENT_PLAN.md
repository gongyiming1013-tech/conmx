# Development Plan — Package Delivery Grouping

## Overview

Given `n` packages (numbered 0 to n-1) and a list of pair constraints `(a, b)` meaning "a and b must be delivered together," determine the maximum number of delivery groups and list the concrete groups. Constraints are transitive: if (A,B) and (B,C), then A, B, C are all in one group.

Core algorithm: **Union-Find** — process each pair to merge groups, then count distinct roots.

---

## Design

### V0 — Simple Functional Implementation

**Goal:** Deliver a minimal, function-based Python solution with input validation and comprehensive tests.

**Architecture:**

```
Input (n, pairs)          # packages: 0 to n-1
    │
    ▼
validate_input(n, pairs)  # IDs must be in [0, n-1]
    │
    ▼
max_groups(n, pairs)
    ├── find(parent, x)      # follow parent chain to root
    ├── union(parent, x, y)  # merge two roots
    └── collect groups by root
    │
    ▼
Output (group_count, groups)
```

**Design Patterns:** None — V0 uses plain functions only, no OOD.

**Strategy Comparison:**

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| Union-Find (array) | Simple, no graph needed, handles duplicates naturally | No path compression in V0 | **Chosen** — simplest for V0 |
| DFS/BFS | Intuitive graph traversal | Requires building adjacency list first | Deferred to V1 if needed |

**Functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `find` | `find(parent: list[int], x: int) -> int` | Follow parent pointers to find root |
| `union` | `union(parent: list[int], x: int, y: int) -> None` | Merge group of x into group of y |
| `max_groups` | `max_groups(n: int, pairs: list[tuple[int,int]]) -> tuple[int, list[list[int]]]` | Main function: returns (count, groups). Package IDs are 0 to n-1 |

**Test Plan:**

| Dimension | What it covers | Key scenarios |
|-----------|---------------|---------------|
| Core functionality | Basic grouping logic | Given example, all connected, no constraints |
| Edge cases | Boundary conditions | n=0, n=1, single pair |
| Duplicate handling | Repeated constraints | Same pair twice |
| Transitivity | Indirect connections | Chain, bridge merge |
| Input validation | Illegal inputs | n=0 with pairs, out-of-range IDs |

---

### V1 (Planned)

**Goal:** Add path compression, union by rank, and potentially OOD refactor.

**Strategy Comparison:** TBD

**Design Discussion:** Should we introduce a `UnionFind` class? Add support for arbitrary package IDs (not just 1..n)?

**Class & Data Structure Changes:** TBD

**Test Plan:** TBD

---

## Roadmap & Implementation

### V0 — Simple Functional Implementation

**Scope:** Implement the Union-Find algorithm as plain Python functions. Include lightweight input validation (check package IDs in range, check n≥0). Return both the number of groups and the concrete group lists. Full test coverage using pytest.

- [x] Create `delivery_groups.py` with `find`, `union`, `max_groups` functions
- [x] Add input validation in `max_groups` (IDs must be in [0, n-1], n=0 with pairs)
- [x] Create `test_delivery_groups.py` with all test cases:
  - [x] Core functionality (given example, no constraints, all connected)
  - [x] Edge cases (n=0, n=1, single pair)
  - [x] Duplicate pairs
  - [x] Transitivity (chain, bridge merge)
  - [x] Input validation errors
- [x] Verify all tests pass and coverage ≥ 95% (achieved 100%)

### V1 — Optimization & OOD Refactor (Planned)

**Scope:** Introduce path compression and union by rank for performance. Potentially refactor into a `UnionFind` class following OOD principles.

- [ ] Design discussion and strategy comparison
- [ ] Implementation
- [ ] Test updates
