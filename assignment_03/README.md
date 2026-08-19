# Assignment 03

### Algorithms Implemented

- Gradient Descent
- Maxflow-Mincut Algorithm

## Directory Structure

```text
assignment_03/
├── src/
│   ├── gradient_descent.h
│   ├── gradient_descent.cpp
│   ├── maxflow_mincut.h
│   └── maxflow_mincut.cpp
├── driver/
│   ├── gd_driver.cpp
│   └── maxmin_driver.cpp
└── tests/
    ├── gradient_descent/
    │   ├── gd_01.txt
    │   ├── gd_02.txt
    │   ├── gd_03.txt
    │   ├── gd_04.txt
    │   └── gd_05.txt
    └── maxflow_mincut/
        ├── maxflow_10.txt
        ├── maxflow_100.txt
        ├── maxflow_1000.txt
        ├── maxflow_10000.txt
        ├── maxflow_50000.txt
        ├── maxflow_bottleneck.txt
        ├── maxflow_chain_10.txt
        ├── maxflow_cycles.txt
        ├── maxflow_direct_edge.txt
        ├── maxflow_disconnected_parts.txt
        ├── maxflow_equal_paths.txt
        ├── maxflow_example.txt
        ├── maxflow_layered.txt
        ├── maxflow_parallel_edges.txt
        ├── maxflow_single_edge.txt
        └── maxflow_two_paths.txt
```
        
## 1. Gradient Descent

Gradient Descent is used to minimize an objective function iteratively by moving the current solution in the direction opposite to the gradient.

The implementation supports the required input parameters such as the initial point, learning rate, tolerance and maximum number of iterations.

# Complexity

For a function of degree d, each iteration evaluates the gradient in O(d) time.

If the algorithm performs I iterations, the overall complexity is:

Time Complexity: O(I × d)
Space Complexity: O(d)

# Compilation

```text
g++ -O2 -std=c++17 \
assignment_03/src/gradient_descent.cpp \
assignment_03/driver/gd_driver.cpp \
-o gradient_descent_driver
```

# Execution

```text
./gradient_descent_driver assignment_03/tests/gradient_descent/gd_01.txt
```

## 2. Maxflow-Mincut

The Maxflow-Mincut implementation computes the maximum flow between a source and sink in a directed capacitated graph.

After computing the maximum flow, the final residual graph is used to determine the vertices reachable from the source. These vertices form the source side of the minimum cut, while the remaining vertices form the sink side.

The minimum cut capacity is computed from the original graph using the edges directed from the source side to the sink side.

# Complexity

the general worst-case complexity is:

Time Complexity: O(V²E)
Space Complexity: O(V + E)

For the implemented CSR-to-residual-network conversion, the graph construction requires:  O(V + E)

time and space in addition to the residual network.

# Compilation

```text
g++ -O2 -std=c++17 \
-Iassignment_01/src \
assignment_01/src/csr.cpp \
assignment_03/src/maxflow_mincut.cpp \
assignment_03/driver/maxmin_driver.cpp \
-o maxmin_driver
```

# Execution

```text
./maxmin_driver assignment_03/tests/maxflow_mincut/maxflow_example.txt
```

# Maxflow-Mincut Results

File | V | E | Source | Sink | Expected Flow | Actual Flow | Cut Capacity | Time(ms) | Status
maxflow_10000.txt | 10000 | 29999 | 0 | 9999 | 180 | 180 | 180 | 27.4034 | Pass
maxflow_1000.txt | 1000 | 2999 | 0 | 999 | 70 | 70 | 70 | 2.482 | Pass
maxflow_100.txt | 100 | 299 | 0 | 99 | 78 | 78 | 78 | 0.193008 | Pass
maxflow_10.txt | 10 | 29 | 0 | 9 | 27 | 27 | 27 | 0.027074 | Pass
maxflow_50000.txt | 50000 | 149999 | 0 | 49999 | 186 | 186 | 186 | 160.382 | Pass
maxflow_bottleneck.txt | 6 | 5 | 0 | 5 | 10 | 10 | 10 | 0.009195 | Pass
maxflow_chain_10.txt | 10 | 9 | 0 | 9 | 10 | 10 | 10 | 0.03696 | Pass
maxflow_cycles.txt | 6 | 8 | 0 | 5 | 12 | 12 | 12 | 0.01278 | Pass
maxflow_direct_edge.txt | 4 | 4 | 0 | 3 | 18 | 18 | 18 | 0.008442 | Pass
maxflow_disconnected_parts.txt | 9 | 5 | 0 | 5 | 10 | 10 | 10 | 0.008151 | Pass
maxflow_equal_paths.txt | 6 | 8 | 0 | 5 | 20 | 20 | 20 | 0.173464 | Pass
maxflow_example.txt | 6 | 10 | 0 | 5 | 23 | 23 | 23 | 0.013794 | Pass
maxflow_layered.txt | 10 | 16 | 0 | 9 | 30 | 30 | 30 | 0.017441 | Pass
maxflow_parallel_edges.txt | 4 | 6 | 0 | 3 | 12 | 12 | 12 | 0.009449 | Pass
maxflow_single_edge.txt | 2 | 1 | 0 | 1 | 25 | 25 | 25 | 0.004843 | Pass
maxflow_two_paths.txt | 6 | 7 | 0 | 5 | 17 | 17 | 17 | 0.009371 | Pass

# 3. Test Coverage

The Maxflow-Mincut test cases cover:

Small graphs
Large graphs
Very large graphs
Single-edge networks
Chain networks
Multiple parallel edges
Equal-capacity paths
Bottleneck edges
Direct source-to-sink edges
Cyclic graphs
Layered networks
Disconnected graph components
Multiple source-to-sink paths
Different graph densities
Large values of V and E

The test cases include graphs ranging from:

V = 2 to 50000

and from:

E = 1 to 149999


## References
Gradient Descent
      https://en.wikipedia.org/wiki/Gradient_descent
Maximum Flow and Minimum Cut
    https://en.wikipedia.org/wiki/Maximum_flow_problem
    https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem

