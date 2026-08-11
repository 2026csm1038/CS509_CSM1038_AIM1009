#!/usr/bin/env python3

"""
Betweenness Centrality test generator for CS509 Assignment 02.

Graphs:
    - Unweighted
    - Undirected
    - Vertices numbered 0 .. V-1
    - Each undirected edge appears in both adjacency lists

Input format:
    V E
    vertex degree neighbor1 neighbor2 ...
    ...
    
The driver computes raw (unnormalized) betweenness centrality.
"""

from pathlib import Path
import random


OUTPUT_DIR = Path(__file__).resolve().parent


# ------------------------------------------------------------
# Graph utilities
# ------------------------------------------------------------

def make_graph(n):
    return [set() for _ in range(n)]


def add_edge(graph, u, v):
    if u == v:
        return

    graph[u].add(v)
    graph[v].add(u)


def add_edges(graph, edges):
    for u, v in edges:
        add_edge(graph, u, v)


def edge_count(graph):
    return sum(len(neighbors) for neighbors in graph) // 2


def write_graph(filename, graph):
    path = OUTPUT_DIR / filename

    n = len(graph)
    e = edge_count(graph)

    with open(path, "w") as f:
        f.write(f"{n} {e}\n")

        for u in range(n):
            neighbors = sorted(graph[u])
            f.write(f"{u} {len(neighbors)}")

            if neighbors:
                f.write(" " + " ".join(map(str, neighbors)))

            f.write("\n")

    print(f"Generated {filename}: V={n}, E={e}")


# ------------------------------------------------------------
# Basic graph families
# ------------------------------------------------------------

def empty_graph(n):
    return make_graph(n)


def single_edge_graph(n):
    g = make_graph(n)

    if n >= 2:
        add_edge(g, 0, 1)

    return g


def path_graph(n):
    g = make_graph(n)

    for i in range(n - 1):
        add_edge(g, i, i + 1)

    return g


def cycle_graph(n):
    g = make_graph(n)

    if n >= 2:
        for i in range(n):
            add_edge(g, i, (i + 1) % n)

    return g


def star_graph(n):
    g = make_graph(n)

    for i in range(1, n):
        add_edge(g, 0, i)

    return g


def complete_graph(n):
    g = make_graph(n)

    for u in range(n):
        for v in range(u + 1, n):
            add_edge(g, u, v)

    return g


def complete_bipartite_graph(left, right):
    n = left + right
    g = make_graph(n)

    for u in range(left):
        for v in range(left, n):
            add_edge(g, u, v)

    return g


def wheel_graph(n):
    """
    Vertex 0 is the center.
    Vertices 1..n-1 form a cycle.
    """

    g = make_graph(n)

    if n < 4:
        return g

    for i in range(1, n):
        add_edge(g, 0, i)

    for i in range(1, n):
        add_edge(g, i, 1 + (i - 1 + 1) % (n - 1))

    return g


def grid_graph(rows, cols):
    n = rows * cols
    g = make_graph(n)

    def vertex(r, c):
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            u = vertex(r, c)

            if r + 1 < rows:
                add_edge(g, u, vertex(r + 1, c))

            if c + 1 < cols:
                add_edge(g, u, vertex(r, c + 1))

    return g


# ------------------------------------------------------------
# Special BC graphs
# ------------------------------------------------------------

def two_paths_graph():
    """
    Two equal-length paths connecting vertices 0 and 5.

        0--1--2--5
         \      /
          3--4

    Creates multiple shortest paths.
    """

    g = make_graph(6)

    edges = [
        (0, 1),
        (1, 2),
        (2, 5),
        (0, 3),
        (3, 4),
        (4, 5),
    ]

    add_edges(g, edges)

    return g


def diamond_graph():
    """
        0
       / \
      1   2
       \ /
        3

    Multiple shortest paths between 0 and 3.
    """

    g = make_graph(4)

    add_edges(
        g,
        [
            (0, 1),
            (0, 2),
            (1, 3),
            (2, 3),
        ],
    )

    return g


