# CS509 Laboratory Repository

## Repository Overview

This repository contains the buddy submissions for **CS509 (First-Year M.Tech CSE, 2026)**. Each assignment is organized in a separate directory with its corresponding source files, drivers, test cases, and a common wrapper for executing the implemented algorithms.

---

# Student Details

**Name 1:** Vanshika Aggarwal

**Entry Number:** CSM1038

**Name 2:** Kanak

**Entry Number:** AI1009

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
    │   ├── bfs.h
    │   ├── bfs.cpp
    │   ├── dfs.h
    │   ├── dfs.cpp
    │   ├── sssp.h
    │   ├── sssp.cpp
    │   ├── csr.h
    │   └── csr.cpp
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

# Common Wrapper

The repository includes a common wrapper (`common_wrapper/wrapper.cpp`) that provides a menu-driven interface for executing the implemented graph algorithms.

### Available Options

1. Breadth First Search (BFS)
2. Depth First Search (DFS)
3. Single Source Shortest Path (Dijkstra)
4. Exit

The wrapper prompts the user for the required input file and invokes the corresponding driver executable.

---

## Build Wrapper

```bash
g++ -O2 -std=c++17 common_wrapper/wrapper.cpp -o wrapper
```

---

## Run Wrapper

```bash
./wrapper
```

---

# Assignment 01

## Objective

Implement graph algorithms using the Compressed Sparse Row (CSR) graph representation.

The assignment includes:

* Breadth First Search (BFS)
* Depth First Search (DFS)
* Single Source Shortest Path (Dijkstra's Algorithm)
* CSR Graph Conversion

---

# Algorithms Implemented

## Breadth First Search (BFS)

* Uses a queue for traversal.
* Computes BFS traversal order.
* Computes shortest distance (number of edges) from the source vertex to every reachable vertex.
* Unreachable vertices are assigned a distance of **-1**.

---

## Depth First Search (DFS)

* Uses an iterative implementation with an explicit stack.
* Produces DFS traversal order.
* Visits each reachable vertex exactly once.

---

## Single Source Shortest Path (SSSP)

* Implemented using Dijkstra's Algorithm.
* Uses a priority queue (min-heap).
* Computes shortest weighted distances from the source vertex.
* Supports positive edge weights.

---

## CSR Graph Conversion

The adjacency list representation is converted into Compressed Sparse Row (CSR) format.

The CSR representation consists of:

* `values`
* `col_ind`
* `row_ptr`

This representation enables efficient traversal while reducing memory overhead for sparse graphs.

---

# Input Format

## BFS / DFS

```
V E
vertex number_of_neighbors neighbor1 neighbor2 ...
...
SOURCE source_vertex
```

---

## SSSP

```
V E
vertex number_of_neighbors neighbor1 weight1 neighbor2 weight2 ...
...
SOURCE source_vertex
```

---

# Test Case Generation

A unified Python script is provided for generating test cases.

```
generate_tests.py
```

The generator creates:

### Standard Test Cases

* 10 vertices
* 100 vertices
* 10,000 vertices
* 50,000 vertices
* 100,000 vertices

### Edge Cases

* Single vertex
* Disconnected graph
* Linear chain
* Dense graph
* Cycle graph
* Star graph
* Equal-weight graph (SSSP)

Separate test files are generated for:

* BFS
* DFS
* SSSP

---

# File Structure

| File              | Purpose                                               |
| ----------------- | ----------------------------------------------------- |
| bfs.cpp / bfs.h   | Breadth First Search implementation                   |
| dfs.cpp / dfs.h   | Depth First Search implementation                     |
| sssp.cpp / sssp.h | Dijkstra's Single Source Shortest Path implementation |
| csr.cpp / csr.h   | CSR graph construction                                |
| bfs_driver.cpp    | Driver program for BFS                                |
| dfs_driver.cpp    | Driver program for DFS                                |
| sssp_driver.cpp   | Driver program for SSSP                               |
| generate_tests.py | Generates all standard and edge-case test files       |
| wrapper.cpp       | Menu-driven launcher for all algorithms               |

---

# Compilation

## BFS

```bash
g++ -O2 -std=c++17 assignment_01/driver/bfs_driver.cpp assignment_01/src/bfs.cpp assignment_01/src/csr.cpp -o bfs_driver
```

## DFS

```bash
g++ -O2 -std=c++17 assignment_01/driver/dfs_driver.cpp assignment_01/src/dfs.cpp assignment_01/src/csr.cpp -o dfs_driver
```

## SSSP

```bash
g++ -O2 -std=c++17 assignment_01/driver/sssp_driver.cpp assignment_01/src/sssp.cpp assignment_01/src/csr.cpp -o sssp_driver
```

---

# Execution

Run the drivers directly.

## BFS

```bash
./bfs_driver assignment_01/tests/bfs_10.txt
```

## DFS

```bash
./dfs_driver assignment_01/tests/dfs_10.txt
```

## SSSP

```bash
./sssp_driver assignment_01/tests/sssp_10.txt
```

Alternatively, execute the wrapper:

```bash
./wrapper
```

and select the desired algorithm from the menu.

---

# Complexity Analysis

| Algorithm                 | Time Complexity  | Space Complexity |
| ------------------------- | ---------------- | ---------------- |
| BFS                       | O(V + E)         | O(V)             |
| DFS                       | O(V + E)         | O(V)             |
| Dijkstra (Priority Queue) | O((V + E) log V) | O(V)             |
| CSR Conversion            | O(V + E)         | O(V + E)         |

---

# References

1. https://en.wikipedia.org/wiki/Breadth-first_search
2. https://en.wikipedia.org/wiki/Depth-first_search
3. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
4. https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)

