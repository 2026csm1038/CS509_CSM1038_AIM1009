#ifndef CONNECTED_COMPONENTS_H
#define CONNECTED_COMPONENTS_H

#include "../../assignment_01/src/csr.h"
#include <vector>
using namespace std;

struct ComponentsResult {
    int numComponents;
    vector<int> component; // component[i] = component id assigned to vertex i
};

ComponentsResult connectedComponents(const CSRGraph& graph);

#endif