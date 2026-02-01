#!/usr/bin/env python3
"""
Graph Visualization for Numbo - Shows support network visually

Requires matplotlib for visualization.
"""

import matplotlib.pyplot as plt
import networkx as nx
from Numbo1 import Numbo, SeqCanvas, SeqState, Want, Consume, ImCell
from FARGish2 import FARGModel

def visualize_support_graph(fm: FARGModel, filename='numbo_graph.png'):
    """
    Create a visual graph of the support network.

    Nodes are colored by type:
    - Want: red (goal)
    - ImCell: green (completed operations)
    - Consume: blue (proposed operations)
    - Canvas: yellow (workspace states)

    Edge thickness shows support strength.
    """
    G = nx.DiGraph()

    # Track node types for coloring
    node_colors = {}
    node_labels = {}

    # Add nodes
    for elem in fm.elems():
        node_id = str(elem)[:40]  # Truncate for readability
        G.add_node(node_id)
        node_labels[node_id] = node_id

        # Color by type
        if isinstance(elem, Want):
            node_colors[node_id] = 'red'
        elif isinstance(elem, ImCell):
            node_colors[node_id] = 'lightgreen'
        elif isinstance(elem, Consume):
            node_colors[node_id] = 'lightblue'
        elif isinstance(elem, SeqCanvas):
            node_colors[node_id] = 'yellow'
        else:
            node_colors[node_id] = 'lightgray'

    # Add edges (support links)
    for elem in fm.elems():
        elem_id = str(elem)[:40]
        for neighbor in fm.neighbors(elem):
            neighbor_id = str(neighbor)[:40]
            if G.has_node(neighbor_id):
                # Edge weight is activation
                weight = fm.a(neighbor)
                G.add_edge(elem_id, neighbor_id, weight=weight)

    # Create visualization
    plt.figure(figsize=(16, 12))
    plt.title(f'Numbo Support Network (t={fm.t})', fontsize=16, fontweight='bold')

    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Draw nodes
    colors = [node_colors.get(n, 'lightgray') for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=800, alpha=0.9)

    # Draw labels
    nx.draw_networkx_labels(G, pos, node_labels, font_size=7)

    # Draw edges with varying thickness based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w*2 for w in weights],
                           alpha=0.5, arrows=True, arrowsize=10)

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red',
                   markersize=10, label='Goal (Want)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen',
                   markersize=10, label='Completed (ImCell)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue',
                   markersize=10, label='Proposed (Consume)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow',
                   markersize=10, label='Workspace (Canvas)'),
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.axis('off')
    plt.tight_layout()

    # Save to file
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nGraph saved to {filename}")

    # Show if running interactively
    plt.show()

def run_and_visualize(timesteps=10, seed=None):
    """Run Numbo for N timesteps and visualize the support graph"""
    print("Setting up Numbo problem: (4, 5, 6) → 15")

    fm = Numbo(seed=seed)
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print(f"Running for {timesteps} timesteps...\n")

    for i in range(timesteps):
        fm.do_timestep()
        print(f"Timestep {fm.t} complete")

    print(f"\nAfter {timesteps} timesteps:")
    print(f"  - Total elements: {len(list(fm.elems()))}")
    print(f"  - Consume agents: {len(list(fm.elems(Consume)))}")
    print(f"  - Operations done: {len(list(fm.elems(ImCell)))}")

    # Show completed operations
    cells = list(fm.elems(ImCell))
    if cells:
        print(f"\nCompleted operations:")
        for cell in cells:
            print(f"  • {cell}")

    print("\nGenerating visualization...")
    visualize_support_graph(fm, f'numbo_graph_t{timesteps}.png')

if __name__ == '__main__':
    import sys

    timesteps = 10
    if len(sys.argv) > 1:
        try:
            timesteps = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [timesteps]")
            sys.exit(1)

    run_and_visualize(timesteps=timesteps, seed=23686273699696067)
