#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <string>
#include <sstream>

#include "../src/kmeans.h"

using namespace std;
using namespace chrono;

static bool readKMeansInput(
    const string& filename,
    vector<vector<double>>& points,
    int& k,
    int& maxIterations,
    double& tolerance)
{
    ifstream input(filename);

    if (!input)
    {
        cerr << "Error: cannot open input file: "
             << filename << endl;
        return false;
    }

    int n, d;

    if (!(input >> n >> d >> k))
    {
        cerr << "Error: invalid K-Means header." << endl;
        return false;
    }

    if (n <= 0)
    {
        cerr << "Error: N must be positive." << endl;
        return false;
    }

    if (d <= 0)
    {
        cerr << "Error: D must be positive." << endl;
        return false;
    }

    if (k <= 0)
    {
        cerr << "Error: K must be positive." << endl;
        return false;
    }

    if (k > n)
    {
        cerr << "Error: K must not exceed N." << endl;
        return false;
    }

    points.assign(n, vector<double>(d));

    for (int i = 0; i < n; i++)
    {
        for (int dim = 0; dim < d; dim++)
        {
            if (!(input >> points[i][dim]))
            {
                cerr << "Error: invalid point data." << endl;
                return false;
            }
        }
    }

    string token;

    if (!(input >> token) || token != "MAX_ITERATIONS")
    {
        cerr << "Error: expected MAX_ITERATIONS." << endl;
        return false;
    }

    if (!(input >> maxIterations))
    {
        cerr << "Error: invalid MAX_ITERATIONS value." << endl;
        return false;
    }

    if (maxIterations <= 0)
    {
        cerr << "Error: MAX_ITERATIONS must be positive." << endl;
        return false;
    }

    if (!(input >> token) || token != "TOLERANCE")
    {
        cerr << "Error: expected TOLERANCE." << endl;
        return false;
    }

    if (!(input >> tolerance))
    {
        cerr << "Error: invalid TOLERANCE value." << endl;
        return false;
    }

    if (tolerance <= 0.0)
    {
        cerr << "Error: TOLERANCE must be positive." << endl;
        return false;
    }

    return true;
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        cerr << "Usage: "
             << argv[0]
             << " <input_file>"
             << endl;

        return 1;
    }

    string filename = argv[1];

    vector<vector<double>> points;
    int k;
    int maxIterations;
    double tolerance;

    /*
     * Input parsing is NOT timed.
     */
    if (!readKMeansInput(
            filename, points, k, maxIterations, tolerance))
    {
        return 1;
    }

    /*
     * Start timing immediately before the algorithm.
     *
     * The kMeans function includes:
     * - the assignment step
     * - the centroid-update step
     * across all iterations.
     */
    auto start = high_resolution_clock::now();

    KMeansResult result =
        kMeans(points, k, maxIterations, tolerance);

    auto end = high_resolution_clock::now();

    double executionTime =
        duration<double, milli>(end - start).count();

    cout << fixed << setprecision(6);

    cout << "Algorithm: K-Means Clustering" << endl;
    cout << "K: " << k << endl;

    cout << "Point assignments:" << endl;

    for (int i = 0; i < (int)result.assignments.size(); i++)
    {
        cout << i << " " << result.assignments[i] << endl;
    }

    cout << "Final centroids:" << endl;

    for (int c = 0; c < (int)result.centroids.size(); c++)
    {
        cout << c << ":";

        for (int dim = 0; dim < (int)result.centroids[c].size(); dim++)
        {
            cout << " " << result.centroids[c][dim];
        }

        cout << endl;
    }

    cout << "WCSS: " << result.wcss << endl;
    cout << "Iterations: " << result.iterations << endl;
    cout << "Converged: "
         << (result.converged ? "true" : "false")
         << endl;

    cout << "Execution time: "
         << executionTime
         << " ms"
         << endl;

    return 0;
}
