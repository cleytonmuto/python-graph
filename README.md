Python Grid Graph Visualizer
============================

This project builds and visualizes a **weighted, directed 2D grid graph** using Python.

By default it creates a **6×6 grid** where:

- **Nodes**: arranged as a square grid in grayscale filled circles.
- **Edges**: connect horizontally (left → right) and vertically (top → down).
- **Weights**: random integers between 1 and 10, displayed near each edge.

Running the script generates four PNG images:

- **`square_graph.png`**: full grid with all directed edges (with arrows).
- **`square_graph_no_arrows.png`**: same grid, but edges without arrow tips.
- **`square_graph_dijkstra.png`**: grid where the **Dijkstra shortest path** from the top‑left node to the bottom‑right node is highlighted in bold.
- **`square_graph_mst.png`**: grid where a **minimum spanning tree (Kruskal)** is highlighted in bold (edges shown without arrows).

## Setup

1. (Optional) Create and activate a virtual environment.
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

From the project root:

```bash
python main.py
```

This will generate the PNG files listed above in the same directory. You can adjust the grid size by changing the default arguments of `build_square_graph` in `main.py`.

