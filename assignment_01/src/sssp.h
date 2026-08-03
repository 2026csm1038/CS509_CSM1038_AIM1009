#ifndef SSSP_H
#define SSSP_H
#include <vector>
#include "csr.h"

std::vector<double> dijkstra(const CSRGraph& graph, int source);

#endif
