import json
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import heapq
import random
import numpy as np

with open('data.json', 'r') as file:
    json_data = json.load(file)

with open('crime_data.json', 'r') as file:
    crime_data = json.load(file)

def crime_density(node):
    node_lat, node_lng = node
    crime_count = 0
    threshold_distance = 1000  # meters 

    for crime in crime_data:
        if "latitude" in crime and "longitude" in crime:
            crime_lat = float(crime["latitude"])
            crime_lng = float(crime["longitude"])
            crime_location = (crime_lat, crime_lng)
            if geodesic(node, crime_location).meters <= threshold_distance:
                crime_count += 1
        elif "lat_lon" in crime and "coordinates" in crime["lat_lon"]:
            coordinates = crime["lat_lon"]["coordinates"]
            crime_lat = float(coordinates[1])
            crime_lng = float(coordinates[0])
            crime_location = (crime_lat, crime_lng)
            if geodesic(node, crime_location).meters <= threshold_distance:
                crime_count += 1

    return crime_count

def compute_heuristic(current, goal):
    distance_heuristic = geodesic(current, goal).meters
    crime_heuristic = crime_density(current) * 100  # Heavily penalize crime-dense areas
    return distance_heuristic + crime_heuristic


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

# A* Search Algorithm
def a_star_search(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    reached = {start: {"cost": 0, "parent": None}}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = compute_heuristic(start, goal)

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
            current_edge_weight = graph[current][neighbor]['weight']
            tentative_g_score = g_score[current] + current_edge_weight

            if neighbor not in reached or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                h_score = compute_heuristic(neighbor, goal)
                f_score[neighbor] = tentative_g_score + h_score
                reached[neighbor] = {"cost": tentative_g_score, "parent": current}
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, float('inf')  # No path found

def visualize_graph(graph, path, title, ax):
    pos = nx.spring_layout(graph, seed=42)
    edge_labels = nx.get_edge_attributes(graph, 'weight')

    node_colors = ['green' if node in path else 'skyblue' for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color=node_colors, edge_color='gray', arrows=True, ax=ax)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d:.2f}m" for (u, v, d) in graph.edges(data='weight')}, font_size=8, ax=ax)
    ax.set_title(title)

def find_best_routes(json_data):
    num_routes = len(json_data["routes"])
    fig, axes = plt.subplots(1, num_routes, figsize=(15, 5))
    axes = np.atleast_1d(axes)

    best_route_index = -1
    min_score = float('inf')
    best_route_summary = ""
    best_route = None

    for route_index, route in enumerate(json_data["routes"]):
        G, start_node, goal_node = build_graph_for_route(route)
        path, total_f_score = a_star_search(G, start_node, goal_node)

        if path:
            total_distance = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
            total_crime = sum(crime_density(node) for node in path)
        else:
            total_distance = float('inf')
            total_crime = float('inf')
            total_f_score = float('inf')

        visualize_graph(G, path, f"Route {route_index + 1}\nDistance: {total_distance:.2f}m\nCrime: {total_crime}\nTotal f_score: {total_f_score:.2f}", axes[route_index])

        print(f"Route {route_index + 1}: Distance = {total_distance:.2f} meters, Crime Density = {total_crime}, f_score = {total_f_score:.2f}")

        if total_f_score < min_score:
            best_route_index = route_index
            best_route = route
            min_score = total_f_score
            best_route_summary = f"Best Route: {route_index + 1} | Distance: {total_distance:.2f}m | Crime: {total_crime} | Total f_score: {total_f_score:.2f}"
    
    print("\n" + best_route_summary)
    plt.show()

# Run the visualization
find_best_routes(json_data)


# Using classes
# Example usage
# if __name__ == "__main__":
#     with open('data.json', 'r') as file:
#         json_data = json.load(file)

#     with open('crime_data.json', 'r') as file:
#         crime_data = json.load(file)

#     planner = RoutePlanner(crime_data)
#     planner.find_best_routes(json_data)