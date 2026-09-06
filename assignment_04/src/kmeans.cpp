#include "kmeans.h"

#include <cmath>
#include <limits>

using namespace std;

// Squared Euclidean distance between two points.
// Squared distance is sufficient for nearest-centroid
// comparisons and avoids an unnecessary sqrt call.
static double squaredDistance(
    const vector<double>& a,
    const vector<double>& b)
{
    double sum = 0.0;

    for (int d = 0; d < (int)a.size(); d++)
    {
        double diff = a[d] - b[d];
        sum += diff * diff;
    }

    return sum;
}

// Assign every point to its nearest centroid.
// Returns true if at least one point changed its
// assignment compared to the previous labeling.
static bool assignPoints(
    const vector<vector<double>>& points,
    const vector<vector<double>>& centroids,
    vector<int>& assignments)
{
    bool changed = false;

    int n = points.size();
    int k = centroids.size();

    for (int i = 0; i < n; i++)
    {
        int bestCluster = 0;
        double bestDistance = numeric_limits<double>::max();

        for (int c = 0; c < k; c++)
        {
            double distance =
                squaredDistance(points[i], centroids[c]);

            if (distance < bestDistance)
            {
                bestDistance = distance;
                bestCluster = c;
            }
        }

        if (assignments[i] != bestCluster)
            changed = true;

        assignments[i] = bestCluster;
    }

    return changed;
}

// Recompute each centroid as the mean of its assigned points.
// If a cluster becomes empty, its previous centroid is kept
// unchanged for this iteration.
// Returns the maximum centroid shift (Euclidean distance)
// across all clusters, used for the tolerance check.
static double updateCentroids(
    const vector<vector<double>>& points,
    const vector<int>& assignments,
    vector<vector<double>>& centroids)
{
    int k = centroids.size();
    int d = centroids[0].size();
    int n = points.size();

    vector<vector<double>> sums(k, vector<double>(d, 0.0));
    vector<int> counts(k, 0);

    for (int i = 0; i < n; i++)
    {
        int c = assignments[i];
        counts[c]++;

        for (int dim = 0; dim < d; dim++)
        {
            sums[c][dim] += points[i][dim];
        }
    }

    double maxShift = 0.0;

    for (int c = 0; c < k; c++)
    {
        if (counts[c] == 0)
        {
            // Empty cluster: keep previous centroid unchanged.
            continue;
        }

        vector<double> newCentroid(d);

        for (int dim = 0; dim < d; dim++)
        {
            newCentroid[dim] = sums[c][dim] / counts[c];
        }

        double shift =
            sqrt(squaredDistance(newCentroid, centroids[c]));

        if (shift > maxShift)
            maxShift = shift;

        centroids[c] = newCentroid;
    }

    return maxShift;
}

// Within-cluster sum of squared distances (WCSS).
static double computeWCSS(
    const vector<vector<double>>& points,
    const vector<int>& assignments,
    const vector<vector<double>>& centroids)
{
    double wcss = 0.0;

    for (int i = 0; i < (int)points.size(); i++)
    {
        wcss += squaredDistance(
            points[i], centroids[assignments[i]]);
    }

    return wcss;
}

KMeansResult kMeans(
    const vector<vector<double>>& points,
    int k,
    int maxIterations,
    double tolerance)
{
    KMeansResult result;

    int n = points.size();

    if (n == 0 || k <= 0 || k > n)
        return result;

    // Initialize centroids as the first K input points,
    // in input order, for reproducibility.
    vector<vector<double>> centroids(k);

    for (int c = 0; c < k; c++)
    {
        centroids[c] = points[c];
    }

    vector<int> assignments(n, -1);

    int iterations = 0;
    bool converged = false;

    while (iterations < maxIterations)
    {
        bool changed = assignPoints(points, centroids, assignments);

        double shift = updateCentroids(points, assignments, centroids);

        iterations++;

        if (!changed || shift <= tolerance)
        {
            converged = true;
            break;
        }
    }

    result.assignments = assignments;
    result.centroids = centroids;
    result.wcss = computeWCSS(points, assignments, centroids);
    result.iterations = iterations;
    result.converged = converged;

    return result;
}
