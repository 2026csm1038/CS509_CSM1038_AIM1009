#include "../src/dfs.h"
#include "../src/csr.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
using namespace std;
using namespace std::chrono;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <input_file>" << endl;
        return 1;
    }

    ifstream fin(argv[1]);
    if (!fin.is_open()) {
        cerr << "Error: could not open input file: " << argv[1] << endl;
        return 1;
    }

    // ---------- Reading + parsing (NOT timed) ----------
    int V, E;
    fin >> V >> E;

    vector<vector<pair<int,double>>> adjList(V);

    for (int i = 0; i < V; i++) {
        int u, degree;
        fin >> u >> degree;
        for (int j = 0; j < degree; j++) {
            int neighbor;
            fin >> neighbor;
            adjList[u].push_back({neighbor, 1.0}); // DFS is unweighted; weight is a placeholder
        }
    }

    string label;   // reads the literal word "SOURCE"
    int source;
    fin >> label >> source;
    fin.close();

    if (source < 0 || source >= V) {
        cerr << "Error: source vertex out of range." << endl;
        return 1;
    }

    // ---------- Adjacency list -> CSR conversion (NOT timed) ----------
    CSRGraph graph = CSRconversion(adjList, V, E);

    // ---------- Timed region: algorithm only ----------
    auto t_start = high_resolution_clock::now();
    vector<int> traversal = dfs(graph, source);
    auto t_end = high_resolution_clock::now();
    double elapsed_ms = duration<double, milli>(t_end - t_start).count();

    // ---------- Output (NOT timed) ----------
    cout << "Algorithm: DFS" << endl;
    cout << "Source: " << source << endl;

    cout << "Traversal: ";
    for (int v : traversal) cout << v << " ";
    cout << endl;

    cout << "Execution time: " << elapsed_ms << " ms" << endl;

    return 0;
}
