#include "connected_components.h"
#include "../../assignment_01/src/bfs.h"
using namespace std;

ComponentsResult connectedComponents(const CSRGraph& graph) {
    ComponentsResult result;
    result.component.assign(graph.V, -1);
    int numComp = 0;

    // Run BFS from every not-yet-visited vertex. Each BFS call only ever
    // touches the vertices of its own component, so across the whole loop
    for (int v = 0; v < graph.V; v++) {
        if (result.component[v] == -1) {
            BFSResult res = bfs(graph, v);
            for (int u : res.traversal) {
                result.component[u] = numComp;
            }
            numComp++;
        }
    }

    result.numComponents = numComp;
    return result;
}