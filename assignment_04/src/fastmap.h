#ifndef FASTMAP_H
#define FASTMAP_H

#include <vector>
#include <utility>

using namespace std;

struct FastMapResult
{
    vector<vector<double>> coordinates;
    vector<pair<int, int>> pivots;
};

FastMapResult fastMap(vector<vector<double>>& distances, int k);

#endif

