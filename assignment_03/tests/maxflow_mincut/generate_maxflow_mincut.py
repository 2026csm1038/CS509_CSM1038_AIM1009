import random
from pathlib import Path


OUTPUT_DIR = Path("assignment_03/tests/maxflow_mincut")


def write_graph(filename, vertices, edges, source, sink):
    """
    Write a directed capacitated graph in the format required
    by Assignment 3.

    edges:
        list of (u, v, capacity)
    """

    outgoing = [[] for _ in range(vertices)]

    for u, v, capacity in edges:
        outgoing[u].append((v, capacity))

    with (OUTPUT_DIR / filename).open("w") as file:
        file.write(f"{vertices} {len(edges)}\n")

        for u in range(vertices):
            file.write(f"{u} {len(outgoing[u])}")

            for v, capacity in outgoing[u]:
                file.write(f" {v} {capacity}")

            file.write("\n")

        file.write(f"SOURCE {source}\n")
        file.write(f"SINK {sink}\n")


def add_edge(edges, u, v, capacity):
    """
    Add one directed capacity edge.
    """
    edges.append((u, v, capacity))


def make_chain(vertices, capacity=10):
    """
    Creates:

        0 -> 1 -> 2 -> ... -> V-1

    Source = 0
    Sink   = V-1
    """
    edges = []

    for u in range(vertices - 1):
        add_edge(edges, u, u + 1, capacity)

    return edges


def make_two_path_graph():
    """
    Two independent paths from source to sink.

            1 ----\
          /        \
        0            5
          \        /
            2 ----/

    Maximum flow = 10 + 7 = 17
    """

    edges = [
        (0, 1, 10),
        (1, 5, 10),

        (0, 2, 7),
        (2, 5, 7),

        (1, 3, 4),
        (3, 4, 4),
        (4, 5, 4),
    ]

    return edges


def make_bottleneck_graph():
    """
    Multiple paths exist, but a common bottleneck limits
    the total flow.

            1 ----\
          /        \
        0 ---- 3 ---- 5
          \        /
            2 ----/

    The edge 3 -> 5 is the bottleneck.
    """

    edges = [
        (0, 1, 20),
        (0, 2, 15),

        (1, 3, 20),
        (2, 3, 15),

        (3, 5, 10),
    ]

    return edges


def make_direct_edge_graph():
    """
    Direct source -> sink edge plus an alternative path.
    """

    edges = [
        (0, 3, 8),
        (0, 1, 10),
        (1, 2, 10),
        (2, 3, 10),
    ]

    return edges


def make_cycle_graph():
    """
    Contains cycles while maintaining an s -> t path.
    """

    edges = [
        (0, 1, 10),
        (1, 2, 8),
        (2, 3, 6),
        (3, 5, 5),

        (2, 1, 3),
        (3, 2, 2),

        (0, 4, 7),
        (4, 5, 7),
    ]

    return edges


def make_parallel_edge_graph():
    """
    Parallel directed edges between the same vertices.

    This is useful because the implementation uses an explicit
    residual graph and must correctly handle multiple edges.
    """

    edges = [
        (0, 1, 5),
        (0, 1, 7),
        (0, 1, 3),

        (1, 2, 8),
        (1, 2, 4),

        (2, 3, 12),
    ]

    return edges


def make_equal_paths_graph():
    """
    Several paths with equal capacities.
    """

    edges = [
        (0, 1, 5),
        (1, 5, 5),

        (0, 2, 5),
        (2, 5, 5),

        (0, 3, 5),
        (3, 5, 5),

        (0, 4, 5),
        (4, 5, 5),
    ]

    return edges


def make_disconnected_graph():
    """
    Source and sink are connected, but some vertices are
    completely outside the s-t network.

    This is still a valid test because the specification
    requires at least one source-to-sink path.
    """

    edges = [
        # Main s-t network
        (0, 1, 10),
        (1, 5, 10),

        # Separate component
        (6, 7, 20),
        (7, 8, 20),

        # Another isolated part
        (3, 4, 5),
    ]

    return edges


def make_example_graph():
    """
    Graph based on the Assignment 3 example.

    Expected maximum flow = 23.
    """

    return [
        (0, 1, 16),
        (0, 2, 13),

        (1, 2, 10),
        (1, 3, 12),

        (2, 1, 4),
        (2, 4, 14),

        (3, 2, 9),
        (3, 5, 20),

        (4, 3, 7),
        (4, 5, 4),
    ]


def make_random_sparse_graph(vertices, extra_edges, seed):
    """
    Generates a sparse directed network.

    A guaranteed chain from source to sink is added first.
    Additional directed edges are then added.

    No adjacency-list graph is stored globally, which keeps
    memory usage reasonable for the 50,000 vertex case.
    """

    random.seed(seed)

    edges = []

    # Guaranteed source-to-sink path.
    for u in range(vertices - 1):
        capacity = random.randint(5, 50)
        edges.append((u, u + 1, capacity))

    # Extra sparse edges.
    for _ in range(extra_edges):
        u = random.randrange(vertices - 1)
        v = random.randrange(u + 1, vertices)

        capacity = random.randint(1, 100)

        edges.append((u, v, capacity))

    return edges


def make_layered_graph():
    """
    Small layered network.

    Useful for testing several simultaneous augmenting paths.
    """

    edges = [
        (0, 1, 10),
        (0, 2, 15),
        (0, 3, 20),

        (1, 4, 8),
        (1, 5, 5),

        (2, 4, 10),
        (2, 5, 10),
        (2, 6, 5),

        (3, 5, 10),
        (3, 6, 10),

        (4, 7, 10),
        (5, 7, 12),
        (5, 8, 8),
        (6, 8, 10),

        (7, 9, 15),
        (8, 9, 15),
    ]

    return edges


def make_large_sparse_graph(vertices, seed):
    """
    Required-size sparse graph.

    Approximately 3V edges.

    The graph is constructed so that source 0 can reach
    sink V-1 through the chain.
    """

    random.seed(seed)

    edges = []

    # V-1 guaranteed chain edges.
    for u in range(vertices - 1):
        edges.append(
            (u, u + 1, random.randint(5, 50))
        )

    # Approximately 2V additional edges.
    extra = 2 * vertices

    for _ in range(extra):
        u = random.randrange(vertices - 1)
        v = random.randrange(u + 1, vertices)

        capacity = random.randint(1, 100)

        edges.append((u, v, capacity))

    return edges


def generate_required_tests():
    """
    Required Assignment 3 sizes:

        10
        100
        1000
        10000
        50000
    """

    sizes = [
        (10, 3001),
        (100, 3002),
        (1000, 3003),
        (10000, 3004),
        (50000, 3005),
    ]

    for vertices, seed in sizes:
        edges = make_large_sparse_graph(
            vertices,
            seed
        )

        filename = f"maxflow_{vertices}.txt"

        write_graph(
            filename,
            vertices,
            edges,
            0,
            vertices - 1
        )

        print(
            f"Generated {filename}: "
            f"V={vertices}, "
            f"E={len(edges)}, "
            f"SOURCE=0, "
            f"SINK={vertices - 1}"
        )


def generate_edge_cases():
    """
    Generate small deterministic edge-case graphs.
    """

    # Assignment example.
    edges = make_example_graph()

    write_graph(
        "maxflow_example.txt",
        6,
        edges,
        0,
        5
    )

    print("Generated maxflow_example.txt")


    # Single edge.
    edges = [
        (0, 1, 25)
    ]

    write_graph(
        "maxflow_single_edge.txt",
        2,
        edges,
        0,
        1
    )

    print("Generated maxflow_single_edge.txt")


    # Simple chain.
    edges = make_chain(10, 10)

    write_graph(
        "maxflow_chain_10.txt",
        10,
        edges,
        0,
        9
    )

    print("Generated maxflow_chain_10.txt")


    # Two paths.
    edges = make_two_path_graph()

    write_graph(
        "maxflow_two_paths.txt",
        6,
        edges,
        0,
        5
    )

    print("Generated maxflow_two_paths.txt")


    # Bottleneck.
    edges = make_bottleneck_graph()

    write_graph(
        "maxflow_bottleneck.txt",
        6,
        edges,
        0,
        5
    )

    print("Generated maxflow_bottleneck.txt")


    # Direct source-sink edge.
    edges = make_direct_edge_graph()

    write_graph(
        "maxflow_direct_edge.txt",
        4,
        edges,
        0,
        3
    )

    print("Generated maxflow_direct_edge.txt")


    # Cycles.
    edges = make_cycle_graph()

    write_graph(
        "maxflow_cycles.txt",
        6,
        edges,
        0,
        5
    )

    print("Generated maxflow_cycles.txt")


    # Parallel edges.
    edges = make_parallel_edge_graph()

    write_graph(
        "maxflow_parallel_edges.txt",
        4,
        edges,
        0,
        3
    )

    print("Generated maxflow_parallel_edges.txt")


    # Equal-capacity paths.
    edges = make_equal_paths_graph()

    write_graph(
        "maxflow_equal_paths.txt",
        6,
        edges,
        0,
        5
    )

    print("Generated maxflow_equal_paths.txt")


    # Disconnected portions but valid s-t path.
    edges = make_disconnected_graph()

    write_graph(
        "maxflow_disconnected_parts.txt",
        9,
        edges,
        0,
        5
    )

    print("Generated maxflow_disconnected_parts.txt")


    # Layered network.
    edges = make_layered_graph()

    write_graph(
        "maxflow_layered.txt",
        10,
        edges,
        0,
        9
    )

    print("Generated maxflow_layered.txt")


def generate_invalid_tests():
    """
    These are NOT required valid assignment test cases.

    They are specifically for checking driver validation.
    """

    # Source == sink.
    edges = [
        (0, 1, 10),
        (1, 2, 10)
    ]

    write_graph(
        "invalid_source_equals_sink.txt",
        3,
        edges,
        0,
        0
    )

    print("Generated invalid_source_equals_sink.txt")


    # Invalid source vertex.
    edges = [
        (0, 1, 10),
        (1, 2, 10)
    ]

    output = OUTPUT_DIR / "invalid_source_vertex.txt"

    with output.open("w") as file:
        file.write("3 2\n")
        file.write("0 1 1 10\n")
        file.write("1 1 2 10\n")
        file.write("2 0\n")
        file.write("SOURCE 10\n")
        file.write("SINK 2\n")

    print("Generated invalid_source_vertex.txt")


    # Invalid sink vertex.
    output = OUTPUT_DIR / "invalid_sink_vertex.txt"

    with output.open("w") as file:
        file.write("3 2\n")
        file.write("0 1 1 10\n")
        file.write("1 1 2 10\n")
        file.write("2 0\n")
        file.write("SOURCE 0\n")
        file.write("SINK 10\n")

    print("Generated invalid_sink_vertex.txt")


    # Negative capacity.
    output = OUTPUT_DIR / "invalid_negative_capacity.txt"

    with output.open("w") as file:
        file.write("3 2\n")
        file.write("0 1 1 -10\n")
        file.write("1 1 2 10\n")
        file.write("2 0\n")
        file.write("SOURCE 0\n")
        file.write("SINK 2\n")

    print("Generated invalid_negative_capacity.txt")


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    generate_required_tests()
    generate_edge_cases()
    generate_invalid_tests()

    print("\nAll Maxflow-Mincut test files generated.")


if __name__ == "__main__":
    main()
