#include "maxflow_mincut.h"

#include <queue>
#include <climits>
#include <cmath>

using namespace std;

namespace
{
    struct Edge
    {
        int to;
        long long cap;
        int rev; // index of the reverse edge in adj[to]
    };

    // Dinic's algorithm on an explicit residual adjacency list.
    // The DFS phase (blocking flow) is implemented with an explicit stack
    // instead of recursion, so it stays safe on the larger required graph
    // sizes (V up to 50,000) where a recursive call chain could otherwise
    // approach the recursion depth / stack limit.
    class Dinic
    {
    public:
        int V;
        vector<vector<Edge>> adj;
        vector<int> level;
        vector<int> iter;

        explicit Dinic(int V) : V(V), adj(V), level(V, -1), iter(V, 0) {}

        void addEdge(int from, int to, long long cap)
        {
            Edge forward{to, cap, (int)adj[to].size()};
            Edge backward{from, 0, (int)adj[from].size()};

            adj[from].push_back(forward);
            adj[to].push_back(backward);
        }

        bool bfs(int s, int t)
        {
            fill(level.begin(), level.end(), -1);

            queue<int> q;
            level[s] = 0;
            q.push(s);

            while (!q.empty())
            {
                int u = q.front();
                q.pop();

                for (const Edge& e : adj[u])
                {
                    if (e.cap > 0 && level[e.to] < 0)
                    {
                        level[e.to] = level[u] + 1;
                        q.push(e.to);
                    }
                }
            }

            return level[t] >= 0;
        }

        // Finds one blocking flow for the current level graph, using an
        // explicit stack to walk augmenting paths from s to t.
        long long blockingFlow(int s, int t)
        {
            long long totalFlow = 0;

            vector<int> pathVertices;
            vector<int> pathEdgeIdx;
            pathVertices.push_back(s);

            while (!pathVertices.empty())
            {
                int u = pathVertices.back();

                if (u == t)
                {
                    long long bottleneck = LLONG_MAX;

                    for (size_t i = 0; i < pathEdgeIdx.size(); i++)
                    {
                        int uu = pathVertices[i];
                        Edge& e = adj[uu][pathEdgeIdx[i]];
                        bottleneck = min(bottleneck, e.cap);
                    }

                    for (size_t i = 0; i < pathEdgeIdx.size(); i++)
                    {
                        int uu = pathVertices[i];
                        Edge& e = adj[uu][pathEdgeIdx[i]];
                        e.cap -= bottleneck;
                        adj[e.to][e.rev].cap += bottleneck;
                    }

                    totalFlow += bottleneck;

                    // Restart the walk from the source; iter[] pointers are
                    // preserved so already-exhausted edges are not retried.
                    pathVertices.resize(1);
                    pathEdgeIdx.clear();
                    continue;
                }

                bool advanced = false;

                for (int& i = iter[u]; i < (int)adj[u].size(); i++)
                {
                    Edge& e = adj[u][i];

                    if (e.cap > 0 && level[e.to] == level[u] + 1)
                    {
                        pathVertices.push_back(e.to);
                        pathEdgeIdx.push_back(i);
                        advanced = true;
                        break;
                    }
                }

                if (!advanced)
                {
                    // Dead end: remove u from the level graph so no other
                    // path tries to route through it again this phase.
                    level[u] = -1;
                    pathVertices.pop_back();

                    if (!pathEdgeIdx.empty())
                        pathEdgeIdx.pop_back();
                }
            }

            return totalFlow;
        }

        long long maxflow(int s, int t)
        {
            long long flow = 0;

            while (bfs(s, t))
            {
                fill(iter.begin(), iter.end(), 0);
                flow += blockingFlow(s, t);
            }

            return flow;
        }

        vector<bool> reachableFromSource(int s)
        {
            vector<bool> visited(V, false);

            queue<int> q;
            visited[s] = true;
            q.push(s);

            while (!q.empty())
            {
                int u = q.front();
                q.pop();

                for (const Edge& e : adj[u])
                {
                    if (e.cap > 0 && !visited[e.to])
                    {
                        visited[e.to] = true;
                        q.push(e.to);
                    }
                }
            }

            return visited;
        }
    };
}

MaxflowResult maxflowMinCut(const CSRGraph& graph, int source, int sink)
{
    Dinic dinic(graph.V);

    for (int u = 0; u < graph.V; u++)
    {
        for (int idx = graph.row_ptr[u]; idx < graph.row_ptr[u + 1]; idx++)
        {
            int v = graph.col_ind[idx];
            long long cap = (long long)llround(graph.values[idx]);

            dinic.addEdge(u, v, cap);
        }
    }

    MaxflowResult result;
    result.maxFlow = dinic.maxflow(source, sink);

    vector<bool> visited = dinic.reachableFromSource(source);

    for (int i = 0; i < graph.V; i++)
    {
        if (visited[i])
            result.sourceSide.push_back(i);
        else
            result.sinkSide.push_back(i);
    }

    long long cutCapacity = 0;

    for (int u = 0; u < graph.V; u++)
    {
        if (!visited[u])
            continue;

        for (int idx = graph.row_ptr[u]; idx < graph.row_ptr[u + 1]; idx++)
        {
            int v = graph.col_ind[idx];
            long long cap = (long long)llround(graph.values[idx]);

            if (!visited[v] && cap > 0)
            {
                result.cutEdges.push_back(make_tuple(u, v, cap));
                cutCapacity += cap;
            }
        }
    }

    result.minCutCapacity = cutCapacity;

    return result;
}
