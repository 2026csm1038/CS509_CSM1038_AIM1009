#include "../../assignment_01/src/csr.h"
#include "../src/maxflow_mincut.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        cerr << "Usage: " << argv[0] << " <input_file>" << endl;
        return 1;
    }

    ifstream fin(argv[1]);

    if (!fin.is_open())
    {
        cerr << "Error: could not open input file: " << argv[1] << endl;
        return 1;
    }

    // ---------- Reading + parsing (NOT timed) ----------

    int V, E;
    fin >> V >> E;

    if (!fin || V <= 0 || E < 0)
    {
        cerr << "Error: invalid V/E in input file." << endl;
        return 1;
    }

    vector<vector<pair<int, double>>> adjList(V);

    for (int i = 0; i < V; i++)
    {
        int u, degree;
        fin >> u >> degree;

        if (!fin || u < 0 || u >= V || degree < 0)
        {
            cerr << "Error: invalid vertex/degree in input file." << endl;
            return 1;
        }

        for (int j = 0; j < degree; j++)
        {
            int neighbor;
            long long capacity;
            fin >> neighbor >> capacity;

            if (!fin || neighbor < 0 || neighbor >= V)
            {
                cerr << "Error: invalid neighbor vertex in input file." << endl;
                return 1;
            }

            if (capacity < 0)
            {
                cerr << "Error: edge capacities must be non-negative." << endl;
                return 1;
            }

            adjList[u].push_back({neighbor, (double)capacity});
        }
    }

    string label;
    int source, sink;

    fin >> label >> source;

    if (!fin || label != "SOURCE")
    {
        cerr << "Error: missing or invalid SOURCE line." << endl;
        return 1;
    }

    fin >> label >> sink;

    if (!fin || label != "SINK")
    {
        cerr << "Error: missing or invalid SINK line." << endl;
        return 1;
    }

    fin.close();

    if (source < 0 || source >= V || sink < 0 || sink >= V)
    {
        cerr << "Error: SOURCE/SINK must be valid vertices." << endl;
        return 1;
    }

    if (source == sink)
    {
        cerr << "Error: SOURCE and SINK must be different vertices." << endl;
        return 1;
    }

    // ---------- Adjacency list -> CSR (NOT timed); reuses Assignment 1's function ----------

    CSRGraph graph = CSRconversion(adjList, V, E);

    // ---------- Timed region: residual-network build + max-flow/min-cut algorithm ----------

    auto t_start = high_resolution_clock::now();
    MaxflowResult result = maxflowMinCut(graph, source, sink);
    auto t_end = high_resolution_clock::now();

    double elapsed_ms = duration<double, milli>(t_end - t_start).count();

    // ---------- Output (NOT timed) ----------

    cout << "Algorithm: Maxflow-Mincut" << endl;
    cout << "Source: " << source << endl;
    cout << "Sink: " << sink << endl;
    cout << "Maximum flow: " << result.maxFlow << endl;
    cout << "Minimum cut capacity: " << result.minCutCapacity << endl;

    cout << "Source side:";
    for (int v : result.sourceSide)
        cout << " " << v;
    cout << endl;

    cout << "Sink side:";
    for (int v : result.sinkSide)
        cout << " " << v;
    cout << endl;

    cout << "Cut edges:" << endl;
    for (const auto& edge : result.cutEdges)
    {
        cout << get<0>(edge) << " " << get<1>(edge) << " " << get<2>(edge) << endl;
    }

    cout << "Execution time: " << elapsed_ms << " ms" << endl;

    return 0;
}
