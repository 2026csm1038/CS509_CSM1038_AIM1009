#include "gradient_descent.h"

#include <cmath>

using namespace std;

long double evaluatePolynomial(
    const vector<long double>& coefficients,
    long double x
)
{
    if (coefficients.empty())
        return 0.0L;

    long double result = coefficients.back();

    for (int i = (int)coefficients.size() - 2; i >= 0; --i)
    {
        result = result * x + coefficients[i];
    }

    return result;
}

long double evaluateDerivative(
    const vector<long double>& coefficients,
    long double x
)
{
    if (coefficients.size() <= 1)
        return 0.0L;

    long double result =
        (long double)(coefficients.size() - 1) *
        coefficients.back();

    for (int i = (int)coefficients.size() - 2; i >= 1; --i)
    {
        result = result * x +
                 (long double)i * coefficients[i];
    }

    return result;
}

GradientDescentResult gradientDescent(
    const vector<long double>& coefficients,
    long double initialX,
    long double learningRate,
    long double tolerance,
    int maxIterations
)
{
    GradientDescentResult result;

    long double x = initialX;
    int iterations = 0;
    bool converged = false;

    while (iterations < maxIterations)
    {
        long double gradient =
            evaluateDerivative(coefficients, x);

        if (fabsl(gradient) <= tolerance)
        {
            converged = true;
            break;
        }

        x = x - learningRate * gradient;

        iterations++;
    }

    result.finalX = x;
    result.finalValue =
        evaluatePolynomial(coefficients, x);

    result.iterations = iterations;
    result.converged = converged;

    if (!converged)
    {
        long double finalGradient =
            evaluateDerivative(coefficients, x);

        if (fabsl(finalGradient) <= tolerance)
            result.converged = true;
    }

    return result;
}
