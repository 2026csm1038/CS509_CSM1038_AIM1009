#!/usr/bin/env python3

import random
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent


# Each entry: (filename, n, k, dimension, seed)
#
# Points are generated in a small Euclidean "hidden" space and the
# pairwise distance matrix is computed from them. This guarantees the
# matrix is symmetric, has a zero diagonal, and satisfies the triangle
# inequality (a genuine metric), which the driver validates on load.
#
# The hidden dimension is unrelated to the FastMap target dimension k;
# it only exists to produce a realistic, well-behaved distance matrix.
TEST_CASES = [
    ("fm_01.txt", 10, 2, 3, 1),
    ("fm_02.txt", 100, 2, 5, 2),
    ("fm_03.txt", 1000, 3, 8, 3),
    ("fm_04.txt", 10000, 3, 8, 4),
    
    # ("fm_05.txt", 50000, 3, 8, 5),
]


def make_points(n, dimension, seed):
    """
    Generate n random points in the given hidden dimension.
    """
    rng = random.Random(seed)

    return [
        [rng.uniform(-100.0, 100.0) for _ in range(dimension)]
        for _ in range(n)
    ]


def euclidean_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def write_fastmap_test(filename, n, k, dimension, seed):
    """
    Write a FastMap input file: N K header followed by the full
    N x N symmetric distance matrix with a zero diagonal.

    Rows are written incrementally so only the O(N * dimension)
    point array is held in memory, not the O(N^2) distance matrix.
    """
    points = make_points(n, dimension, seed)

    path = OUTPUT_DIR / filename

    with path.open("w") as file:
        file.write(f"{n} {k}\n")

        for i in range(n):
            row = []

            for j in range(n):
                if i == j:
                    row.append("0.000000")
                else:
                    row.append(f"{euclidean_distance(points[i], points[j]):.6f}")

            file.write(" ".join(row) + "\n")


def main():
    for filename, n, k, dimension, seed in TEST_CASES:
        print(f"Generating {filename}: N={n}, k={k} ...")
        write_fastmap_test(filename, n, k, dimension, seed)

    print("Done.")


if __name__ == "__main__":
    main()