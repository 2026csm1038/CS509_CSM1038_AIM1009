// betweenness_centrality.cpp
// Implements Brandes' algorithm for unweighted, undirected graphs,
// using the shared CSRGraph from assignment_01/src/csr.h.
// Edge weights are ignored -- BC's input graph is unweighted, so
// CSRconversion() is called with every edge weight set to 1.0.

#include "betweenness_centrality.h"
#include <vector>
#include <queue>
#include <stack>

// -----------------------------------------------------------------------
// betweennessCentrality
// Brandes' algorithm, O(V*E) for unweighted graphs.
// Returns raw (unnormalized) betweenness centrality for every vertex.
// -----------------------------------------------------------------------
std::vector<double> betweennessCentrality(const CSRGraph& csr) {
    int V = csr.V;
    std::vector<double> centrality(V, 0.0);

    for (int s = 0; s < V; ++s) {
        // Single-source data structures (Brandes)
        std::vector<std::vector<int>> predecessors(V);
        std::vector<long long> sigma(V, 0);   // number of shortest paths
        std::vector<int> dist(V, -1);         // distance from s
        std::vector<double> delta(V, 0.0);    // dependency of s on v

        sigma[s] = 1;
        dist[s] = 0;

        std::stack<int> order;                // vertices in non-decreasing dist order
        std::queue<int> bfsQueue;
        bfsQueue.push(s);

        while (!bfsQueue.empty()) {
            int v = bfsQueue.front();
            bfsQueue.pop();
            order.push(v);

            int start = csr.row_ptr[v];
            int end = csr.row_ptr[v + 1];
            for (int idx = start; idx < end; ++idx) {
                int w = csr.col_ind[idx];   // weight in csr.values[idx] is ignored (unweighted BC)

                // w found for the first time?
                if (dist[w] < 0) {
                    dist[w] = dist[v] + 1;
                    bfsQueue.push(w);
                }

                // shortest path to w via v?
                if (dist[w] == dist[v] + 1) {
                    sigma[w] += sigma[v];
                    predecessors[w].push_back(v);
                }
            }
        }

        // Accumulate dependencies, processing vertices in reverse BFS order
        while (!order.empty()) {
            int w = order.top();
            order.pop();

            for (int v : predecessors[w]) {
                if (sigma[w] != 0) {
                    delta[v] += (static_cast<double>(sigma[v]) / sigma[w]) * (1.0 + delta[w]);
                }
            }

            if (w != s) {
                centrality[w] += delta[w];
            }
        }
    }

    // Undirected graph: each shortest path is counted once from each
    // endpoint's perspective, so every pair is double-counted.
    for (int v = 0; v < V; ++v) {
        centrality[v] /= 2.0;
    }

    return centrality;
}
