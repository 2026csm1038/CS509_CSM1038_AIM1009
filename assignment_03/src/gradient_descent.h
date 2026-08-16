#ifndef GRADIENT_DESCENT_H
#define GRADIENT_DESCENT_H

#include <vector>

using namespace std;

struct GradientDescentResult
{
    long double finalX;
    long double finalValue;
    int iterations;
    bool converged;
};

long double evaluatePolynomial(
    const vector<long double>& coefficients,
    long double x
);

long double evaluateDerivative(
    const vector<long double>& coefficients,
    long double x
);

GradientDescentResult gradientDescent(
    const vector<long double>& coefficients,
    long double initialX,
    long double learningRate,
    long double tolerance,
    int maxIterations
);

#endif
