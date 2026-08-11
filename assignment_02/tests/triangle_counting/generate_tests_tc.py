#!/usr/bin/env python3

"""
Triangle Counting test generator for CS509 Assignment 02.

Graphs:
    - Unweighted
    - Undirected
    - Vertices numbered 0 .. V-1
    - Each undirected edge appears in both adjacency lists

Input format (no SOURCE line -- triangle counting runs over the whole graph):
    V E
    vertex degree neighbor1 neighbor2 ...
    ...

Design idea: most graphs below are built from families whose exact triangle
count can be computed with a formula (cliques, wheels, windmills, disjoint
triangles) or, for small graphs, brute force. That means you know the
expected "Total triangles" value BEFORE running your C++ driver, so you can
verify correctness independently -- not just check that the program runs.
"""

from pathlib import Path
from itertools import combinations
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


def write_graph(filename, graph, expected_triangles=None):
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

    if expected_triangles is not None:
        print(f"Generated {filename}: V={n}, E={e}, expected triangles={expected_triangles}")
    else:
        print(f"Generated {filename}: V={n}, E={e}")


def count_triangles_bruteforce(graph):
    """
    O(V^3) exact check. Only use on small graphs (roughly V <= 300) --
    this exists purely to double-check the analytic formulas below, and to
    give an expected value for graphs that don't have a clean formula.
    """

    n = len(graph)
    total = 0

    for u, v, w in combinations(range(n), 3):
        if v in graph[u] and w in graph[u] and w in graph[v]:
            total += 1

    return total


# ------------------------------------------------------------
# Triangle-free graph families
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
    """Triangle-free unless n == 3 (a 3-cycle IS a triangle)."""

    g = make_graph(n)

    if n >= 3:
        for i in range(n):
            add_edge(g, i, (i + 1) % n)

    return g


def star_graph(n):
    """Tree -> always 0 triangles."""

    g = make_graph(n)

    for i in range(1, n):
        add_edge(g, 0, i)

    return g


def tree_graph(n):
    """Deterministic binary-tree-like structure. Always 0 triangles."""

    g = make_graph(n)

    for v in range(1, n):
        parent = (v - 1) // 2
        add_edge(g, parent, v)

    return g


def grid_graph(rows, cols):
    """Square grid, no diagonals -> always 0 triangles."""

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


def complete_bipartite_graph(left, right):
    """Bipartite -> no odd cycles -> always 0 triangles."""

    n = left + right
    g = make_graph(n)

    for u in range(left):
        for v in range(left, n):
            add_edge(g, u, v)

    return g


# ------------------------------------------------------------
# Triangle-rich graph families (exact count known by formula)
# ------------------------------------------------------------

def complete_graph(n):
    """Every triple of vertices is a triangle: C(n, 3) total."""

    g = make_graph(n)

    for u in range(n):
        for v in range(u + 1, n):
            add_edge(g, u, v)

    return g


def complete_graph_triangle_count(n):
    if n < 3:
        return 0
    return n * (n - 1) * (n - 2) // 6


def windmill_graph(k):
    """
    "Friendship graph" F_k: one hub vertex (0) plus k independent pairs,
    each pair forming a triangle with the hub. Vertices = 2k + 1.
    Exact triangle count = k (the k triangles never overlap except at hub).
    """

    n = 2 * k + 1
    g = make_graph(n)

    for i in range(k):
        a = 1 + 2 * i
        b = 2 + 2 * i
        add_edge(g, 0, a)
        add_edge(g, 0, b)
        add_edge(g, a, b)

    return g, k


def disjoint_triangles_graph(k):
    """k separate, non-touching triangles. Vertices = 3k. Count = k."""

    n = 3 * k
    g = make_graph(n)

    for i in range(k):
        a, b, c = 3 * i, 3 * i + 1, 3 * i + 2
        add_edge(g, a, b)
        add_edge(g, b, c)
        add_edge(g, a, c)

    return g, k


