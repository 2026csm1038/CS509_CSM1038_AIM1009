// betweenness_centrality.h
#ifndef BETWEENNESS_CENTRALITY_H
#define BETWEENNESS_CENTRALITY_H

#include <vector>
#include "../../assignment_01/src/csr.h"   // shared CSRGraph + CSRconversion

// Computes raw (unnormalized) betweenness centrality for every vertex
// using Brandes' algorithm. Assumes an unweighted, undirected graph
// (edge weights in the CSR are ignored -- only adjacency matters).
std::vector<double> betweennessCentrality(const CSRGraph& csr);

#endif // BETWEENNESS_CENTRALITY_H
