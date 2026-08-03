#include "dfs.h"
#include <stack>
using namespace std;

vector<int> dfs(const CSRGraph& graph, int source) {
    vector<int> traversal;
    vector<bool> visited(graph.V, false);
    stack<int> st;
    st.push(source);

    while (!st.empty()) {
        int u = st.top();
        st.pop();

        if (visited[u]) continue;  
        visited[u] = true;
        traversal.push_back(u);

        int start = graph.row_ptr[u];
        int end   = graph.row_ptr[u + 1];

        
        for (int i = end - 1; i >= start; i--) {
            int v = graph.col_ind[i];
            if (!visited[v]) {
                st.push(v);
            }
        }
    }
    return traversal;
}