def bridge_graph():
    """
    Two dense components connected by a single bridge.

    The bridge endpoints should have high BC.
    """

    g = make_graph(10)

    # Left clique: 0..4
    for u in range(5):
        for v in range(u + 1, 5):
            add_edge(g, u, v)

    # Right clique: 5..9
    for u in range(5, 10):
        for v in range(u + 1, 10):
            add_edge(g, u, v)

    # Single bridge
    add_edge(g, 4, 5)

    return g


def lollipop_graph(clique_size, path_length):
    """
    Clique connected to a path.

    Useful for testing strong bottlenecks.
    """

    n = clique_size + path_length
    g = make_graph(n)

    # Clique
    for u in range(clique_size):
        for v in range(u + 1, clique_size):
            add_edge(g, u, v)

    # Path starting from the last clique vertex
    start = clique_size - 1

    for i in range(path_length):
        u = start + i
        v = start + i + 1

        if v < n:
            add_edge(g, u, v)

    return g


def tree_graph(n):
    """
    Deterministic binary-tree-like structure.
    """

    g = make_graph(n)

    for v in range(1, n):
        parent = (v - 1) // 2
        add_edge(g, parent, v)

    return g


def two_component_graph():
    """
    Several disconnected components:

    component 1: path
    component 2: triangle
    component 3: isolated vertices
    """

    g = make_graph(10)

    # Path: 0-1-2-3
    add_edges(
        g,
        [
            (0, 1),
            (1, 2),
            (2, 3),
        ],
    )

    # Triangle: 4-5-6-4
    add_edges(
        g,
        [
            (4, 5),
            (5, 6),
            (6, 4),
        ],
    )

    # 7, 8, 9 remain isolated

    return g


# ------------------------------------------------------------
# Random graphs
# ------------------------------------------------------------

def random_graph(n, probability, seed):
    rng = random.Random(seed)

    g = make_graph(n)

    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < probability:
                add_edge(g, u, v)

    return g


def random_sparse_graph(n, edges, seed):
    """
    Generates exactly up to 'edges' unique undirected edges.
    """

    rng = random.Random(seed)
    g = make_graph(n)

    max_edges = n * (n - 1) // 2
    edges = min(edges, max_edges)

    selected = set()

    while len(selected) < edges:
        u = rng.randrange(n)
        v = rng.randrange(n)

        if u == v:
            continue

        if u > v:
            u, v = v, u

        selected.add((u, v))

    add_edges(g, selected)

    return g


# ------------------------------------------------------------
# Robustness graphs
# ------------------------------------------------------------

def duplicate_edge_graph():
    """
    Optional robustness case.

    The input contains duplicate adjacency entries.
    This is NOT a standard simple-graph case.
    """

    n = 4

    rows = [
        [1, 1],
        [0, 0, 2],
        [1, 3],
        [2],
    ]

    path = OUTPUT_DIR / "bc_duplicate_edges.txt"

    with open(path, "w") as f:
        f.write("4 4\n")

        for u in range(n):
            neighbors = rows[u]
            f.write(f"{u} {len(neighbors)}")
            f.write(" " + " ".join(map(str, neighbors)))
            f.write("\n")

    print("Generated bc_duplicate_edges.txt")


def self_loop_graph():
    """
    Optional robustness case.

    Self-loops are outside the normal simple undirected graph model.
    """

    path = OUTPUT_DIR / "bc_self_loop.txt"

    with open(path, "w") as f:
        f.write("4 3\n")
        f.write("0 2 0 1\n")
        f.write("1 2 0 2\n")
        f.write("2 2 1 3\n")
        f.write("3 1 2\n")

    print("Generated bc_self_loop.txt")


# ------------------------------------------------------------
# Required Assignment 2 sizes
# ------------------------------------------------------------

