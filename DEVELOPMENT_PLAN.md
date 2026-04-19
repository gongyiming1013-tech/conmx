# Development Plan — Package Delivery Grouping

## Overview

Given `n` packages (numbered 0 to n-1) and a list of pair constraints `(a, b)` meaning "a and b must be delivered together," determine the maximum number of delivery groups and list the concrete groups. Constraints are transitive: if (A,B) and (B,C), then A, B, C are all in one group.

Three algorithm variants explored in V0:
- **V0 (Union-Find)** — process each pair to merge groups, then count distinct roots.
- **V0A (DFS)** — build adjacency list, find connected components via depth-first search.
- **V0B (BFS)** — build adjacency list, find connected components via breadth-first search.

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
| Union-Find (array) | Simple, no graph needed, handles duplicates naturally | No path compression in V0 | **V0** — implemented |
| DFS | Intuitive, easy to reason about components | Requires adjacency list; recursion depth for large n | **V0A** — implemented |
| BFS | Iterative, no recursion depth concern | Requires adjacency list and queue | **V0B** — implemented |

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

### V0A — DFS Implementation

**Goal:** Find connected components using DFS on an adjacency list.

**Architecture:**

```
Input (n, pairs)
    │
    ▼
validate_input(n, pairs)
    │
    ▼
max_groups_dfs(n, pairs)
    ├── build_graph(n, pairs)  # adjacency list
    └── dfs(graph, node, visited, component)  # recursive traversal
    │
    ▼
Output (group_count, groups)
```

**Functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `build_graph` | `build_graph(n: int, pairs: list[tuple[int,int]]) -> list[list[int]]` | Build adjacency list from pairs |
| `dfs` | `dfs(graph: list[list[int]], node: int, visited: list[bool], component: list[int]) -> None` | Recursively visit all nodes in a component |
| `max_groups_dfs` | `max_groups_dfs(n: int, pairs: list[tuple[int,int]]) -> tuple[int, list[list[int]]]` | Main function using DFS |

**Test Plan:** Same 5 dimensions as V0 (same interface, same expected behavior).

---

### V0B — BFS Implementation

**Goal:** Find connected components using BFS on an adjacency list.

**Architecture:**

```
Input (n, pairs)
    │
    ▼
validate_input(n, pairs)
    │
    ▼
max_groups_bfs(n, pairs)
    ├── build_graph(n, pairs)  # adjacency list
    └── bfs(graph, start, visited)  # iterative traversal with queue
    │
    ▼
Output (group_count, groups)
```

**Functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `build_graph` | `build_graph(n: int, pairs: list[tuple[int,int]]) -> list[list[int]]` | Build adjacency list from pairs |
| `bfs` | `bfs(graph: list[list[int]], start: int, visited: list[bool]) -> list[int]` | BFS from start, return all nodes in component |
| `max_groups_bfs` | `max_groups_bfs(n: int, pairs: list[tuple[int,int]]) -> tuple[int, list[list[int]]]` | Main function using BFS |

**Test Plan:** Same 5 dimensions as V0 (same interface, same expected behavior).

---

### V1 — OOD Refactor with Optimized Union-Find

**Goal:** Refactor the functional Union-Find into an object-oriented design with path compression and union by rank, separating data structure logic from domain logic via composition.

**Architecture:**

```
Input (n, pairs)
    │
    ▼
DeliveryGrouper(n, pairs)
    ├── _validate(n, pairs)              # guard clauses at construction
    ├── _uf: UnionFind                   # composition
    │       ├── find(x) -> int           # path compression
    │       ├── union(x, y) -> bool      # union by rank
    │       ├── connected(x, y) -> bool  # membership query
    │       ├── get_groups() -> list      # collect components
    │       └── component_count -> int   # property
    ├── max_groups() -> (int, list)
    └── min_trucks(weights, capacity) -> int
    │
    ▼
Output (group_count, groups)
```

**Design Patterns:**

