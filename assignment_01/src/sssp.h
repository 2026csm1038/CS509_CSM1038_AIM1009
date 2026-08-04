#ifndef SSSP_H
#define SSSP_H
#include <vector>
#include "csr.h"


// Returns a vector which is the shortest distance from source to vertex i.
// Unreachable vertices will have distance = infinity.
std::vector<double> dijkstra(const CSRGraph& graph, int source);

#endif
