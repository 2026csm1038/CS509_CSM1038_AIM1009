# CS509 Assignment 01 — Buddy

## Objective

This assignment implements graph algorithms using the Compressed Sparse Row (CSR) representation:

* Breadth First Search (BFS)
* Depth First Search (DFS)
* Single Source Shortest Path (SSSP) using Dijkstra's algorithm
* CSR graph construction

---

## Algorithms

### Breadth First Search

BFS uses a queue-based traversal to visit vertices level by level. It computes the traversal order and the shortest distance in number of edges from the selected source vertex.

**Complexity:** `O(V + E)`

---

### Depth First Search

DFS uses an iterative stack-based traversal to visit every reachable vertex.

**Complexity:** `O(V + E)`

---

### Single Source Shortest Path

SSSP is implemented using Dijkstra's algorithm with a priority queue (min-heap). It computes the shortest weighted distance from the selected source vertex to every reachable vertex.

**Complexity:** `O((V + E) log V)`

---

### CSR Graph

The adjacency-list representation is converted into Compressed Sparse Row (CSR) format using:

* `row_ptr`
* `col_ind`
* `values`

CSR conversion is performed before algorithm timing begins.

**Complexity:** `O(V + E)`

---

# Input Format

## BFS / DFS

```text
V E
vertex number_of_neighbors neighbor1 neighbor2 ...
...
SOURCE source_vertex
```

Example:

```text
4 3
0 1 1
1 2 0 2
2 2 1 3
3 1 2
SOURCE 0
```

## SSSP

```text
V E
vertex number_of_neighbors neighbor1 weight1 neighbor2 weight2 ...
...
SOURCE source_vertex
```

---

# Test Cases

A unified Python test generator is provided:

```text
assignment_01/tests/generate_tests.py
```

The generated tests include:

* 10 vertices
* 100 vertices
* 10,000 vertices
* 50,000 vertices
* 100,000 vertices
* Single vertex
* Disconnected graph
* Linear chain
* Dense graph
* Cycle graph
* Star graph
* Equal-weight graph for SSSP

---

# Compilation

Run the following commands from the repository root.

### BFS

```bash
g++ -O2 -std=c++17 \
assignment_01/driver/bfs_driver.cpp \
assignment_01/src/bfs.cpp \
assignment_01/src/csr.cpp \
-o bfs_driver
```

### DFS

```bash
g++ -O2 -std=c++17 \
assignment_01/driver/dfs_driver.cpp \
assignment_01/src/dfs.cpp \
assignment_01/src/csr.cpp \
-o dfs_driver
```

### SSSP

```bash
g++ -O2 -std=c++17 \
assignment_01/driver/sssp_driver.cpp \
assignment_01/src/sssp.cpp \
assignment_01/src/csr.cpp \
-o sssp_driver
```

---

# Execution

### BFS

```bash
./bfs_driver assignment_01/tests/bfs_100.txt
```

### DFS

```bash
./dfs_driver assignment_01/tests/dfs_100.txt
```

### SSSP

```bash
./sssp_driver assignment_01/tests/sssp_100.txt
```

---

# Common Wrapper

Compile:

```bash
g++ -O2 -std=c++17 common_wrapper/wrapper.cpp -o wrapper
```

Run:

```bash
./wrapper
```

Select:

```text
1. BFS
2. DFS
3. SSSP
4. Betweenness Centrality
5. Connected Components
6. Triangle Counting
7. Exit
```

For Assignment 01, select options **1–3**.

Example:

```text
Choice: 1
Enter input file: assignment_01/tests/bfs_100.txt
```

The selected driver executes and prints its result and execution time.

---

# Execution Results

| Algorithm | Test File               | Time (ms) |
| --------- | ----------------------- | --------: |
| BFS       | `bfs_100000.txt`        |   14.1892 |
| BFS       | `bfs_10000.txt`         |   1.03655 |
| BFS       | `bfs_100.txt`           |  0.010579 |
| BFS       | `bfs_10.txt`            |       N/A |
| BFS       | `bfs_50000.txt`         |    9.2073 |
| BFS       | `bfs_cycle.txt`         |  0.004654 |
| BFS       | `bfs_dense.txt`         |  0.001913 |
| BFS       | `bfs_disconnected.txt`  |  0.002577 |
| BFS       | `bfs_linear_chain.txt`  |  0.003051 |
| BFS       | `bfs_single_vertex.txt` |  0.000827 |
| BFS       | `bfs_star.txt`          |  0.002716 |
| DFS       | `dfs_100000.txt`        |   15.6132 |
| DFS       | `dfs_10000.txt`         |  0.917571 |
| DFS       | `dfs_100.txt`           |  0.009343 |
| DFS       | `dfs_10.txt`            |  0.001407 |
| DFS       | `dfs_50000.txt`         |    5.9000 |
| DFS       | `dfs_cycle.txt`         |  0.002983 |
| DFS       | `dfs_dense.txt`         |  0.002678 |
| DFS       | `dfs_disconnected.txt`  |  0.002531 |
| DFS       | `dfs_linear_chain.txt`  |  0.001718 |
| DFS       | `dfs_single_vertex.txt` |  0.000847 |
| DFS       | `dfs_star.txt`          |  0.001428 |
| SSSP      | `sssp_100000.txt`       |   82.6064 |
| SSSP      | `sssp_10000.txt`        |   5.00568 |
| SSSP      | `sssp_100.txt`          |  0.021723 |
| SSSP      | `sssp_10.txt`           |  0.002959 |
| SSSP      | `sssp_50000.txt`        |   33.2991 |
| SSSP      | `sssp_cycle.txt`        |  0.002131 |

---

# Complexity

| Algorithm      | Time               | Space      |
| -------------- | ------------------ | ---------- |
| BFS            | `O(V + E)`         | `O(V)`     |
| DFS            | `O(V + E)`         | `O(V)`     |
| Dijkstra       | `O((V + E) log V)` | `O(V)`     |
| CSR Conversion | `O(V + E)`         | `O(V + E)` |

---

# References

1. Breadth First Search — https://en.wikipedia.org/wiki/Breadth-first_search
2. Depth First Search — https://en.wikipedia.org/wiki/Depth-first_search
3. Dijkstra's Algorithm — https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
4. Compressed Sparse Row — https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)

