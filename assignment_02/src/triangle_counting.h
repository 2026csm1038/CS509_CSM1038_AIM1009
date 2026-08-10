#ifndef TRIANGLE_COUNTING_H
#define TRIANGLE_COUNTING_H

#include "../../assignment_01/src/csr.h"
#include <vector>
#include <array>
using namespace std;

struct TriangleResult {
    long long count;
    vector<array<int,3>> triangles; // filled only when collectTriangles=true
};

// Sorts each vertex's neighbour list in place. 
void sortCSRNeighbors(CSRGraph& graph);

// Counts triangles in an undirected graph stored in CSR form.
// If collectTriangles is true, each triangle (u < v < w) is recorded once.
TriangleResult countTriangles(const CSRGraph& graph, bool collectTriangles);

#endif