def wheel_graph(n):
    """
    Vertex 0 is the hub, vertices 1..n-1 form a rim cycle.
    Every rim edge + the two spokes to its endpoints forms a triangle,
    so the exact count = n - 1 (the rim length), for n >= 4.
    """

    g = make_graph(n)

    if n < 4:
        return g, 0

    rim = n - 1

    for i in range(1, n):
        add_edge(g, 0, i)

    for i in range(rim):
        u = 1 + i
        v = 1 + (i + 1) % rim
        add_edge(g, u, v)

    return g, rim


def clustered_graph(n, cluster_size=4):
    """
    Chops n vertices into cliques of 'cluster_size' (last cluster may be
    smaller), then chains the cliques together with single bridge edges
    (bridges never create a triangle). Exact triangle count is the sum of
    C(k, 3) over each cluster's size k -- computed WITHOUT brute force, so
    this scales cleanly up to V = 100,000.
    """

    g = make_graph(n)
    clusters = []

    i = 0
    while i < n:
        size = min(cluster_size, n - i)
        clusters.append(list(range(i, i + size)))
        i += size

    for cluster in clusters:
        for a in range(len(cluster)):
            for b in range(a + 1, len(cluster)):
                add_edge(g, cluster[a], cluster[b])

    for c in range(len(clusters) - 1):
        u = clusters[c][-1]
        v = clusters[c + 1][0]
        add_edge(g, u, v)  # bridge, no triangle added

    expected = sum(complete_graph_triangle_count(len(c)) for c in clusters)

    return g, expected


# ------------------------------------------------------------
# Random graphs
# ------------------------------------------------------------

def random_graph(n, probability, seed):
    """O(n^2) -- fine for small/medium n, avoid for very large n."""

    rng = random.Random(seed)
    g = make_graph(n)

    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < probability:
                add_edge(g, u, v)

    return g


def random_sparse_graph(n, edges, seed):
    """
    Generates up to 'edges' unique undirected edges by direct sampling
    (not O(n^2)), so this is safe for very large n.
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
    Optional robustness case: the input contains duplicate adjacency
    entries. Not a standard simple-graph case -- see how your driver
    handles it (e.g. does hasEdge / sorting break, or does it just work).
    """

    n = 4

    rows = [
        [1, 1],
        [0, 0, 2],
        [1, 3],
        [2],
    ]

    path = OUTPUT_DIR / "tc_duplicate_edges.txt"

    with open(path, "w") as f:
        f.write("4 4\n")

        for u in range(n):
            neighbors = rows[u]
            f.write(f"{u} {len(neighbors)}")
            f.write(" " + " ".join(map(str, neighbors)))
            f.write("\n")

    print("Generated tc_duplicate_edges.txt")


def self_loop_graph():
    """Optional robustness case: self-loops are outside the simple-graph model."""

    path = OUTPUT_DIR / "tc_self_loop.txt"

    with open(path, "w") as f:
        f.write("4 3\n")
        f.write("0 2 0 1\n")
        f.write("1 2 0 2\n")
        f.write("2 2 1 3\n")
        f.write("3 1 2\n")

    print("Generated tc_self_loop.txt")


# ------------------------------------------------------------
# Required Assignment 2 sizes: 10, 100, 10000, 50000, 100000
# ------------------------------------------------------------

def generate_required_tests():
    required_sizes = [10, 100, 10000, 50000, 100000]

    for n in required_sizes:
        # cluster_size=4 keeps generation O(n) even at V=100,000, and the
        # expected triangle count is exact (sum of C(4,3)=4 per cluster).
        g, expected = clustered_graph(n, cluster_size=4)
        write_graph(f"tc_{n}.txt", g, expected)

    # Extra structured performance tests at V=1000
    g = path_graph(1000)
    write_graph("tc_path_1000.txt", g, expected_triangles=0)

    g = cycle_graph(1000)
    write_graph("tc_cycle_1000.txt", g, expected_triangles=0)

    g = star_graph(1000)
    write_graph("tc_star_1000.txt", g, expected_triangles=0)

    g = tree_graph(1000)
    write_graph("tc_tree_1000.txt", g, expected_triangles=0)

    g, expected = clustered_graph(1000, cluster_size=6)
    write_graph("tc_clustered_1000.txt", g, expected)

    g = random_sparse_graph(1000, 2000, seed=2001)
    write_graph("tc_random_sparse_1000.txt", g)  # no closed-form count; cross-check in your driver

    g = random_sparse_graph(1000, 5000, seed=2002)
    write_graph("tc_random_medium_1000.txt", g)


