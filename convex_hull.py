import random

import matplotlib.pyplot as plt


def _cross(
    o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]
) -> float:
    """2D cross product of OA and OB vectors (z-component).

    Positive if OAB makes a counter-clockwise turn, negative for clockwise,
    and zero if the points are collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def compute_convex_hull(
    points: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """Compute the convex hull of a set of 2D points using Andrew's monotone chain.

    Returns the hull vertices in counter-clockwise order without repeating
    the first point at the end. If there are fewer than 3 unique points,
    the returned list is the unique points themselves.
    """
    # Remove duplicates and sort lexicographically (by x, then y)
    unique_points = sorted(set(points))
    if len(unique_points) <= 1:
        return unique_points

    # Build lower hull
    lower: list[tuple[float, float]] = []
    for p in unique_points:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper: list[tuple[float, float]] = []
    for p in reversed(unique_points):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper to get full hull; omit last point of each
    # list because it's repeated at the start of the other list.
    return lower[:-1] + upper[:-1]


def draw_points_and_hull(
    points: list[tuple[float, float]],
    show_hull: bool,
    output_path: str,
) -> None:
    """Draw points (and optionally their convex hull) to an image file."""
    if not points:
        raise ValueError("points list must not be empty")

    hull: list[tuple[float, float]] = compute_convex_hull(points) if show_hull else []

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor("white")

    # Plot all points as medium-sized black dots
    xs, ys = zip(*points)
    ax.scatter(xs, ys, s=50, color="black", zorder=2)

    # Draw convex hull polygon if requested and we have at least a triangle
    if show_hull and len(hull) >= 3:
        hx, hy = zip(*hull)
        hx_list = list(hx)
        hy_list = list(hy)
        # Close the polygon by repeating the first point at the end
        hx_list.append(hx_list[0])
        hy_list.append(hy_list[0])

        # Light filled polygon with a solid border
        ax.fill(
            hx_list,
            hy_list,
            facecolor="tab:blue",
            alpha=0.15,
            edgecolor="none",
            zorder=1,
        )
        ax.plot(
            hx_list,
            hy_list,
            color="tab:blue",
            linewidth=2.0,
            zorder=3,
        )

    # Set a small margin around the unit square so points and hull are not clipped
    margin = 0.05
    ax.set_xlim(-margin, 1.0 + margin)
    ax.set_ylim(-margin, 1.0 + margin)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    """Entry point to generate random convex hull visualizations."""
    n_points = 20
    if n_points <= 0:
        raise ValueError("n_points must be positive")

    # Generate a single random point set to use for both images
    points: list[tuple[float, float]] = [
        (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
        for _ in range(n_points)
    ]

    # Image without the solution (points only)
    points_only_file = "convex_hull_points.png"
    draw_points_and_hull(points, show_hull=False, output_path=points_only_file)
    print(f"Convex hull (points only) graph saved to {points_only_file}")

    # Image with the convex hull solution
    hull_file = "convex_hull.png"
    draw_points_and_hull(points, show_hull=True, output_path=hull_file)
    print(f"Convex hull (with solution) graph saved to {hull_file}")


if __name__ == "__main__":
    main()