def generate_required_tests():
    # Required BC sizes:
    # 10, 100, 1000, 5000, 10000

    required_sizes = [10, 100, 1000, 5000, 10000]

    for n in required_sizes:

        # Sparse deterministic graph
        if n <= 100:
            edges = max(n - 1, 2 * n)
        else:
            edges = 2 * n

        g = random_sparse_graph(
            n,
            edges,
            seed=1000 + n,
        )

        write_graph(f"bc_{n}.txt", g)

    # Extra structured performance tests

    g = path_graph(1000)
    write_graph("bc_path_1000.txt", g)

    g = star_graph(1000)
    write_graph("bc_star_1000.txt", g)

    g = cycle_graph(1000)
    write_graph("bc_cycle_1000.txt", g)

    g = tree_graph(1000)
    write_graph("bc_tree_1000.txt", g)

    g = random_graph(1000, 0.01, seed=2001)
    write_graph("bc_random_sparse_1000.txt", g)

    g = random_graph(1000, 0.05, seed=2002)
    write_graph("bc_random_medium_1000.txt", g)


# ------------------------------------------------------------
# Exhaustive small tests
# ------------------------------------------------------------

def generate_small_tests():

    tests = {
        "bc_empty_1.txt": empty_graph(1),

        "bc_empty_2.txt": empty_graph(2),

        "bc_single_edge.txt": single_edge_graph(2),

        "bc_path_3.txt": path_graph(3),

        "bc_path_4.txt": path_graph(4),

        "bc_path_5.txt": path_graph(5),

        "bc_path_10.txt": path_graph(10),

        "bc_cycle_3.txt": cycle_graph(3),

        "bc_cycle_4.txt": cycle_graph(4),

        "bc_cycle_5.txt": cycle_graph(5),

        "bc_cycle_10.txt": cycle_graph(10),

        "bc_star_4.txt": star_graph(4),

        "bc_star_5.txt": star_graph(5),

        "bc_star_10.txt": star_graph(10),

        "bc_complete_3.txt": complete_graph(3),

        "bc_complete_4.txt": complete_graph(4),

        "bc_complete_5.txt": complete_graph(5),

        "bc_complete_6.txt": complete_graph(6),

        "bc_two_paths.txt": two_paths_graph(),

        "bc_diamond.txt": diamond_graph(),

        "bc_bridge.txt": bridge_graph(),

        "bc_lollipop.txt": lollipop_graph(5, 5),

        "bc_tree_10.txt": tree_graph(10),

        "bc_components.txt": two_component_graph(),

        "bc_bipartite_3x3.txt": complete_bipartite_graph(3, 3),

        "bc_bipartite_4x4.txt": complete_bipartite_graph(4, 4),

        "bc_grid_3x3.txt": grid_graph(3, 3),

        "bc_grid_4x4.txt": grid_graph(4, 4),

        "bc_wheel_10.txt": wheel_graph(10),
    }

    for filename, graph in tests.items():
        write_graph(filename, graph)


# ------------------------------------------------------------
# Random small exhaustive-style tests
# ------------------------------------------------------------

def generate_random_small_tests():

    configurations = [
        (6, 0.20, 3001),
        (6, 0.40, 3002),
        (6, 0.60, 3003),
        (6, 0.80, 3004),
        (8, 0.20, 3005),
        (8, 0.40, 3006),
        (8, 0.60, 3007),
        (8, 0.80, 3008),
        (10, 0.20, 3009),
        (10, 0.40, 3010),
        (10, 0.60, 3011),
        (10, 0.80, 3012),
        (15, 0.15, 3013),
        (15, 0.30, 3014),
        (15, 0.50, 3015),
    ]

    for index, (n, probability, seed) in enumerate(configurations, 1):

        g = random_graph(n, probability, seed)

        write_graph(
            f"bc_random_small_{index:02d}.txt",
            g,
        )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGenerating Betweenness Centrality test cases...\n")

    generate_small_tests()

    print("\nGenerating random small graphs...\n")
    generate_random_small_tests()

    print("\nGenerating required Assignment 2 sizes...\n")
    generate_required_tests()

    print("\nGenerating optional robustness tests...\n")
    duplicate_edge_graph()
    self_loop_graph()

    print("\nAll BC test cases generated.")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
