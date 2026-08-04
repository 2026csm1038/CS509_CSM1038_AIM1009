#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <limits>
#include "../src/csr.h"
#include "../src/sssp.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <input_file>" << endl;
        return 1;
    }

    ifstream infile(argv[1]);
    if (!infile.is_open()) {
        cerr << "Error: could not open input file: " << argv[1] << endl;
        return 1;
    }

    
    int V, E;
    infile >> V >> E;

    vector<vector<pair<int,double>>> adjList(V); // Adjacency list: for each vertex u, a list of (neighbor, weight) pairs.

    for (int i = 0; i < V; i++) {
        int u, degree;
        infile >> u >> degree;
        for (int j = 0; j < degree; j++) {
            int neighbor;
            double weight;
            infile >> neighbor >> weight;
            if (weight <= 0) {
                cerr << "Error: SSSP requires all edge weights to be positive." << endl;// SSSP requires strictly positive edge weights
                return 1;
            }
            adjList[u].push_back({neighbor, weight});
        }
    }

    string sourceLabel;
    int source;
    infile >> sourceLabel >> source;

    if (sourceLabel != "SOURCE") {
        cerr << "Error: expected SOURCE line in input file." << endl;
        return 1;
    }
    if (source < 0 || source >= V) {
        cerr << "Error: invalid source vertex." << endl;
        return 1;
    }

    infile.close();

    
    CSRGraph graph = CSRconversion(adjList, V, E);//convert adjacency list into CSR format (conversion time is not added to the timer)

    //algo time 
    auto startTime = chrono::high_resolution_clock::now();
    vector<double> dist = dijkstra(graph, source);
    auto endTime = chrono::high_resolution_clock::now();
    double elapsedMs = chrono::duration<double, milli>(endTime - startTime).count();

    
    const double INF = numeric_limits<double>::infinity();
    cout << "Algorithm: SSSP" << endl;
    cout << "Source: " << source << endl;
    cout << "Vertex Distance" << endl;
    for (int v = 0; v < V; v++) {
        cout << v << " ";
        if (dist[v] == INF) {
            cout << "INF" << endl;
        } else {
            cout << dist[v] << endl;
        }
    }
    cout << "Execution time: " << elapsedMs << " ms" << endl;

    return 0;
}
