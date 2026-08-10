// bc_driver.cpp
// Driver for Betweenness Centrality.
// Usage: ./bc_driver <input_file>
//
// Input format (Section 8.1 of the assignment spec):
//   V E
//   u0 degree neighbor1 neighbor2 ...
//   u1 degree neighbor1 neighbor2 ...
//   ...
// No SOURCE line -- centrality is computed for every vertex.
//
// CSR conversion is done via the shared CSRconversion() helper from
// assignment_01/src/csr.h. Since BC's graph is unweighted, every edge
// is given weight 1.0 when building the adjacency list that gets
// passed to CSRconversion (the weight is ignored by the algorithm).

#include "../src/betweenness_centrality.h"
#include "../../assignment_01/src/csr.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <utility>
#include <chrono>
#include <iomanip>
#include <stdexcept>

// Reads the adjacency-list file into the weighted format CSRconversion
// expects, with every weight set to 1.0 (BC's graph is unweighted).
static std::vector<std::vector<std::pair<int, double>>>
readAdjacencyList(const std::string& path, int& V, int& E) {
    std::ifstream infile(path);
    if (!infile.is_open()) {
        throw std::runtime_error("Could not open input file: " + path);
    }

    infile >> V >> E;
    if (infile.fail() || V < 0 || E < 0) {
        throw std::runtime_error("Malformed header: expected 'V E' at top of file.");
    }

    std::vector<std::vector<std::pair<int, double>>> adjList(V);

    for (int i = 0; i < V; ++i) {
        int vertexId, degree;
        infile >> vertexId >> degree;
        if (infile.fail() || vertexId < 0 || vertexId >= V || degree < 0) {
            throw std::runtime_error("Malformed adjacency row for vertex " + std::to_string(i));
        }

        adjList[vertexId].reserve(degree);
        for (int j = 0; j < degree; ++j) {
            int neighbor;
            infile >> neighbor;
            if (infile.fail() || neighbor < 0 || neighbor >= V) {
                throw std::runtime_error("Malformed neighbor entry for vertex " + std::to_string(vertexId));
            }
            adjList[vertexId].push_back({neighbor, 1.0});   // unweighted -> weight 1.0
        }
    }

    return adjList;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Error: missing input file path.\n";
        std::cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }

    std::string inputPath = argv[1];
    int V = 0, E = 0;
    std::vector<std::vector<std::pair<int, double>>> adjList;

    try {
        adjList = readAdjacencyList(inputPath, V, E);
    } catch (const std::exception& ex) {
        std::cerr << "Error reading input file: " << ex.what() << "\n";
        return 1;
    }

    // CSR conversion is setup work -- not timed, per Section 10.
    CSRGraph csr = CSRconversion(adjList, V, E);

    // Timer wraps only the algorithm call.
    auto startTime = std::chrono::high_resolution_clock::now();
    std::vector<double> centrality = betweennessCentrality(csr);
    auto endTime = std::chrono::high_resolution_clock::now();

    double elapsedMs = std::chrono::duration<double, std::milli>(endTime - startTime).count();

    // Output format per Section 8.3
    std::cout << "Algorithm: Betweenness Centrality\n";
    std::cout << "Vertex Centrality\n";
    std::cout << std::fixed << std::setprecision(2);
    for (int v = 0; v < V; ++v) {
        std::cout << v << " " << centrality[v] << "\n";
    }
    std::cout << "Execution time: " << elapsedMs << " ms\n";

    return 0;
}
