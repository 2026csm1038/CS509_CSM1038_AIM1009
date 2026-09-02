#include "fastmap.h"

#include <cmath>
#include <algorithm>
#include <limits>
#include <cstdlib>

using namespace std;

// Find the object farthest from a given object.
static int findFarthest(
    const vector<vector<double>>& distances,
    int start)
{
    int n = distances.size();

    int farthest = start;
    double maxDistance = -1.0;

    for (int i = 0; i < n; i++)
    {
        if (distances[start][i] > maxDistance)
        {
            maxDistance = distances[start][i];
            farthest = i;
        }
    }

    return farthest;
}

// Select approximately farthest pair of objects.
// FastMap heuristic:
// 1. Pick an arbitrary object.
// 2. Find object farthest from it.
// 3. Find object farthest from that object.
// 4. Repeat a couple of times.
static pair<int, int> choosePivots(
    const vector<vector<double>>& distances)
{
    int n = distances.size();

    if (n < 2)
        return {0, 0};

    int a = 0;
    int b = findFarthest(distances, a);

    for (int iteration = 0; iteration < 2; iteration++)
    {
        a = b;
        b = findFarthest(distances, a);
    }

    return {a, b};
}

FastMapResult fastMap(vector<vector<double>>& distances, int k)
{
    int n = distances.size();

    FastMapResult result;

    if (n == 0 || k <= 0)
        return result;

    k = min(k, n - 1);

    result.coordinates.assign(n, vector<double>(k, 0.0));

    // Working copy of distances.
    //
    // Each iteration modifies this matrix by removing the
    // distance contribution captured by the current dimension.
    vector<vector<double>> currentDistances = distances;

    for (int dimension = 0; dimension < k; dimension++)
    {
        pair<int, int> pivots = choosePivots(currentDistances);

        int a = pivots.first;
        int b = pivots.second;

        result.pivots.push_back({a, b});

        double pivotDistance = currentDistances[a][b];

        // If the pivot distance is zero, all remaining
        // coordinates for this dimension are zero.
        if (pivotDistance <= 0.0)
        {
            for (int i = 0; i < n; i++)
            {
                result.coordinates[i][dimension] = 0.0;
            }

            continue;
        }

        /*
         * Projection using the law of cosines:
         *
         * x_i =
         * (d(a,i)^2 + d(a,b)^2 - d(b,i)^2)
         * ---------------------------------
         *             2*d(a,b)
         *
         * This gives the coordinate of object i along
         * the line joining the two pivots.
         */
        for (int i = 0; i < n; i++)
        {
            double dai = currentDistances[a][i];
            double dbi = currentDistances[b][i];

            double coordinate =
                (dai * dai +
                 pivotDistance * pivotDistance -
                 dbi * dbi)
                / (2.0 * pivotDistance);

            result.coordinates[i][dimension] = coordinate;
        }

        /*
         * Deflate the remaining distances.
         *
         * d'(i,j)^2 =
         * d(i,j)^2 -
         * (x_i - x_j)^2
         *
         * Numerical round-off can occasionally make the
         * value slightly negative, so clamp it to zero.
         */
        for (int i = 0; i < n; i++)
        {
            for (int j = i + 1; j < n; j++)
            {
                double difference =
                    result.coordinates[i][dimension] -
                    result.coordinates[j][dimension];

                double remainingSquared =
                    currentDistances[i][j] *
                    currentDistances[i][j] -
                    difference * difference;

                if (remainingSquared < 0.0)
                    remainingSquared = 0.0;

                double remainingDistance =
                    sqrt(remainingSquared);

                currentDistances[i][j] = remainingDistance;
                currentDistances[j][i] = remainingDistance;
            }
        }
    }

    return result;
}

