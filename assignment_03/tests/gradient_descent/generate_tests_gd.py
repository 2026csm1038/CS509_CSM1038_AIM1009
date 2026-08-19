#!/usr/bin/env python3


from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent


# Each entry: (filename, degree, coefficients, initial_x, learning_rate,
#              tolerance, max_iterations, expected_x_star)
# Coefficients are in ascending power order: c0, c1, c2, ..., cd.
TEST_CASES = [
    (
        "gd_01.txt",
        2,
        [9, -6, 1],                                   # x^2 - 6x + 9
        0,
        0.10,
        "1e-6",
        5000,
        3,
    ),
    (
        "gd_02.txt",
        4,
        [0, 0, 2, 0, 1],                               # x^4 + 2x^2
        2,
        0.02,
        "1e-6",
        10000,
        0,
    ),
    (
        "gd_03.txt",
        6,
        [0, 0, 1, 0, 0.5, 0, 0.1],                      # 0.1x^6 + 0.5x^4 + x^2
        2,
        0.02,
        "1e-6",
        20000,
        0,
    ),
    (
        "gd_04.txt",
        8,
        [0, 0, 1, 0, 0.2, 0, 0.05, 0, 0.01],            # 0.01x^8 + 0.05x^6 + 0.2x^4 + x^2
        2,
        0.01,
        "1e-8",
        50000,
        0,
    ),
    (
        "gd_05.txt",
        10,
        [0, 0, 1, 0, 0.2, 0, 0.05, 0, 0.01, 0, 0.002],  # 0.002x^10 + 0.01x^8 + 0.05x^6 + 0.2x^4 + x^2
        2,
        0.005,
        "1e-10",
        100000,
        0,
    ),
]


def format_coefficient(c):
    # Keep integers looking like integers (0, not 0.0) and floats as-is.
    if isinstance(c, float) and c.is_integer():
        c = int(c)
    return str(c)


def write_test(filename, degree, coefficients, initial_x, learning_rate,
               tolerance, max_iterations, expected_x_star):
    assert len(coefficients) == degree + 1, (
        f"{filename}: expected {degree + 1} coefficients, got {len(coefficients)}"
    )

    path = OUTPUT_DIR / filename
    coeff_str = " ".join(format_coefficient(c) for c in coefficients)

    with open(path, "w") as f:
        f.write(f"DEGREE {degree}\n")
        f.write(f"COEFFICIENTS {coeff_str}\n")
        f.write(f"INITIAL_X {initial_x}\n")
        f.write(f"LEARNING_RATE {learning_rate}\n")
        f.write(f"TOLERANCE {tolerance}\n")
        f.write(f"MAX_ITERATIONS {max_iterations}\n")

    print(
        f"Generated {filename}: degree={degree}, x0={initial_x}, "
        f"rate={learning_rate}, tol={tolerance}, max_iter={max_iterations}, "
        f"expected x*={expected_x_star}"
    )


if __name__ == "__main__":
    for case in TEST_CASES:
        write_test(*case)