| Pattern | Where | Why |
|---------|-------|-----|
| Composition | `DeliveryGrouper` owns a `UnionFind` instance | SRP — separates generic disjoint-set logic from domain-specific validation and grouping |

**Strategy Comparison:**

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| Single `UnionFind` class handling everything | Fewer files, simple | Violates SRP — mixes data structure with domain validation/logic | Rejected |
| `UnionFind` + `DeliveryGrouper` (composition) | Clean separation, `UnionFind` is reusable, each class has one job | Two classes | **Selected** |
| Strategy pattern with swappable algorithms (UF/DFS/BFS) | Maximum flexibility, hot-swap algorithms | Over-engineered for current requirements; V0A/V0B already serve as standalone alternatives | Deferred to V2 |

**Class & Data Structure Reference:**

| Class | Member | Signature | Description | Thread-safe |
|-------|--------|-----------|-------------|-------------|
| `UnionFind` | `__init__` | `(n: int)` | Initialize `_parent: list[int]` (self-referencing) and `_rank: list[int]` (zeros) for `n` elements | N/A |
| | `find` | `(x: int) -> int` | Return root of `x` with **path compression** (all nodes on path point directly to root) | No |
| | `union` | `(x: int, y: int) -> bool` | Merge sets of `x` and `y` by **rank**; return `True` if a merge occurred, `False` if already connected | No |
| | `connected` | `(x: int, y: int) -> bool` | Return whether `x` and `y` share the same root | No |
| | `get_groups` | `() -> list[list[int]]` | Return all connected components as sorted lists | No |
| | `component_count` | `@property -> int` | Number of distinct components (count unique roots) | No |
| `DeliveryGrouper` | `__init__` | `(n: int, pairs: list[tuple[int, int]])` | Validate input, build `UnionFind`, process all pairs. Raises `ValueError` on invalid input | N/A |
| | `max_groups` | `() -> tuple[int, list[list[int]]]` | Return `(count, groups)` delegating to `_uf.get_groups()` | No |
| | `min_trucks` | `(weights: list[int], capacity: int) -> int` | Return minimum trucks needed or `-1` if any group exceeds capacity. Raises `ValueError` on invalid weights/capacity | No |

**Test Plan:**

| Dimension | What it covers | Key scenarios |
|-----------|---------------|---------------|
| UnionFind — core ops | `find`, `union`, `connected` | Basic merge, self-union (no-op), reflexive connected, transitive merge |
| UnionFind — path compression | Tree flattening after `find` | After deep chain, verify `_parent[x] == root` for all nodes on path |
| UnionFind — union by rank | Rank-based attachment | Equal-rank merge increments rank; unequal-rank keeps higher root |
| UnionFind — components | `get_groups`, `component_count` | All singletons, one big group, mixed |
| UnionFind — edge cases | Boundary conditions | n=1 singleton, n=0 (empty), large n with no unions |
| DeliveryGrouper — core | `max_groups` behavior | Given example, no constraints, all connected (same expected output as V0) |
| DeliveryGrouper — edge cases | Boundary conditions | n=0, n=1, single pair |
| DeliveryGrouper — validation | Illegal inputs | n=0 with pairs, out-of-range IDs, negative IDs |
| DeliveryGrouper — min_trucks | Truck capacity logic | Same scenarios as V0 bonus: exact capacity, overweight, zero/negative capacity, negative weights, length mismatch |

---

### V1.1 — Quality Hardening (from code & security review)

**Goal:** Close HIGH-severity defects and test blind spots uncovered by the code-reviewer and security-reviewer passes. No public API changes, no cross-file refactors; V0/V0A/V0B/V1 remain available.

**Scope Boundary:**

- No new public functions or classes
- No change to existing public signatures
- Fixes are local to each affected file

**Changes Summary:**

