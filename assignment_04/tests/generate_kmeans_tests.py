import os
import random
import math

OUTPUT_DIR = "assignment_04/tests/kmeans"


def write_test(filename, points, k, max_iterations=300, tolerance=0.0001):
    path = os.path.join(OUTPUT_DIR, filename)

    n = len(points)
    d = len(points[0])

    with open(path, "w") as f:
        f.write(f"{n} {d} {k}\n")

        for point in points:
            f.write(" ".join(f"{x:.6f}" for x in point) + "\n")

        f.write(f"MAX_ITERATIONS {max_iterations}\n")
        f.write(f"TOLERANCE {tolerance}\n")

    print(f"Created {path}  (N={n}, D={d}, K={k})")


def generate_clustered_points(n, d, k, seed):
    random.seed(seed)

    points = []

    # Generate well-separated cluster centers.
    centers = []

    for c in range(k):
        center = []

        for j in range(d):
            center.append((c + 1) * 10.0 + j * 2.0)

        centers.append(center)

    # Generate points around the centers.
    for i in range(n):
        cluster = i % k

        point = []

        for j in range(d):
            value = centers[cluster][j] + random.gauss(0, 1.5)
            point.append(value)

        points.append(point)

    return points


def generate_uniform_points(n, d, seed):
    random.seed(seed)

    points = []

    for _ in range(n):
        point = []

        for _ in range(d):
            point.append(random.uniform(-100, 100))

        points.append(point)

    return points


def generate_identical_points(n, d):
    return [[5.0 for _ in range(d)] for _ in range(n)]


def generate_duplicate_points():
    return [
        [1.0, 1.0],
        [1.0, 1.0],
        [2.0, 2.0],
        [2.0, 2.0],
        [10.0, 10.0],
        [10.0, 10.0],
        [20.0, 20.0],
        [20.0, 20.0],
    ]


def generate_collinear_points(n):
    points = []

    for i in range(n):
        points.append([
            float(i),
            float(2 * i)
        ])

    return points


def generate_empty_cluster_case():
    # K=3 but the first three centroids are deliberately
    # very close to the same region.
    return [
        [0.0, 0.0],
        [0.1, 0.1],
        [0.2, 0.2],

        [10.0, 10.0],
        [10.2, 9.9],
        [9.8, 10.1],

        [20.0, 20.0],
        [20.2, 20.1],
        [19.8, 19.9],
    ]


def generate_invalid_tests():
    # Invalid N
    path = os.path.join(OUTPUT_DIR, "km_invalid_n.txt")

    with open(path, "w") as f:
        f.write("-5 2 2\n")

    # Invalid D
    path = os.path.join(OUTPUT_DIR, "km_invalid_d.txt")

    with open(path, "w") as f:
        f.write("5 0 2\n")

    # Invalid K = 0
    path = os.path.join(OUTPUT_DIR, "km_invalid_k_zero.txt")

    with open(path, "w") as f:
        f.write("5 2 0\n")

    # K > N
    path = os.path.join(OUTPUT_DIR, "km_invalid_k_large.txt")

    with open(path, "w") as f:
        f.write("3 2 5\n")

    # Invalid tolerance
    path = os.path.join(OUTPUT_DIR, "km_invalid_tolerance.txt")

    with open(path, "w") as f:
        f.write("3 2 2\n")
        f.write("0 0\n")
        f.write("1 1\n")
        f.write("2 2\n")
        f.write("MAX_ITERATIONS 100\n")
        f.write("TOLERANCE -0.001\n")

    # Invalid max iterations
    path = os.path.join(OUTPUT_DIR, "km_invalid_iterations.txt")

    with open(path, "w") as f:
        f.write("3 2 2\n")
        f.write("0 0\n")
        f.write("1 1\n")
        f.write("2 2\n")
        f.write("MAX_ITERATIONS 0\n")
        f.write("TOLERANCE 0.0001\n")

    print("Created invalid K-Means tests.")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ---------------------------------------------------------
    # REQUIRED TESTS FROM ASSIGNMENT
    # ---------------------------------------------------------

    # km_01: N=100, D=2, K=3
    points = generate_clustered_points(
        n=100,
        d=2,
        k=3,
        seed=101
    )

    write_test(
        "km_01.txt",
        points,
        k=3,
        max_iterations=300,
        tolerance=0.0001
    )

    # km_02: N=1000, D=2, K=5
    points = generate_clustered_points(
        n=1000,
        d=2,
        k=5,
        seed=102
    )

    write_test(
        "km_02.txt",
        points,
        k=5,
        max_iterations=300,
        tolerance=0.0001
    )

    # km_03: N=10000, D=5, K=8
    points = generate_clustered_points(
        n=10000,
        d=5,
        k=8,
        seed=103
    )

    write_test(
        "km_03.txt",
        points,
        k=8,
        max_iterations=300,
        tolerance=0.0001
    )

    # km_04: N=100000, D=5, K=10
    points = generate_clustered_points(
        n=100000,
        d=5,
        k=10,
        seed=104
    )

    write_test(
        "km_04.txt",
        points,
        k=10,
        max_iterations=300,
        tolerance=0.0001
    )

    # ---------------------------------------------------------
    # EDGE CASES
    # ---------------------------------------------------------

    # Smallest meaningful case: K = N
    points = [
        [0.0, 0.0],
        [10.0, 10.0],
    ]

    write_test(
        "km_two_points.txt",
        points,
        k=2
    )

    # All points identical
    points = generate_identical_points(10, 2)

    write_test(
        "km_identical.txt",
        points,
        k=3
    )

    # Duplicate points
    points = generate_duplicate_points()

    write_test(
        "km_duplicates.txt",
        points,
        k=4
    )

    # Collinear data
    points = generate_collinear_points(20)

    write_test(
        "km_collinear.txt",
        points,
        k=3
    )

    # Empty-cluster situation
    points = generate_empty_cluster_case()

    write_test(
        "km_empty_cluster.txt",
        points,
        k=3
    )

    # Negative coordinates
    points = [
        [-10.0, -10.0],
        [-9.0, -11.0],
        [-8.0, -9.0],
        [10.0, 10.0],
        [11.0, 9.0],
        [9.0, 11.0],
    ]

    write_test(
        "km_negative_coordinates.txt",
        points,
        k=2
    )

    # Higher dimensional small test
    points = generate_uniform_points(
        n=50,
        d=10,
        seed=200
    )

    write_test(
        "km_high_dimension.txt",
        points,
        k=5
    )

    # ---------------------------------------------------------
    # INVALID INPUT TESTS
    # ---------------------------------------------------------

    generate_invalid_tests()

    print("\nAll K-Means tests generated.")


if __name__ == "__main__":
    main()
