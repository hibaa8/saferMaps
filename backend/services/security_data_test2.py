import json
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import heapq
import random
import numpy as np
from rtree import index

# Preprocess crime data into a spatial index
def preprocess_crime_data(crime_data):
    crime_idx = index.Index()
    for i, crime in enumerate(crime_data):
        lat = float(crime["latitude"])
        lng = float(crime["longitude"])
        # Rtree uses (minx, miny, maxx, maxy)
        crime_idx.add(i, (lng, lat, lng, lat))
    return crime_idx

# Precompute crime density using spatial index
def get_crime_count(node, crime_idx, crime_data, threshold=600):
    lat, lng = node
    # Approximate radius in degrees (1 degree ≈ 111,000 meters)
    radius_deg = threshold / 111000
    min_lat = lat - radius_deg
    max_lat = lat + radius_deg
    min_lng = lng - radius_deg
    max_lng = lng + radius_deg
    
    crime_count = 0
    # Query the spatial index for crimes within the bounding box
    for i in crime_idx.intersection((min_lng, min_lat, max_lng, max_lat)):
        crime = crime_data[i]
        crime_lat = float(crime["latitude"])
        crime_lng = float(crime["longitude"])
        if geodesic((lat, lng), (crime_lat, crime_lng)).meters <= threshold:
            crime_count += 1
    return crime_count

def compute_heuristic(current, goal):
    distance_heuristic = geodesic(current, goal).meters
    crime_heuristic = get_crime_count(current, crime_idx, crime_data) * 100  # Penalize crime-dense areas
    return distance_heuristic + crime_heuristic

# Function to build graph for a specific route
def build_graph_for_route(route):
    G = nx.DiGraph()

    start_node = (route["legs"][0]["startLocation"]["latLng"]["latitude"],
                  route["legs"][0]["startLocation"]["latLng"]["longitude"])
    previous_node = start_node
    G.add_node(start_node)

    for leg in route["legs"]:
        for step in leg["steps"]:
            end_lat = step["endLocation"]["latLng"]["latitude"]
            end_lng = step["endLocation"]["latLng"]["longitude"]
            end_node = (end_lat, end_lng)

            weight = geodesic(previous_node, end_node).meters
            G.add_edge(previous_node, end_node, weight=weight)
            previous_node = end_node

    goal_node = previous_node
    return G, start_node, goal_node

# A* Search Algorithm with priority queue optimizations
def a_star_search(graph, start, goal, crime_idx, crime_data):
    open_set = []
    heapq.heappush(open_set, (0, start))
    reached = {start: {"cost": 0, "parent": None}}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = compute_heuristic(start, goal, crime_idx, crime_data)

    while open_set:
        current_f_score, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            total_path_f_score = 0

            # Backtrack using the reached map to build the path and accumulate f_score
            while current:
                path.append(current)
                total_path_f_score += f_score[current]
                current = reached[current]["parent"]
            return path[::-1], total_path_f_score

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']

            if neighbor not in reached or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                h_score = compute_heuristic(neighbor, goal, crime_idx, crime_data)
                f_score[neighbor] = tentative_g_score + h_score
                reached[neighbor] = {"cost": tentative_g_score, "parent": current}
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, float('inf')  # No path found

# Visualization function
def visualize_graph(graph, path, title, ax):
    pos = nx.spring_layout(graph, seed=42)
    edge_labels = nx.get_edge_attributes(graph, 'weight')

    node_colors = ['green' if node in path else 'skyblue' for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color=node_colors, edge_color='gray', arrows=True, ax=ax)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d:.2f}m" for (u, v, d) in graph.edges(data='weight')}, font_size=8, ax=ax)
    ax.set_title(title)

# Find and visualize the best routes with optimizations
def find_best_routes(json_data, crime_data):
    num_routes = len(json_data["routes"])
    fig, axes = plt.subplots(1, num_routes, figsize=(15, 5))
    axes = np.atleast_1d(axes)

    # Preprocess crime data
    crime_idx = preprocess_crime_data(crime_data)

    best_route_index = -1
    min_score = float('inf')
    best_route_summary = ""

    for route_index, route in enumerate(json_data["routes"]):
        G, start_node, goal_node = build_graph_for_route(route)
        path, total_f_score = a_star_search(G, start_node, goal_node, crime_idx, crime_data)

        if path:
            total_distance = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
            total_crime = sum(get_crime_count(node, crime_idx, crime_data) for node in path)
        else:
            total_distance = float('inf')
            total_crime = float('inf')
            total_f_score = float('inf')

        visualize_graph(G, path, f"Route {route_index + 1}\nDistance: {total_distance:.2f}m\nCrime: {total_crime}\nTotal f_score: {total_f_score:.2f}", axes[route_index])

        print(f"Route {route_index + 1}: Distance = {total_distance:.2f} meters, Crime Density = {total_crime}, f_score = {total_f_score:.2f}")

        if total_f_score < min_score:
            best_route_index = route_index
            min_score = total_f_score
            best_route_summary = f"Best Route: {route_index + 1} | Distance: {total_distance:.2f}m | Crime: {total_crime} | Total f_score: {total_f_score:.2f}"

    print("\n" + best_route_summary)
    plt.show()

# Run the visualization with optimizations
with open('data.json', 'r') as file:
    json_data = json.load(file)

with open('crime_data.json', 'r') as file:
    crime_data = json.load(file)

find_best_routes(json_data, crime_data)