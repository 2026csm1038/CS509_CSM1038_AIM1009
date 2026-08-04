#include "sssp.h"
#include <queue>
#include <limits>

using namespace std;

vector<double> dijkstra(const CSRGraph& graph, int source) {
    const double INF = numeric_limits<double>::infinity();//all distances unknown (infinity) except the source
    vector<double> dist(graph.V, INF);
    dist[source] = 0;

    using PQItem = pair<double,int>;// Min-heap of (distance, vertex) pairs. greater<> makes it a min-heap
    priority_queue<PQItem, vector<PQItem>, greater<PQItem>> pq;
    pq.push({0.0, source});


   // Lazy deletion check: since we never remove outdated entries from
   // the heap when we find a shorter path, an entry might now be stale
   // (a better distance for u was already found and processed).
   // If so, just skip it instead of reprocessing u.
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;

        int start = graph.row_ptr[u];//u's outgoing edges using the CSR range (start, end)
        int end = graph.row_ptr[u+1];
        for (int i = start; i < end; i++) {
            int v = graph.col_ind[i];// neighbor vertex
            double w = graph.values[i];// weight of edge
            

              if (dist[u] + w < dist[v]) {// Relaxation step
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