| File | Change | Source finding |
|------|--------|----------------|
| `delivery_groups.py` | `min_trucks` adds structural validation for `group_list`; `max_groups` adds `n < 0` guard; module docstring | HIGH-1, MED-3, LOW-2 |
| `delivery_groups_dfs.py` | `dfs` rewritten as explicit-stack iteration; `max_groups_dfs` adds `n < 0` guard; module docstring | HIGH-2 / M-1, MED-3 |
| `delivery_groups_bfs.py` | `max_groups_bfs` adds `n < 0` guard; module docstring | MED-3 |
| `delivery_grouper.py` | `__init__` adds `n < 0` guard | MED-3 / I-1 |
| `union_find.py` | Class docstring states `get_groups` returns ascending-ordered inner groups | MED-7 |
| V0 / V0A / V0B docstrings | Declare group-internal order **undefined** | MED-7 |

**Contract Decisions:**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Group-internal order (V0/V0A/V0B) | **Undefined** | Zero runtime cost; tests already normalize via `sorted()`; preserves algorithmic purity |
| Group-internal order (V1 `UnionFind.get_groups`) | **Ascending** | Existing behavior; documented explicitly |
| Self-loop pair `(a, a)` | **Allowed**, does not affect result | All current implementations handle it naturally; locked in by equivalence test |

**Test Plan:**

| Dimension | What it covers | Key scenarios |
|-----------|---------------|---------------|
| `min_trucks` structural validation | `group_list` well-formedness | Out-of-range ID, duplicate ID across groups, empty sub-group, negative ID |
| DFS recursion depth | Iterative traversal correctness on deep chains | `n=2000` chain input — no `RecursionError`, returns single component of size 2000 |
| Negative `n` guard | All four entry points | `max_groups(-1, [])`, `max_groups_bfs(-1, [])`, `max_groups_dfs(-1, [])`, `DeliveryGrouper(-1, [])` all raise `ValueError` |
| Cross-algorithm equivalence | V0/V0A/V0B/V1 agree on all inputs | Parametrized over: empty, singleton, all-isolated, full chain, disjoint pairs, duplicates, self-loop, out-of-order pairs |
| Group-order contract | Lock documented behavior | V1 `get_groups` returns each group ascending; V0 variants tested via set-equivalence only |

**Deferred to later versions (from review, intentionally out of scope for V1.1):**

| Item | Reason for deferral |
|------|---------------------|
| Extract shared `_validate_pairs` / `_build_graph` util (MED-2) | Cross-file refactor; separate version |
| Remove redundant `sorted()` in `UnionFind.get_groups` (MED-4) | Would break current ascending-order contract |
| `cached_property` for `DeliveryGrouper.groups` (MED-8) | Non-functional optimization |
| `requirements.txt` / lockfile (L-2) | Infrastructure layer; independent branch |
| PEP 8 spacing, `_` prefix on helpers, test renaming (LOW-1/8, LOW-7) | Style sweep via `code-simplifier` |

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

### V0A — DFS Implementation

**Scope:** Implement connected component detection using DFS. Build adjacency list from pairs, then recursively traverse to find all components. Same input validation and test cases as V0.

- [x] Create `delivery_groups_dfs.py` with `build_graph`, `dfs`, `max_groups_dfs` functions
- [x] Create `test_delivery_groups_dfs.py` with all test cases
- [x] Verify all tests pass and coverage ≥ 95% (achieved 100%)

### V0B — BFS Implementation

**Scope:** Implement connected component detection using BFS. Build adjacency list from pairs, then iteratively traverse with a queue to find all components. Same input validation and test cases as V0.

- [x] Create `delivery_groups_bfs.py` with `build_graph`, `bfs`, `max_groups_bfs` functions
- [x] Create `test_delivery_groups_bfs.py` with all test cases
- [x] Verify all tests pass and coverage ≥ 95% (achieved 100%)

### V1 — OOD Refactor with Optimized Union-Find

**Scope:** Refactor the V0 functional implementation into two classes following OOD principles. `UnionFind` is a general-purpose disjoint-set data structure with path compression and union by rank (near-constant amortized time). `DeliveryGrouper` composes `UnionFind` and encapsulates domain-specific input validation, grouping, and truck capacity logic. This separation makes `UnionFind` independently reusable and keeps each class focused on a single responsibility.

