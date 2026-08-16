#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <chrono>

#include "../src/gradient_descent.h"

using namespace std;
using namespace chrono;

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        cerr << "Usage: " << argv[0]
             << " <input_file>" << endl;
        return 1;
    }

    ifstream input(argv[1]);

    if (!input)
    {
        cerr << "Error: Could not open input file."
             << endl;
        return 1;
    }

    string label;

    int degree;
    vector<long double> coefficients;

    long double initialX;
    long double learningRate;
    long double tolerance;

    int maxIterations;

    // DEGREE
    input >> label >> degree;

    if (!input || label != "DEGREE")
    {
        cerr << "Error: Invalid DEGREE line." << endl;
        return 1;
    }

    if (degree < 0)
    {
        cerr << "Error: Invalid degree." << endl;
        return 1;
    }

    // COEFFICIENTS
    input >> label;

    if (!input || label != "COEFFICIENTS")
    {
        cerr << "Error: Invalid COEFFICIENTS line."
             << endl;
        return 1;
    }

    coefficients.resize(degree + 1);

    for (int i = 0; i <= degree; ++i)
    {
        input >> coefficients[i];

        if (!input)
        {
            cerr << "Error: Incorrect number of coefficients."
                 << endl;
            return 1;
        }
    }

    // INITIAL_X
    input >> label >> initialX;

    if (!input || label != "INITIAL_X")
    {
        cerr << "Error: Invalid INITIAL_X line."
             << endl;
        return 1;
    }

    // LEARNING_RATE
    input >> label >> learningRate;

    if (!input || label != "LEARNING_RATE")
    {
        cerr << "Error: Invalid LEARNING_RATE line."
             << endl;
        return 1;
    }

    if (learningRate <= 0.0L)
    {
        cerr << "Error: Learning rate must be positive."
             << endl;
        return 1;
    }

    // TOLERANCE
    input >> label >> tolerance;

    if (!input || label != "TOLERANCE")
    {
        cerr << "Error: Invalid TOLERANCE line."
             << endl;
        return 1;
    }

    if (tolerance <= 0.0L)
    {
        cerr << "Error: Tolerance must be positive."
             << endl;
        return 1;
    }

    // MAX_ITERATIONS
    input >> label >> maxIterations;

    if (!input || label != "MAX_ITERATIONS")
    {
        cerr << "Error: Invalid MAX_ITERATIONS line."
             << endl;
        return 1;
    }

    if (maxIterations <= 0)
    {
        cerr << "Error: MAX_ITERATIONS must be positive."
             << endl;
        return 1;
    }

    // -------------------------------------------------
    // Algorithm timing starts here.
    // File reading and validation are excluded.
    // -------------------------------------------------

    auto start = high_resolution_clock::now();

    GradientDescentResult result =
        gradientDescent(
            coefficients,
            initialX,
            learningRate,
            tolerance,
            maxIterations
        );

    auto end = high_resolution_clock::now();

    long double executionTime =
        duration<long double, milli>(end - start).count();

    // -------------------------------------------------
    // Output
    // -------------------------------------------------

    cout << fixed << setprecision(10);

    cout << "Algorithm: Gradient Descent" << endl;
    cout << "Degree: " << degree << endl;

    cout << "Final x: "
         << result.finalX << endl;

    cout << "Final f(x): "
         << result.finalValue << endl;

    cout << "Iterations: "
         << result.iterations << endl;

    cout << "Converged: "
         << (result.converged ? "true" : "false")
         << endl;

    cout << "Execution time: "
         << executionTime << " ms" << endl;

    return 0;
}
