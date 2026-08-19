#ifndef MAXFLOW_MINCUT_H
#define MAXFLOW_MINCUT_H

#include <vector>
#include <tuple>

#include "../../assignment_01/src/csr.h"

using namespace std;

struct MaxflowResult
{
    long long maxFlow;
    long long minCutCapacity;

    vector<int> sourceSide; // vertices reachable from source in final residual graph
    vector<int> sinkSide;   // remaining vertices

    // cut edges as (u, v, capacity), directed edges from sourceSide to sinkSide
    vector<tuple<int, int, long long>> cutEdges;
};

// Computes maximum flow (Dinic's algorithm) and the corresponding minimum
// s-t cut on a directed capacitated graph supplied in CSR form.
// graph.values holds edge capacities (non-negative integers stored as double).
// Building the residual network from the CSR representation happens inside
// this call, so it is part of the timed algorithm region as required by the
// assignment spec.
MaxflowResult maxflowMinCut(const CSRGraph& graph, int source, int sink);

#endif
