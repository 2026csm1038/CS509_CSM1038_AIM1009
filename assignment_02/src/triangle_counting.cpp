#include "triangle_counting.h"
#include <algorithm>
using namespace std;

void sortCSRNeighbors(CSRGraph& graph) {
    for (int u = 0; u < graph.V; u++) {
        sort(graph.col_ind.begin() + graph.row_ptr[u],
             graph.col_ind.begin() + graph.row_ptr[u + 1]);
    }
}

// Binary search for edge (v, w) in v's sorted neighbour list.
static bool hasEdge(const CSRGraph& graph, int v, int w) {
    int start = graph.row_ptr[v];
    int end   = graph.row_ptr[v + 1];
    return binary_search(graph.col_ind.begin() + start, graph.col_ind.begin() + end, w);
}

TriangleResult countTriangles(const CSRGraph& graph, bool collectTriangles) {
    TriangleResult result;
    long long rawCount = 0;

    for (int u = 0; u < graph.V; u++) {
        int start = graph.row_ptr[u];
        int end   = graph.row_ptr[u + 1];

        // Examine every pair of u's neighbours.
        for (int i = start; i < end; i++) {
            for (int j = i + 1; j < end; j++) {
                int v = graph.col_ind[i];
                int w = graph.col_ind[j]; // v <= w since the row is sorted

                if (hasEdge(graph, v, w)) {
                    rawCount++; // each triangle is found once at each of its 3 vertices

                    if (collectTriangles && u < v) {
                        // u is the smallest vertex of this triangle here,
                        // so it is recorded exactly once, as (u, v, w).
                        result.triangles.push_back({u, v, w});
                    }
                }
            }
        }
    }

    result.count = rawCount / 3;
    return result;
}