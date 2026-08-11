# Assignment 02

## Objective

The buddy assignment contains the following graph algorithms:

1. **Betweenness Centrality**
2. **Connected Components**
3. **Triangle Counting**

The implementations use the CSR graph representation from the repository.

---

# Directory Structure

```text
CS509_CSM1038_AIM1009/
│
├── common_wrapper/
│   └── wrapper.cpp
│
└── assignment_02/
    ├── src/
    │   ├── betweenness_centrality.cpp
    │   ├── betweenness_centrality.h
    │   ├── connected_components.cpp
    │   ├── connected_components.h
    │   ├── triangle_counting.cpp
    │   └── triangle_counting.h
    │
    ├── driver/
    │   ├── betweenness_centrality_driver.cpp
    │   ├── connected_components_driver.cpp
    │   └── triangle_counting_driver.cpp
    │
    └── tests/
        ├── bc_*.txt
        ├── cc_*.txt
        └── triangle_*.txt
```

---

# Betweenness Centrality

Betweenness Centrality measures the importance of a vertex based on how frequently it lies on shortest paths between pairs of vertices.

The implementation computes the centrality values for the vertices of the graph.

### Compilation

```bash
g++ -O2 -std=c++17 \
-Iassignment_01/src \
assignment_01/src/csr.cpp \
assignment_02/src/betweenness_centrality.cpp \
assignment_02/driver/bc_driver.cpp \
-o betweenness_centrality_driver
```

### Execution

```bash
./bc_driver assignment_02/tests/betweenness_centrality/bc_100.txt
```

---

# Connected Components

Connected Components identifies the separate connected portions of an undirected graph.

The implementation traverses the graph and assigns each vertex to its corresponding connected component.

### Compilation

```bash
g++ -O2 -std=c++17 \
-Iassignment_01/src \
assignment_01/src/bfs.cpp \
assignment_01/src/csr.cpp \
assignment_02/src/connected_components.cpp \
assignment_02/driver/connected_components_driver.cpp \
-o connected_components_driver
```

### Execution

```bash
./connected_components_driver assignment_02/tests/connected_components/cc_100.txt
```

---

# Triangle Counting

Triangle Counting determines the number of triangles present in the graph.

The implementation:

* Converts the adjacency-list representation into CSR.
* Sorts CSR neighbour lists.
* Checks whether pairs of neighbouring vertices are connected.
* Counts each triangle without double-counting it.

For small graphs, the implementation can also collect and display the triangles found.

### Compilation

```bash
g++ -O2 -std=c++17 \
-Iassignment_01/src \
assignment_01/src/csr.cpp \
assignment_02/src/triangle_counting.cpp \
assignment_02/driver/triangle_counting_driver.cpp \
-o triangle_counting_driver
```

### Execution

```bash
./triangle_counting_driver assignment_02/tests/triangle_counting/tc_100.txt
```

---

# Common Wrapper

The common wrapper provides a menu-driven interface for running the graph algorithms.

Build it using:

```bash
g++ -O2 -std=c++17 common_wrapper/wrapper.cpp -o wrapper
```

Run:

```bash
./wrapper
```

The wrapper provides:

```text
========== Common Wrapper ==========
1. BFS
2. DFS
3. SSSP
4. Betweenness Centrality
5. Connected Components
6. Triangle Counting
7. Exit
Choice:
```

After selecting an algorithm, the wrapper asks:

```text
Enter input file:
```

Enter the path of the corresponding test case.

For example:

### Betweenness Centrality

```text
assignment_02/tests/betweenness_centrality/bc_100.txt
```

### Connected Components

```text
assignment_02/tests/connected_components/cc_100.txt
```

### Triangle Counting

```text
assignment_02/tests/triangle_counting/tc_test.txt
```

The selected driver then executes and displays its output and execution time.

---

# Test Cases

The test cases cover both normal and edge-case graph structures.

## Betweenness Centrality

The test set includes:

* Small graphs
* Large graphs
* Paths
* Cycles
* Stars
* Complete graphs
* Bipartite graphs
* Trees
* Grids
* Bridges
* Lollipop graphs
* Graphs containing multiple components
* Duplicate edges
* Self-loops
* Empty/sparse cases
* Random graphs

## Connected Components

The test set includes:

* Small graphs
* Large graphs
* Fully connected graphs
* Fully isolated vertices
* Cycles
* Paths
* Stars
* Empty graphs
* Single vertices
* Two-component graphs
* Mixed connectivity cases

## Triangle Counting

Test cases include graph structures designed to test:

* No triangles
* Single triangle
* Multiple triangles
* Complete graphs
* Sparse graphs
* Cyclic graphs
* Dense graphs
* Edge cases

---

# Execution Results

Execution times were measured with the algorithm execution only; input reading, graph construction, and output are handled separately by the drivers.

## Betweenness Centrality