- [x] Create `union_find.py` with `UnionFind` class
  - [x] `__init__(n)` — initialize `_parent` and `_rank` arrays
  - [x] `find(x)` — iterative root lookup with path compression
  - [x] `union(x, y)` — merge by rank, return `bool`
  - [x] `connected(x, y)` — same-root check
  - [x] `get_groups()` — collect all components as sorted lists
  - [x] `component_count` property — count distinct roots
- [x] Create `delivery_grouper.py` with `DeliveryGrouper` class
  - [x] `__init__(n, pairs)` — validate input and build internal `UnionFind`
  - [x] `max_groups()` — return `(count, groups)`
  - [x] `min_trucks(weights, capacity)` — return min trucks or `-1`
- [x] Create `test_union_find.py` with `UnionFind` unit tests
  - [x] Core operations (find, union, connected)
  - [x] Path compression verification
  - [x] Union by rank verification
  - [x] Components (get_groups, component_count)
  - [x] Edge cases (n=1, n=0, no unions)
- [x] Create `test_delivery_grouper.py` with `DeliveryGrouper` tests
  - [x] Core functionality (given example, no constraints, all connected)
  - [x] Edge cases (n=0, n=1, single pair)
  - [x] Duplicate pairs
  - [x] Transitivity (chain, bridge merge)
  - [x] Input validation errors
  - [x] min_trucks (all existing V0 scenarios)
- [x] Verify all tests pass and coverage ≥ 95% (achieved 100%)

### V1.1 — Quality Hardening (from code & security review)

**Scope:** Close HIGH-severity defects and test blind spots identified by the code-reviewer + security-reviewer pass. Purely additive validation + one DFS rewrite. No new public API, no cross-file refactors, no changes to V0/V0A/V0B/V1 public signatures.

- [x] `delivery_groups.py`
  - [x] Add module-level docstring
  - [x] Add `n < 0` guard in `max_groups`
  - [x] Add structural validation in `min_trucks` (IDs in `[0, len(weights))`, no cross-group duplicates, no empty sub-groups); reorder guards to top
  - [x] Update docstrings: state group-internal order is undefined
- [x] `delivery_groups_dfs.py`
  - [x] Add module-level docstring
  - [x] Rewrite `dfs` as explicit-stack iterative traversal (same signature)
  - [x] Add `n < 0` guard in `max_groups_dfs`
  - [x] Update docstring: state group-internal order is undefined
- [x] `delivery_groups_bfs.py`
  - [x] Add module-level docstring
  - [x] Add `n < 0` guard in `max_groups_bfs`
  - [x] Update docstring: state group-internal order is undefined
- [x] `delivery_grouper.py`
  - [x] Add `n < 0` guard in `__init__`
- [x] `union_find.py`
  - [x] Document ascending-order contract for `get_groups` in class docstring
- [x] Tests
  - [x] `test_delivery_groups.py`: add `test_min_trucks_rejects_out_of_range_id`, `test_min_trucks_rejects_duplicate_id_across_groups`, `test_min_trucks_rejects_empty_subgroup`, `test_min_trucks_rejects_negative_id`, `test_min_trucks_rejects_weights_longer_than_total`, `test_negative_n_raises`
  - [x] `test_delivery_groups_dfs.py`: add `test_dfs_handles_long_chain_without_recursion_error`, `test_negative_n_raises`, `test_self_loop_pair_is_accepted`
  - [x] `test_delivery_groups_bfs.py`: add `test_negative_n_raises`, `test_self_loop_pair_is_accepted`
  - [x] `test_delivery_grouper.py`: add `test_negative_n_raises`, `test_self_loop_pair_is_accepted`
  - [x] Create `test_algorithm_equivalence.py` with parametrized cross-algorithm equivalence test
- [x] Verify all tests pass and coverage ≥ 95% (achieved 100% branch coverage, 123/123 tests pass)
