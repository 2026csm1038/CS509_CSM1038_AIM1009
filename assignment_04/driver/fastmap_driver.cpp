#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <string>

#include "../src/fastmap.h"

using namespace std;
using namespace chrono;

static bool readFastMapInput(
    const string& filename,
    vector<vector<double>>& distances,
    int& k)
{
    ifstream input(filename);

    if (!input)
    {
        cerr << "Error: cannot open input file: "
             << filename << endl;
        return false;
    }

    int n;

    if (!(input >> n >> k))
    {
        cerr << "Error: invalid FastMap header." << endl;
        return false;
    }

    if (n <= 0)
    {
        cerr << "Error: N must be positive." << endl;
        return false;
    }

    if (k <= 0 || k >= n)
    {
        cerr << "Error: target dimensionality k must satisfy "
             << "1 <= k < N." << endl;
        return false;
    }

    distances.assign(n, vector<double>(n));

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (!(input >> distances[i][j]))
            {
                cerr << "Error: invalid distance matrix." << endl;
                return false;
            }

            if (distances[i][j] < 0.0)
            {
                cerr << "Error: negative distance found at "
                     << "(" << i << ", " << j << ")."
                     << endl;
                return false;
            }
        }
    }

    /*
     * Validate:
     * - diagonal must be zero
     * - matrix must be symmetric
     */
    const double EPS = 1e-9;

    for (int i = 0; i < n; i++)
    {
        if (fabs(distances[i][i]) > EPS)
        {
            cerr << "Error: distance matrix diagonal must be zero."
                 << endl;
            return false;
        }

        for (int j = i + 1; j < n; j++)
        {
            if (fabs(distances[i][j] - distances[j][i]) > EPS)
            {
                cerr << "Error: distance matrix must be symmetric."
                     << endl;
                return false;
            }
        }
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

    vector<vector<double>> distances;
    int k;

    /*
     * Input parsing is NOT timed.
     */
    if (!readFastMapInput(filename, distances, k))
    {
        return 1;
    }

    /*
     * Start timing immediately before the algorithm.
     *
     * The FastMap function includes:
     * - pivot selection
     * - projection
     * - distance deflation
     */
    auto start = high_resolution_clock::now();

    FastMapResult result =
        fastMap(distances, k);

    auto end = high_resolution_clock::now();

    double executionTime =
        duration<double, milli>(end - start).count();

    cout << fixed << setprecision(6);

    cout << "Algorithm: FastMap" << endl;
    cout << "Target dimensions: " << k << endl;

    cout << "Pivots per dimension:" << endl;

    for (int d = 0; d < (int)result.pivots.size(); d++)
    {
        cout << "Dim " << d + 1 << ": "
             << result.pivots[d].first << " "
             << result.pivots[d].second
             << endl;
    }

    cout << "Object coordinates:" << endl;

    for (int i = 0; i < (int)result.coordinates.size(); i++)
    {
        cout << i << ":";

        for (int d = 0; d < k; d++)
        {
            cout << " "
                 << result.coordinates[i][d];
        }

        cout << endl;
    }

    cout << "Execution time: "
         << executionTime
         << " ms"
         << endl;

    return 0;
}
