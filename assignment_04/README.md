# Assignment 04

## Algorithms Implemented

* K-Means Clustering
* FastMap

---

## Directory Structure

```text
assignment_04/
├── src/
│   ├── kmeans.h
│   ├── kmeans.cpp
│   ├── fastmap.h
│   └── fastmap.cpp
│
├── driver/
│   ├── kmeans_driver.cpp
│   └── fastmap_driver.cpp
│
└── tests/
    ├── kmeans/
    │   ├── km_01.txt
    │   ├── km_02.txt
    │   ├── km_03.txt
    │   ├── km_04.txt
    │   ├── km_collinear.txt
    │   ├── km_duplicates.txt
    │   ├── km_empty_cluster.txt
    │   ├── km_high_dimension.txt
    │   ├── km_identical.txt
    │   ├── km_invalid_d.txt
    │   ├── km_invalid_iterations.txt
    │   ├── km_invalid_k_large.txt
    │   ├── km_invalid_k_zero.txt
    │   ├── km_invalid_n.txt
    │   ├── km_invalid_tolerance.txt
    │   ├── km_negative_coordinates.txt
    │   └── km_two_points.txt
    │
    └── fastmap/
        ├── fm_01.txt
        ├── fm_02.txt
        ├── fm_03.txt
        ├── fm_04.txt
        └── ...
```

---

# 1. K-Means Clustering

K-Means is an iterative clustering algorithm that partitions `N` data points in `D`-dimensional space into `K` clusters.

The implementation uses the first `K` input points as the initial centroids to keep the results reproducible.

At each iteration:

1. Each point is assigned to the nearest centroid using Euclidean distance.
2. Each centroid is recomputed as the mean of the points assigned to that cluster.
3. The algorithm checks the centroid shift against the specified tolerance.
4. The process continues until convergence or until the maximum number of iterations is reached.
5. If a cluster becomes empty, its previous centroid is retained.

The implementation supports:

* Arbitrary number of points `N`
* Arbitrary dimensions `D`
* Arbitrary number of clusters `K`
* Maximum iteration limit
* Convergence tolerance
* Empty clusters
* Negative coordinates
* Duplicate points
* High-dimensional data

## Input Format

```text
N D K
x0_1 x0_2 ... x0_D
x1_1 x1_2 ... x1_D
...
x(N-1)_1 x(N-1)_2 ... x(N-1)_D
MAX_ITERATIONS n
TOLERANCE epsilon
```

## Complexity

For `N` points, `D` dimensions, `K` clusters and `I` iterations:

* **Time Complexity:** `O(I × N × K × D)`
* **Space Complexity:** `O(N × D + K × D)`

The assignment and centroid-update steps for all iterations are included in the measured execution time.

## Compilation

```bash
g++ -O2 -std=c++17 \
assignment_04/src/kmeans.cpp \
assignment_04/driver/kmeans_driver.cpp \
-o assignment_04/driver/kmeans_driver
```

## Execution

```bash
./assignment_04/driver/kmeans_driver \
assignment_04/tests/kmeans/km_01.txt
```

---

# 2. FastMap

FastMap is a heuristic dimensionality-reduction algorithm that maps `N` objects, described by pairwise distances, into a `k`-dimensional Euclidean space.

Unlike K-Means, FastMap does not require the original feature vectors. It operates directly on the supplied pairwise distance matrix.

For every target dimension, the implementation:

1. Selects an approximately farthest pair of pivot objects.
2. Projects every object onto the line between the two pivots using the law of cosines.
3. Deflates the remaining pairwise distances to remove the contribution of the current dimension.
4. Repeats the process until `k` dimensions have been generated.

The pivot-selection process uses a farthest-point heuristic.

## Input Format

```text
N K
d(0,0) d(0,1) ... d(0,N-1)
d(1,0) d(1,1) ... d(1,N-1)
...
d(N-1,0) d(N-1,1) ... d(N-1,N-1)
```

The distance matrix must:

* Be square
* Be symmetric
* Have zero diagonal
* Contain non-negative distances
* Represent meaningful distances satisfying the triangle inequality

## Complexity

For `N` objects and `k` target dimensions:

* **Time Complexity:** approximately `O(k × N²)`
* **Space Complexity:** `O(N² + N × k)`

