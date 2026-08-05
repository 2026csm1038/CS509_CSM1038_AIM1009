import random
import os

OUT_DIR = "."


# ---------------------------------------------------------
# Connected graph builder
# ---------------------------------------------------------
def build_connected_graph(V, avg_degree, weighted, seed=42):
    random.seed(seed)

    adj = [[] for _ in range(V)]
    edges = set()

    def add_edge(u, v):
        if weighted:
            w = random.randint(1, 20)
            adj[u].append((v, w))
            adj[v].append((u, w))
        else:
            adj[u].append(v)
            adj[v].append(u)
        edges.add((min(u, v), max(u, v)))

    # ensure connectivity
    for i in range(1, V):
        j = random.randint(0, i - 1)
        add_edge(i, j)

    target_edges = (V * avg_degree) // 2

    attempts = 0
    while len(edges) < target_edges and attempts < target_edges * 10:
        attempts += 1
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)

        if u == v:
            continue

        key = (min(u, v), max(u, v))

        if key in edges:
            continue

        add_edge(u, v)

    return adj, len(edges)


# ---------------------------------------------------------
# Writers
# ---------------------------------------------------------
def write_sssp(V, degree, filename, source=0, seed=42):
    adj, E = build_connected_graph(V, degree, True, seed)

    with open(os.path.join(OUT_DIR, filename), "w") as f:
        f.write(f"{V} {E}\n")

        for u in range(V):
            line = f"{u} {len(adj[u])}"
            for v, w in adj[u]:
                line += f" {v} {w}"
            f.write(line + "\n")

        f.write(f"SOURCE {source}\n")

    print(filename)


def write_unweighted(V, degree, filename, source=0, seed=42):
    adj, E = build_connected_graph(V, degree, False, seed)

    with open(os.path.join(OUT_DIR, filename), "w") as f:
        f.write(f"{V} {E}\n")

        for u in range(V):
            line = f"{u} {len(adj[u])}"
            for v in adj[u]:
                line += f" {v}"
            f.write(line + "\n")

        f.write(f"SOURCE {source}\n")

    print(filename)


# ---------------------------------------------------------
# Helper for edge cases
# ---------------------------------------------------------
def write_pair(V, E, weighted_adj, unweighted_adj, name, source):

    with open(os.path.join(OUT_DIR, f"sssp_{name}.txt"), "w") as f:
        f.write(f"{V} {E}\n")
        for u in range(V):
            line = f"{u} {len(weighted_adj[u])}"
            for v, w in weighted_adj[u]:
                line += f" {v} {w}"
            f.write(line + "\n")
        f.write(f"SOURCE {source}\n")

    for algo in ("bfs", "dfs"):
        with open(os.path.join(OUT_DIR, f"{algo}_{name}.txt"), "w") as f:
            f.write(f"{V} {E}\n")
            for u in range(V):
                line = f"{u} {len(unweighted_adj[u])}"
                for v in unweighted_adj[u]:
                    line += f" {v}"
                f.write(line + "\n")
            f.write(f"SOURCE {source}\n")


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------
def disconnected():
    V = 10

    w_adj = [[] for _ in range(V)]
    u_adj = [[] for _ in range(V)]

    edges = 0

    def add(u, v):
        nonlocal edges
        w = random.randint(1, 10)

        w_adj[u].append((v, w))
        w_adj[v].append((u, w))

        u_adj[u].append(v)
        u_adj[v].append(u)

        edges += 1

    for i in range(4):
        add(i, i + 1)

    for i in range(5, 9):
        add(i, i + 1)

    write_pair(V, edges, w_adj, u_adj, "disconnected", 0)


def single_vertex():
    write_pair(1, 0, [[]], [[]], "single_vertex", 0)


def linear_chain(V=20):
    w_adj = [[] for _ in range(V)]
    u_adj = [[] for _ in range(V)]

    edges = 0

    for i in range(V - 1):
        w = random.randint(1, 5)

        w_adj[i].append((i + 1, w))
        w_adj[i + 1].append((i, w))

        u_adj[i].append(i + 1)
        u_adj[i + 1].append(i)

        edges += 1

    write_pair(V, edges, w_adj, u_adj, "linear_chain", 0)


def dense(V=15):
    w_adj = [[] for _ in range(V)]
    u_adj = [[] for _ in range(V)]

    edges = 0

    for i in range(V):
        for j in range(i + 1, V):
            w = random.randint(1, 15)

            w_adj[i].append((j, w))
            w_adj[j].append((i, w))

            u_adj[i].append(j)
            u_adj[j].append(i)

            edges += 1

    write_pair(V, edges, w_adj, u_adj, "dense", 0)


def cycle(V=10):
    w_adj = [[] for _ in range(V)]
    u_adj = [[] for _ in range(V)]

    edges = 0

    for i in range(V):
        j = (i + 1) % V
        w = random.randint(1, 10)

        w_adj[i].append((j, w))
        w_adj[j].append((i, w))

        u_adj[i].append(j)
        u_adj[j].append(i)

        edges += 1

    write_pair(V, edges, w_adj, u_adj, "cycle", 0)


def star(V=12):
    w_adj = [[] for _ in range(V)]
    u_adj = [[] for _ in range(V)]

    hub = 0
    edges = 0

    for i in range(1, V):
        w = random.randint(1, 10)

        w_adj[hub].append((i, w))
        w_adj[i].append((hub, w))

        u_adj[hub].append(i)
        u_adj[i].append(hub)

        edges += 1

    write_pair(V, edges, w_adj, u_adj, "star", hub)


def equal_weights():
    V = 6

    adj = [[] for _ in range(V)]

    edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (2, 4),
        (3, 5),
        (4, 5),
    ]

    for u, v in edges:
        adj[u].append((v, 5))
        adj[v].append((u, 5))

    with open(os.path.join(OUT_DIR, "sssp_equal_weights.txt"), "w") as f:
        f.write(f"{V} {len(edges)}\n")

        for u in range(V):
            line = f"{u} {len(adj[u])}"
            for v, w in adj[u]:
                line += f" {v} {w}"
            f.write(line + "\n")

        f.write("SOURCE 0\n")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
if __name__ == "__main__":

    random.seed(7)

    sizes = [
        (10, 3),
        (100, 4),
        (10000, 4),
        (50000, 4),
        (100000, 4),
    ]

    for V, d in sizes:
        write_sssp(V, d, f"sssp_{V}.txt")
        write_unweighted(V, d, f"bfs_{V}.txt")
        write_unweighted(V, d, f"dfs_{V}.txt")

    disconnected()
    single_vertex()
    linear_chain()
    dense()
    cycle()
    star()
    equal_weights()

    print("\nAll test cases generated successfully.")
