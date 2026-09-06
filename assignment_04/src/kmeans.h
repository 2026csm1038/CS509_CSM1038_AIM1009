#ifndef KMEANS_H
#define KMEANS_H

#include <vector>

using namespace std;

struct KMeansResult
{
    vector<int> assignments;
    vector<vector<double>> centroids;
    double wcss;
    int iterations;
    bool converged;
};

KMeansResult kMeans(
    const vector<vector<double>>& points,
    int k,
    int maxIterations,
    double tolerance
);

#endif