The pivot selection, projection and distance-deflation operations for all target dimensions are included in the measured execution time.

For large inputs, unnecessary additional copies of the distance matrix should be avoided.

## Compilation

```bash
g++ -O2 -std=c++17 \
assignment_04/src/fastmap.cpp \
assignment_04/driver/fastmap_driver.cpp \
-o assignment_04/driver/fastmap_driver
```

## Execution

```bash
./assignment_04/driver/fastmap_driver \
assignment_04/tests/fastmap/fm_01.txt
```

---

# 3. K-Means Results

| File                          |       N |  D |  K | Max Iter. | Actual Iter. |           WCSS |          Time | Status |
| ----------------------------- | ------: | -: | -: | --------: | -----------: | -------------: | ------------: | ------ |
| `km_01.txt`                   |     100 |  2 |  3 |       300 |            2 |     458.936481 |   0.021595 ms | Pass   |
| `km_02.txt`                   |   1,000 |  2 |  5 |       300 |            3 |    4623.525569 |   0.298351 ms | Pass   |
| `km_03.txt`                   |  10,000 |  5 |  8 |       300 |            2 |  111276.783681 |   7.923169 ms | Pass   |
| `km_04.txt`                   | 100,000 |  5 | 10 |       300 |            2 | 1127230.893296 | 100.403399 ms | Pass   |
| `km_collinear.txt`            |      20 |  2 |  3 |       300 |            - |     367.500000 |   0.026264 ms | Pass   |
| `km_duplicates.txt`           |       8 |  2 |  4 |       300 |            - |     200.000000 |   0.011655 ms | Pass   |
| `km_empty_cluster.txt`        |       9 |  2 |  3 |       300 |            - |     300.210000 |   0.038695 ms | Pass   |
| `km_high_dimension.txt`       |      50 | 10 |  5 |       300 |            - | 1147127.507257 |   0.095676 ms | Pass   |
| `km_identical.txt`            |      10 |  2 |  3 |       300 |            - |       0.000000 |   0.005117 ms | Pass   |
| `km_invalid_d.txt`            |       5 |  0 |  2 |         - |            - |              - |             - | Fail   |
| `km_invalid_iterations.txt`   |       3 |  2 |  2 |         0 |            - |              - |             - | Fail   |
| `km_invalid_k_large.txt`      |       3 |  2 |  5 |         - |            - |              - |             - | Fail   |
| `km_invalid_k_zero.txt`       |       5 |  2 |  0 |         - |            - |              - |             - | Fail   |
| `km_invalid_n.txt`            |      -5 |  2 |  2 |         - |            - |              - |             - | Fail   |
| `km_invalid_tolerance.txt`    |       3 |  2 |  2 |       100 |            - |              - |             - | Fail   |
| `km_negative_coordinates.txt` |       6 |  2 |  2 |       300 |            - |       8.000000 |   0.006872 ms | Pass   |
| `km_two_points.txt`           |       2 |  2 |  2 |       300 |            - |       0.000000 |   0.005349 ms | Pass   |


# 4. FastMap Results

| File | N | Target k | Pivots (per dim) | Avg. Distance Error | Time | Status |
| ---- | --: | --: | --- | --: | --: | ------ |
| `fm_01.txt` | 10 | 2 | d1(0,6), d2(8,5) | – | 0.001430 ms | Pass |
| `fm_02.txt` | 100 | 2 | d1(0,53), d2(31,30) | – | 0.094998 ms | Pass |
| `fm_03.txt` | 1,000 | 3 | d1(190,854), d2(763,121), d3(38,23) | – | 12.002081 ms | Pass |
| `fm_04.txt` | 10,000 | 3 | d1(8838,625), d2(5890,1626), d3(9966,4235) | – | 2088.927451 ms | Pass |

Pivot selection is randomized (farthest-point heuristic), so exact pivots and coordinates can differ slightly between correct runs; only pivot *indices* are reported here, per file, per target dimension.

The optional 50,000-object test (`fm_05.txt`) was not generated — at that size the distance matrix alone is on the order of tens of GB as plain text, so it was not attempted on this machine.

---

## References

### K-Means Clustering

* Stanford CS229 — K-Means Clustering
* Wikipedia — K-Means Clustering

### FastMap

* ACM Digital Library — FastMap
* Wikipedia — Dimensionality Reduction

