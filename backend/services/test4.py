import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import json

def create_graph_and_plot_routes_simple(data):
    route_graphs = []

    for route_index, route in enumerate(data["routes"]):
        graph = nx.DiGraph()
        pos = {}  # Position for each node to visualize in the plot
        previous_node = None

        for leg in route["legs"]:
            for step_index, step in enumerate(leg["steps"]):
                start_coords = (
                    round(step["startLocation"]["latLng"]["latitude"], 5),
                    round(step["startLocation"]["latLng"]["longitude"], 5)
                )
                end_coords = (
                    round(step["endLocation"]["latLng"]["latitude"], 5),
                    round(step["endLocation"]["latLng"]["longitude"], 5)
                )

                # Calculate geodesic distance between start and end coordinates
                step_distance = geodesic(start_coords, end_coords).meters

                # Define unique node labels
                start_node = (start_coords[0], start_coords[1], f"step_{step_index}_start_{route_index}")
                end_node = (end_coords[0], end_coords[1], f"step_{step_index}_end_{route_index}")

                # Prevent self-loops and zero-length edges
                if start_coords != end_coords:
                    graph.add_node(start_node)
                    graph.add_node(end_node)

                    # Add edge only if start and end coordinates are not the same, and prevent consecutive identical nodes
                    if previous_node is None or (previous_node[:2] != start_coords):
                        graph.add_edge(start_node, end_node, weight=step_distance)

                    # Connect to the previous node if it exists and is not the same as the current start node
                    if previous_node and previous_node != start_node:
                        graph.add_edge(previous_node, start_node, weight=0)  # Smooth connection

                    # Store positions for visualization
                    pos[start_node] = (start_coords[1], start_coords[0])  # (lon, lat)
                    pos[end_node] = (end_coords[1], end_coords[0])  # (lon, lat)

                    # Update previous node
                    previous_node = end_node
                else:
                    # Update previous node when start == end to avoid orphan nodes
                    previous_node = start_node

        # Store graph and visualize
        route_graphs.append(graph)

        # Plotting the graph using spring layout to avoid curved paths
        plt.figure(figsize=(8, 6))
        layout = nx.spring_layout(graph, seed=42)  # Spread out nodes nicely
        nx.draw(graph, layout, with_labels=True, node_size=50, font_size=6, node_color='skyblue', edge_color='gray')
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, layout, edge_labels={k: f"{v:.1f}m" for k, v in labels.items()}, font_size=5)
        plt.title(f"Graph for Route {route_index + 1}")
        plt.show()

# Load and process data
with open('data.json', 'r') as file:
    data = json.load(file)
    create_graph_and_plot_routes_simple(data)
