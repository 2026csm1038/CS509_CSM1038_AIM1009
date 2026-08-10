# CS509 Laboratory Repository

## Repository Overview

This repository contains the submission for **CS509 Assignment 1 (buddy) **. The assignment implements graph algorithms using the Compressed Sparse Row (CSR) representation along with a common wrapper to execute all implementations from a single interface.

---

# Student Details

**Name 1 :** Vanshika Aggarwal

**Entry Number:** CSM1038

**Name 2 :** Kanak

**Entry Number:** AI1009

**Git Repository:** https://github.com/2026csm1038/CS509_CSM1038_AIM1009

---

# Language and Environment

* **Language:** C++
* **Compiler:** g++ (GCC)
* **Compilation Flags:** `-O2 -std=c++17`
* **Operating System:** Ubuntu (VirtualBox)

---

# Directory Structure

```text
CS509_CSM1038_AIM1009/
│
├── README.md
├── common_wrapper/
│   └── wrapper.cpp
│
└── assignment_01/
    ├── src/
    │   ├── bfs.cpp
    │   ├── bfs.h
    │   ├── dfs.cpp
    │   ├── dfs.h
    │   ├── sssp.cpp
    │   ├── sssp.h
    │   ├── csr.cpp
    │   └── csr.h
    │
    ├── driver/
    │   ├── bfs_driver.cpp
    │   ├── dfs_driver.cpp
    │   └── sssp_driver.cpp
    │
    └── tests/
        ├── generate_tests.py
        ├── bfs_*.txt
        ├── dfs_*.txt
        └── sssp_*.txt
```

---

# Assignment 01

## Objective

Implement the following graph algorithms using the CSR graph representation.

* Breadth First Search (BFS)
* Depth First Search (DFS)
* Single Source Shortest Path (Dijkstra)
* CSR Graph Construction

---

# Algorithms Implemented

### Breadth First Search (BFS)

* Queue-based graph traversal.
* Computes traversal order and shortest distance (in number of edges) from the source vertex.

### Depth First Search (DFS)

* Stack-based iterative traversal.
* Visits every reachable vertex exactly once.

### Single Source Shortest Path (SSSP)

* Implemented using Dijkstra's Algorithm.
* Uses a priority queue (min-heap).
* Computes shortest weighted distance from the source vertex.

### CSR Graph

Converts an adjacency list into the CSR representation using:

* `row_ptr`
* `col_ind`
* `values`

---

# Input Format

## BFS / DFS

```text
V E
vertex number_of_neighbors neighbor1 neighbor2 ...
...
SOURCE source_vertex
```

## SSSP

```text
V E
vertex number_of_neighbors neighbor1 weight1 neighbor2 weight2 ...
...
SOURCE source_vertex
```

---

# Test Case Generation

The repository contains a unified Python script:

```text
generate_tests.py
```

It generates:

* Standard graphs (10, 100, 10000, 50000 and 100000 vertices)
* Single vertex graph
* Disconnected graph
* Linear chain
* Dense graph
* Cycle graph
* Star graph
* Equal-weight graph (SSSP)

---

# Compilation

### BFS

```bash
g++ -O2 -std=c++17 assignment_01/driver/bfs_driver.cpp assignment_01/src/bfs.cpp assignment_01/src/csr.cpp -o bfs_driver
```

### DFS

```bash
g++ -O2 -std=c++17 assignment_01/driver/dfs_driver.cpp assignment_01/src/dfs.cpp assignment_01/src/csr.cpp -o dfs_driver
```

### SSSP

```bash
g++ -O2 -std=c++17 assignment_01/driver/sssp_driver.cpp assignment_01/src/sssp.cpp assignment_01/src/csr.cpp -o sssp_driver
```

### Common Wrapper

```bash
g++ -O2 -std=c++17 common_wrapper/wrapper.cpp -o wrapper
```

---

# Execution

### Run Individual Drivers

```bash
./bfs_driver assignment_01/tests/bfs_100.txt

./dfs_driver assignment_01/tests/dfs_100.txt

./sssp_driver assignment_01/tests/sssp_100.txt
```

### Run Using Common Wrapper

```bash
./wrapper
```

The wrapper displays the following menu:

```text
1. BFS
2. DFS
3. SSSP
4. Exit
```

Choose the required algorithm by entering its corresponding number.

For example:

* Enter **1** for BFS
* Enter **2** for DFS
* Enter **3** for SSSP

The wrapper then prompts:

```text
Enter input file:
```

Provide the complete path to the required test file.

Examples:

For BFS

```text
assignment_01/tests/bfs_100.txt
```

For DFS

```text
assignment_01/tests/dfs_100.txt
```

For SSSP

```text
assignment_01/tests/sssp_100.txt
```

The selected driver executes and prints the traversal/shortest path along with the execution time.

---

# Execution Results

| Algorithm | Test File             | Time (ms) |
| --------- | --------------------- | --------: |
| BFS       | bfs_100000.txt        |   14.1892 |
| BFS       | bfs_10000.txt         |   1.03655 |
| BFS       | bfs_100.txt           |  0.010579 |
| BFS       | bfs_10.txt            |       N/A |
| BFS       | bfs_50000.txt         |    9.2073 |
| BFS       | bfs_cycle.txt         |  0.004654 |
| BFS       | bfs_dense.txt         |  0.001913 |
| BFS       | bfs_disconnected.txt  |  0.002577 |
| BFS       | bfs_linear_chain.txt  |  0.003051 |
| BFS       | bfs_single_vertex.txt |  0.000827 |
| BFS       | bfs_star.txt          |  0.002716 |
| DFS       | dfs_100000.txt        |   15.6132 |
| DFS       | dfs_10000.txt         |  0.917571 |
| DFS       | dfs_100.txt           |  0.009343 |
| DFS       | dfs_10.txt            |  0.001407 |
| DFS       | dfs_50000.txt         |    5.9000 |
| DFS       | dfs_cycle.txt         |  0.002983 |
| DFS       | dfs_dense.txt         |  0.002678 |
| DFS       | dfs_disconnected.txt  |  0.002531 |
| DFS       | dfs_linear_chain.txt  |  0.001718 |
| DFS       | dfs_single_vertex.txt |  0.000847 |
| DFS       | dfs_star.txt          |  0.001428 |
| SSSP      | sssp_100000.txt       |   82.6064 |
| SSSP      | sssp_10000.txt        |   5.00568 |
| SSSP      | sssp_100.txt          |  0.021723 |
| SSSP      | sssp_10.txt           |  0.002959 |
| SSSP      | sssp_50000.txt        |   33.2991 |
| SSSP      | sssp_cycle.txt        |  0.002131 |

---

# Complexity Analysis

| Algorithm        | Time Complexity  | Space Complexity |
| ---------------- | ---------------- | ---------------- |
| BFS              | O(V + E)         | O(V)             |
| DFS              | O(V + E)         | O(V)             |
| Dijkstra (SSSP)  | O((V + E) log V) | O(V)             |
| CSR Construction | O(V + E)         | O(V + E)         |

---

# References

1. https://en.wikipedia.org/wiki/Breadth-first_search
2. https://en.wikipedia.org/wiki/Depth-first_search
3. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
4. https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)

