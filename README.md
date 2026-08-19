# CS509 Laboratory Repository

## Repository Overview

This repository contains the **Buddy assignments for CS509 (First-Year M.Tech CSE, 2026)**.

The repository contains graph algorithms implemented using C++ and the Compressed Sparse Row (CSR) representation. Each assignment has its own source files, drivers, test cases and documentation. A common wrapper provides a single menu-driven interface for running the implemented graph algorithms.

---

## Student Details

**Name 1:** Vanshika Aggarwal
**Entry Number:** CSM1038

**Name 2:** Kanak
**Entry Number:** AIM1009

**Git Repository:**
https://github.com/2026csm1038/CS509_CSM1038_AIM1009

---

## Language and Environment

* **Language:** C++
* **Compiler:** g++ (GCC)
* **Compiler Version:** Ubuntu 15.2.0-16ubuntu1
* **Compilation Flags:** `-O2 -std=c++17`
* **Operating System:** Ubuntu running in VirtualBox

---

## Repository Structure

```text
CS509_CSM1038_AIM1009/
│
├── README.md
│
├── common_wrapper/
│   └── wrapper.cpp
│
├── assignment_01/
│   ├── README.md
│   ├── src/
│   │   ├── bfs.cpp
│   │   ├── bfs.h
│   │   ├── dfs.cpp
│   │   ├── dfs.h
│   │   ├── sssp.cpp
│   │   ├── sssp.h
│   │   ├── csr.cpp
│   │   └── csr.h
│   │
│   ├── driver/
│   │   ├── bfs_driver.cpp
│   │   ├── dfs_driver.cpp
│   │   └── sssp_driver.cpp
│   │
│   └── tests/
│       ├── generate_tests.py
│       ├── bfs_*.txt
│       ├── dfs_*.txt
│       └── sssp_*.txt
│
├── assignment_02/
│   ├── README.md
│   ├── src/
│   │   ├── betweenness_centrality.cpp
│   │   ├── betweenness_centrality.h
│   │   ├── connected_components.cpp
│   │   ├── connected_components.h
│   │   ├── triangle_counting.cpp
│   │   └── triangle_counting.h
│   │
│   ├── driver/
│   │   ├── bc_driver.cpp
│   │   ├── connected_components_driver.cpp
│   │   └── triangle_counting_driver.cpp
│   │
│   └── tests/
│       ├── betweenness_centrality/
│       ├── connected_components/
│       └── triangle_counting/
│
└── assignment_03/
    ├── README.md
    ├── src/
    │   ├── gradient_descent.cpp
    │   ├── gradient_descent.h
    │   ├── maxflow_mincut.cpp
    │   └── maxflow_mincut.h
    │
    ├── driver/
    │   ├── gd_driver.cpp
    │   └── maxmin_driver.cpp
    │
    └── tests/
        ├── gradient_descent/
        └── maxflow_mincut/
```

Compiled driver binaries are generated locally and are not stored in the Git repository.

---

### Common Wrapper

The common wrapper provides a menu-driven way to launch assignment drivers.

The repository provides a Makefile to compile the common wrapper and the assignment drivers.

```text
make clean 
make 
./wrapper
```

# Assignments

## Assignment 01 — Buddy

Assignment 01 implements:

* Breadth First Search (BFS)
* Depth First Search (DFS)
* Single Source Shortest Path using Dijkstra's algorithm
* CSR graph construction

Detailed implementation, compilation, execution and test results are documented in:

```text
assignment_01/README.md
```

---

## Assignment 02 — Buddy

Assignment 02 implements:

* Triangle Counting
* Betweenness Centrality
* Connected Components

The three algorithms operate on undirected graphs represented using adjacency lists and converted to CSR before algorithm execution.

Detailed implementation, compilation, execution and test results are documented in:

```text
assignment_02/README.md
```

---
## Assignment 03 — Buddy

Assignment 03 implements:

* Gradient Descent for polynomial functions
* Maxflow-Mincut using Dinic's algorithm
* 
Assignment 03 includes Gradient Descent for polynomial optimization and Maxflow-Mincut using Dinic’s algorithm on CSR-based directed graphs.

Detailed implementation, compilation, execution and test results are documented in:

```text
assignment_03/README.md
```
---

# Runtime Measurement

For all graph algorithms:

* Input reading is not included in the measured time.
* Input parsing is not included.
* CSR conversion is performed before timing.
* Output printing is not included.
* The timer starts immediately before the algorithm call.
* The timer stops immediately after the algorithm finishes.
* Execution time is reported in milliseconds.

This follows the CS509 timing requirements.