# ------------------------------------------------------------
# Exhaustive small tests (exact expected counts, verified by formula
# and/or brute force so you can hand-check your driver's output)
# ------------------------------------------------------------

def generate_small_tests():
    tests_with_known_counts = [
        ("tc_empty_1.txt", empty_graph(1), 0),
        ("tc_empty_5.txt", empty_graph(5), 0),
        ("tc_single_edge.txt", single_edge_graph(2), 0),
        ("tc_triangle.txt", complete_graph(3), complete_graph_triangle_count(3)),
        ("tc_path_5.txt", path_graph(5), 0),
        ("tc_path_10.txt", path_graph(10), 0),
        ("tc_cycle_3.txt", cycle_graph(3), 1),
        ("tc_cycle_5.txt", cycle_graph(5), 0),
        ("tc_cycle_10.txt", cycle_graph(10), 0),
        ("tc_star_5.txt", star_graph(5), 0),
        ("tc_star_10.txt", star_graph(10), 0),
        ("tc_complete_4.txt", complete_graph(4), complete_graph_triangle_count(4)),
        ("tc_complete_5.txt", complete_graph(5), complete_graph_triangle_count(5)),
        ("tc_complete_6.txt", complete_graph(6), complete_graph_triangle_count(6)),
        ("tc_complete_8.txt", complete_graph(8), complete_graph_triangle_count(8)),
        ("tc_bipartite_3x3.txt", complete_bipartite_graph(3, 3), 0),
        ("tc_bipartite_4x4.txt", complete_bipartite_graph(4, 4), 0),
        ("tc_grid_3x3.txt", grid_graph(3, 3), 0),
        ("tc_grid_4x4.txt", grid_graph(4, 4), 0),
        ("tc_tree_10.txt", tree_graph(10), 0),
    ]

    for filename, graph, expected in tests_with_known_counts:
        write_graph(filename, graph, expected)

    # Families that return their own expected count alongside the graph
    g, expected = windmill_graph(3)
    write_graph("tc_windmill_3.txt", g, expected)

    g, expected = windmill_graph(5)
    write_graph("tc_windmill_5.txt", g, expected)

    g, expected = disjoint_triangles_graph(4)
    write_graph("tc_disjoint_triangles_4.txt", g, expected)

    g, expected = wheel_graph(10)
    write_graph("tc_wheel_10.txt", g, expected)

    g, expected = wheel_graph(20)
    write_graph("tc_wheel_20.txt", g, expected)

    g, expected = clustered_graph(20, cluster_size=5)
    write_graph("tc_clustered_20.txt", g, expected)


# ------------------------------------------------------------
# Random small tests, cross-checked with brute force (safe up to ~V=200)
# ------------------------------------------------------------

def generate_random_small_tests():
    configurations = [
        (6, 0.20, 3001),
        (6, 0.40, 3002),
        (6, 0.60, 3003),
        (8, 0.20, 3004),
        (8, 0.40, 3005),
        (8, 0.60, 3006),
        (10, 0.20, 3007),
        (10, 0.40, 3008),
        (10, 0.60, 3009),
        (15, 0.15, 3010),
        (15, 0.30, 3011),
        (20, 0.10, 3012),
        (20, 0.25, 3013),
    ]

    for index, (n, probability, seed) in enumerate(configurations, 1):
        g = random_graph(n, probability, seed)
        expected = count_triangles_bruteforce(g)  # cheap at this size
        write_graph(f"tc_random_small_{index:02d}.txt", g, expected)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGenerating small, exact-count Triangle Counting test cases...\n")
    generate_small_tests()

    print("\nGenerating random small graphs (brute-force verified)...\n")
    generate_random_small_tests()

    print("\nGenerating required Assignment 2 sizes...\n")
    generate_required_tests()

    print("\nGenerating optional robustness tests...\n")
    duplicate_edge_graph()
    self_loop_graph()

    print("\nAll Triangle Counting test cases generated.")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()