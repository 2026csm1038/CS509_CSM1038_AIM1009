#include "sssp.h"
#include <queue>
#include <limits>

using namespace std;

vector<double> dijkstra(const CSRGraph& graph, int source) {
    const double INF = numeric_limits<double>::infinity();
    vector<double> dist(graph.V, INF);
    dist[source] = 0;

    using PQItem = pair<double,int>;
    priority_queue<PQItem, vector<PQItem>, greater<PQItem>> pq;
    pq.push({0.0, source});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;

        int start = graph.row_ptr[u];
        int end = graph.row_ptr[u+1];
        for (int i = start; i < end; i++) {
            int v = graph.col_ind[i];
            double w = graph.values[i];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