| Algorithm              | Test File                 | Time (ms) |
| ---------------------- | ------------------------- | --------: |
| Betweenness Centrality | bc_10000.txt              |  58821.64 |
| Betweenness Centrality | bc_1000.txt               |    487.23 |
| Betweenness Centrality | bc_100.txt                |      5.18 |
| Betweenness Centrality | bc_10.txt                 |      0.02 |
| Betweenness Centrality | bc_5000.txt               |  14783.83 |
| Betweenness Centrality | bc_bipartite_3x3.txt      |      0.01 |
| Betweenness Centrality | bc_bipartite_4x4.txt      |      0.03 |
| Betweenness Centrality | bc_bridge.txt             |      0.01 |
| Betweenness Centrality | bc_complete_3.txt         |      0.00 |
| Betweenness Centrality | bc_complete_4.txt         |      0.00 |
| Betweenness Centrality | bc_complete_5.txt         |      0.00 |
| Betweenness Centrality | bc_complete_6.txt         |      0.00 |
| Betweenness Centrality | bc_components.txt         |      0.02 |
| Betweenness Centrality | bc_cycle_1000.txt         |    408.60 |
| Betweenness Centrality | bc_cycle_10.txt           |      0.01 |
| Betweenness Centrality | bc_cycle_3.txt            |      0.00 |
| Betweenness Centrality | bc_cycle_4.txt            |      0.00 |
| Betweenness Centrality | bc_cycle_5.txt            |      0.00 |
| Betweenness Centrality | bc_diamond.txt            |      0.00 |
| Betweenness Centrality | bc_duplicate_edges.txt    |      0.01 |
| Betweenness Centrality | bc_empty_1.txt            |      0.00 |
| Betweenness Centrality | bc_empty_2.txt            |      0.00 |
| Betweenness Centrality | bc_grid_3x3.txt           |      0.03 |
| Betweenness Centrality | bc_grid_4x4.txt           |      0.10 |
| Betweenness Centrality | bc_lollipop.txt           |      0.03 |
| Betweenness Centrality | bc_path_1000.txt          |    398.09 |
| Betweenness Centrality | bc_path_10.txt            |      0.03 |
| Betweenness Centrality | bc_path_3.txt             |      0.01 |
| Betweenness Centrality | bc_path_4.txt             |      0.00 |
| Betweenness Centrality | bc_path_5.txt             |      0.00 |
| Betweenness Centrality | bc_random_medium_1000.txt |   1321.27 |
| Betweenness Centrality | bc_random_small_01.txt    |      0.01 |
| Betweenness Centrality | bc_random_small_02.txt    |      0.02 |
| Betweenness Centrality | bc_random_small_03.txt    |      0.05 |
| Betweenness Centrality | bc_random_small_04.txt    |      0.01 |
| Betweenness Centrality | bc_random_small_05.txt    |      0.01 |
| Betweenness Centrality | bc_random_small_06.txt    |      0.02 |
| Betweenness Centrality | bc_random_small_07.txt    |      0.01 |
| Betweenness Centrality | bc_random_small_08.txt    |      0.03 |
| Betweenness Centrality | bc_random_small_09.txt    |      0.01 |
| Betweenness Centrality | bc_random_small_10.txt    |      0.01 |
| Betweenness Centrality | bc_random_small_11.txt    |      0.02 |
| Betweenness Centrality | bc_random_small_12.txt    |      0.02 |
| Betweenness Centrality | bc_random_small_13.txt    |      0.07 |
| Betweenness Centrality | bc_random_small_14.txt    |      0.09 |
| Betweenness Centrality | bc_random_small_15.txt    |      0.11 |
| Betweenness Centrality | bc_random_sparse_1000.txt |    768.96 |
| Betweenness Centrality | bc_self_loop.txt          |      0.00 |
| Betweenness Centrality | bc_single_edge.txt        |      0.00 |
| Betweenness Centrality | bc_star_1000.txt          |    388.03 |
| Betweenness Centrality | bc_star_10.txt            |      0.01 |
| Betweenness Centrality | bc_star_4.txt             |      0.00 |
| Betweenness Centrality | bc_star_5.txt             |      0.00 |
| Betweenness Centrality | bc_test.txt               |      0.01 |
| Betweenness Centrality | bc_tree_1000.txt          |    398.41 |
| Betweenness Centrality | bc_tree_10.txt            |      0.03 |
| Betweenness Centrality | bc_two_paths.txt          |      0.01 |
| Betweenness Centrality | bc_wheel_10.txt           |      0.01 |

---

## Connected Components

| Algorithm            | Test File                  | Time (ms) |
| -------------------- | -------------------------- | --------: |
| Connected Components | cc_100000.txt              |   22.2306 |
| Connected Components | cc_10000.txt               |   1.80379 |
| Connected Components | cc_100.txt                 |  0.019419 |
| Connected Components | cc_10.txt                  |  0.002352 |
| Connected Components | cc_50000.txt               |   7.01738 |
| Connected Components | cc_edge_all_connected.txt  |  0.002004 |
| Connected Components | cc_edge_all_isolated.txt   |  0.006918 |
| Connected Components | cc_edge_cycle.txt          |  0.005608 |
| Connected Components | cc_edge_empty.txt          |  0.002203 |
| Connected Components | cc_edge_mixed.txt          |  0.002687 |
| Connected Components | cc_edge_one_edge.txt       |  0.004400 |
| Connected Components | cc_edge_path.txt           |  0.011480 |
| Connected Components | cc_edge_single.txt         |  0.002054 |
| Connected Components | cc_edge_star.txt           |  0.027028 |
| Connected Components | cc_edge_two_components.txt |  0.004047 |

---

## Triangle Counting



# Complexity Analysis

| Algorithm              | Time Complexity                                     | Space Complexity |
| ---------------------- | --------------------------------------------------- | ---------------- |
| Betweenness Centrality | O(VE) for unweighted graphs using Brandes' approach | O(V + E)         |
| Connected Components   | O(V + E)                                            | O(V)             |
| Triangle Counting      | O(Σ deg(v)² log V) with binary-search edge checks   | O(V + E)         |
| CSR Construction       | O(V + E)                                            | O(V + E)         |

---

# References

1. https://en.wikipedia.org/wiki/Betweenness_centrality
2. https://en.wikipedia.org/wiki/Connected_component_(graph_theory)
3. https://en.wikipedia.org/wiki/Triangle_(graph)
4. https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)

