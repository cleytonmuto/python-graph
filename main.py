import random

import matplotlib.pyplot as plt
import networkx as nx


def build_square_graph(n_rows: int = 6, n_cols: int = 6) -> nx.DiGraph:
    """
    Build a directed grid graph (n_rows x n_cols) with random edge weights.

    - Nodes are numbered from 0 to n_rows * n_cols - 1.
    - Layout is a grid:
        row 0 is the top row, row n_rows-1 is the bottom row.
        column 0 is the leftmost column, column n_cols-1 is the rightmost.
    - Directed edges:
        - Horizontal edges: left -> right
        - Vertical edges: top -> down
    """
    g = nx.DiGraph()

    # Add all vertices
    num_nodes = n_rows * n_cols
    g.add_nodes_from(range(num_nodes))

    def idx(r: int, c: int) -> int:
        return r * n_cols + c

    # Add directed edges between horizontally and vertically adjacent nodes
    for r in range(n_rows):
        for c in range(n_cols):
            u = idx(r, c)

            # Horizontal: left -> right
            if c < n_cols - 1:
                v = idx(r, c + 1)
                weight = random.randint(1, 10)
                g.add_edge(u, v, weight=weight)

            # Vertical: top -> down
            if r < n_rows - 1:
                v = idx(r + 1, c)
                weight = random.randint(1, 10)
                g.add_edge(u, v, weight=weight)

    # Store grid shape on the graph for drawing
    g.graph["n_rows"] = n_rows
    g.graph["n_cols"] = n_cols

    return g


def draw_graph(
    g: nx.DiGraph,
    output_path: str = "square_graph.png",
    highlight_edges: set[tuple[int, int]] | None = None,
    use_arrows: bool = True,
) -> None:
    """Draw the directed, weighted graph as a square and save to an image file.

    Requirements:
    - Filled circular vertices
    - Straight edges
    - Arrow tip gently touching the circle (not covered by the node)
    - Edge weights placed just outside the edge, text not rotated
    """
    # Grid layout based on stored dimensions
    n_rows = g.graph.get("n_rows", 6)
    n_cols = g.graph.get("n_cols", 6)

    # Map node index -> (x, y) in data coords
    pos: dict[int, tuple[float, float]] = {}
    for n in g.nodes():
        r = n // n_cols
        c = n % n_cols
        # x increases to the right, y decreases downward; we want top row to have highest y
        x = float(c)
        y = float((n_rows - 1) - r)
        pos[n] = (x, y)

    # Increase figure size by ~20% so nodes and labels have more room
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.axis("off")

    # Add a small margin so circles are fully visible (not cut off)
    margin = 0.2
    max_x = float(n_cols - 1)
    max_y = float(n_rows - 1)
    ax.set_xlim(-margin, max_x + margin)
    ax.set_ylim(-margin, max_y + margin)

    # Radius of nodes in data coordinates (slightly larger so circles are more visible)
    node_radius = 0.12

    # Draw filled nodes (circles) without inner values
    for n, (x, y) in pos.items():
        circle = plt.Circle(
            (x, y),
            radius=node_radius,
            facecolor="lightgray",
            edgecolor="black",
            linewidth=1.5,
            zorder=2,
        )
        ax.add_patch(circle)

    # Draw edges (optionally with arrow tips) touching the circle
    # Slightly smaller offset so labels sit closer to edges
    label_offset = 0.2

    highlight_edges = highlight_edges or set()

    for u, v, data in g.edges(data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]

        dx = x2 - x1
        dy = y2 - y1
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length == 0:
            continue

        ux = dx / length
        uy = dy / length

        # Start/end just outside the node circles
        start_x = x1 + ux * node_radius
        start_y = y1 + uy * node_radius
        end_x = x2 - ux * node_radius
        end_y = y2 - uy * node_radius

        # Choose style: highlighted edges are thicker and darker
        if (u, v) in highlight_edges:
            edge_color = "black"
            edge_width = 2.8
            edge_zorder = 5
        else:
            edge_color = "gray"
            edge_width = 1.5
            edge_zorder = 4

        if use_arrows:
            # Draw arrow (above nodes so tip is visible)
            ax.annotate(
                "",
                xy=(end_x, end_y),
                xytext=(start_x, start_y),
                arrowprops=dict(
                    arrowstyle="->",
                    color=edge_color,
                    linewidth=edge_width,
                    mutation_scale=20,  # slightly larger arrow tip
                    shrinkA=0,
                    shrinkB=0,
                ),
                zorder=edge_zorder,
            )
        else:
            # Draw plain straight line (no arrowheads)
            ax.plot(
                [start_x, end_x],
                [start_y, end_y],
                color=edge_color,
                linewidth=edge_width,
                zorder=edge_zorder,
            )

        # Compute label position slightly outside the edge
        mid_x = (start_x + end_x) / 2.0
        mid_y = (start_y + end_y) / 2.0

        label_x, label_y = mid_x, mid_y

        # Standard notation for label placement:
        # - Horizontal edges: labels above (top-sided)
        # - Vertical edges: labels to the left (left-sided)
        if abs(dy) < 1e-6:
            # Horizontal edge -> move label upward
            label_y += label_offset
        elif abs(dx) < 1e-6:
            # Vertical edge -> move label left
            label_x -= label_offset

        weight = data.get("weight")
        ax.text(
            label_x,
            label_y,
            str(weight),
            fontsize=10,
            color="dimgray",
            ha="center",
            va="center",
            rotation=0,  # keep text upright (no rotation)
            zorder=5,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    g = build_square_graph()

    # Base grid image with arrows
    base_file = "square_graph.png"
    draw_graph(g, base_file, use_arrows=True)
    print(f"Base graph saved to {base_file}")

    # Additional base image without arrow tips
    base_no_arrows_file = "square_graph_no_arrows.png"
    draw_graph(g, base_no_arrows_file, use_arrows=False)
    print(f"Base graph without arrows saved to {base_no_arrows_file}")

    # Dijkstra shortest path from top-left (0) to bottom-right (last node)
    n_rows = g.graph["n_rows"]
    n_cols = g.graph["n_cols"]
    source = 0
    target = n_rows * n_cols - 1

    try:
        dijkstra_path = nx.shortest_path(g, source=source, target=target, weight="weight")
        dijkstra_edges: set[tuple[int, int]] = set(
            (dijkstra_path[i], dijkstra_path[i + 1]) for i in range(len(dijkstra_path) - 1)
        )
    except nx.NetworkXNoPath:
        dijkstra_edges = set()

    dijkstra_file = "square_graph_dijkstra.png"
    # Keep arrows on the Dijkstra shortest path image
    draw_graph(g, dijkstra_file, highlight_edges=dijkstra_edges, use_arrows=True)
    print(f"Dijkstra shortest-path graph saved to {dijkstra_file}")

    # Minimum spanning tree using Kruskal on the undirected version
    undirected = g.to_undirected()
    mst = nx.minimum_spanning_tree(undirected, weight="weight")

    mst_edges: set[tuple[int, int]] = set()
    for u, v in mst.edges():
        if g.has_edge(u, v):
            mst_edges.add((u, v))
        elif g.has_edge(v, u):
            mst_edges.add((v, u))

    mst_file = "square_graph_mst.png"
    # MST image without arrow tips
    draw_graph(g, mst_file, highlight_edges=mst_edges, use_arrows=False)
    print(f"Kruskal MST graph saved to {mst_file}")


if __name__ == "__main__":
    main()

