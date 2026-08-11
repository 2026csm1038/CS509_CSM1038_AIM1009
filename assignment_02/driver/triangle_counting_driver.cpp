#include "../../assignment_01/src/csr.h"
#include "../src/triangle_counting.h"
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
            adjList[u].push_back({neighbor, 1.0}); // unweighted -> placeholder weight
        }
    }
    fin.close();

    // ---------- Adjacency list -> CSR (NOT timed); reuses Assignment 1's function ----------
    CSRGraph graph = CSRconversion(adjList, V, E);

    // Sorting neighbour lists is preprocessing too -- needed for the fast
    // common-neighbour check -- so it happens before the timer starts.
    sortCSRNeighbors(graph);

    
    bool collectTriangles = (V <= 100);

    // ---------- Timed region: algorithm only ----------
    auto t_start = high_resolution_clock::now();
    TriangleResult result = countTriangles(graph, collectTriangles);
    auto t_end = high_resolution_clock::now();
    double elapsed_ms = duration<double, milli>(t_end - t_start).count();

    // ---------- Output (NOT timed) ----------
    cout << "Algorithm: Triangle Counting" << endl;
    cout << "Total triangles: " << result.count << endl;

    if (collectTriangles) {
        cout << "Triangles found:" << endl;
        for (auto& t : result.triangles) {
            cout << "(" << t[0] << ", " << t[1] << ", " << t[2] << ")" << endl;
        }
    }

    cout << "Execution time: " << elapsed_ms << " ms" << endl;

    return 0;
}
