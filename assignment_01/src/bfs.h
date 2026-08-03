#ifndef BFS_H
#define BFS_H

#include "csr.h"
#include <vector>
using namespace std;


struct BFSResult {
    vector<int> traversal;
    vector<int> distance;
};

BFSResult bfs(const CSRGraph& graph, int source);

#endif
