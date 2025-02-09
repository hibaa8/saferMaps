# import json
# import networkx as nx
# from geopy.distance import geodesic
# import matplotlib.pyplot as plt
# import heapq
# import numpy as np

# with open('data.json', 'r') as file:
#     json_data = json.load(file)

# def get_edge_weight(start, end, static_duration=None, travel_mode=None):
#     base_distance = geodesic(start, end).meters
    
#     if travel_mode == "WALK":
#         mode_penalty = 0.8 
#     elif travel_mode == "TRANSIT":
#         mode_penalty = 1  
#     else:
#         mode_penalty = 1.0  # Default penalty

#     duration_penalty = 0
#     if static_duration:
#         duration_penalty = float(static_duration[:-1]) / 60.0 # minutes

#     return base_distance * mode_penalty + duration_penalty

# def build_graph_for_route(route):
#     """Build a graph for a specific route."""
#     G = nx.DiGraph() 

#     start_node = (route["legs"][0]["startLocation"]["latLng"]["latitude"],
#                   route["legs"][0]["startLocation"]["latLng"]["longitude"])
#     previous_node = start_node
#     G.add_node(start_node)

#     for leg in route["legs"]:
#         for step in leg["steps"]:
#             end_lat = step["endLocation"]["latLng"]["latitude"]
#             end_lng = step["endLocation"]["latLng"]["longitude"]
#             end_node = (end_lat, end_lng)

#             weight = get_edge_weight(
#                 previous_node, end_node,
#                 static_duration=step.get("staticDuration", "0s"),
#                 travel_mode=step.get("travelMode", None)
#             )
            
#             G.add_edge(previous_node, end_node, weight=weight)
#             previous_node = end_node

#     goal_node = previous_node  
#     return G, start_node, goal_node

# def a_star_search(graph, start, goal):
#     """A* search algorithm to find the shortest path."""
#     open_set = []
#     heapq.heappush(open_set, (0, start))
#     came_from = {}
#     g_score = {node: float('inf') for node in graph.nodes}
#     g_score[start] = 0
#     f_score = {node: float('inf') for node in graph.nodes}
#     f_score[start] = geodesic(start, goal).meters

#     while open_set:
#         _, current = heapq.heappop(open_set)

#         if current == goal:
#             path = []
#             while current in came_from:
#                 path.append(current)
#                 current = came_from[current]
#             path.append(start)
#             return path[::-1]

#         for neighbor in graph.neighbors(current):
#             tentative_g_score = g_score[current] + graph[current][neighbor]['weight']

#             if tentative_g_score < g_score[neighbor]:
#                 came_from[neighbor] = current
#                 g_score[neighbor] = tentative_g_score
#                 f_score[neighbor] = tentative_g_score + geodesic(neighbor, goal).meters
#                 if neighbor not in [n[1] for n in open_set]:
#                     heapq.heappush(open_set, (f_score[neighbor], neighbor))

#     return None  

# def visualize_graph(graph, path, title, ax):
#     """Visualize the given graph and highlight the optimal path."""
#     pos = nx.spring_layout(graph, seed=42)  
#     edge_labels = nx.get_edge_attributes(graph, 'weight')

#     node_colors = ['green' if node in path else 'skyblue' for node in graph.nodes]
#     nx.draw(graph, pos, with_labels=True, node_size=700, node_color=node_colors, edge_color='gray', arrows=True, ax=ax)
#     nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d:.2f}m" for (u, v, d) in graph.edges(data='weight')}, font_size=8, ax=ax)
#     ax.set_title(title)

# def find_best_route_and_visualize(json_data):
#     best_route_index = -1
#     best_route_cost = float('inf')
#     best_route_path = None
#     best_graph = None

#     num_routes = len(json_data["routes"])
#     fig, axes = plt.subplots(1, num_routes, figsize=(15, 5))
#     axes = np.atleast_1d(axes)  

#     for route_index, route in enumerate(json_data["routes"]):
#         G, start_node, goal_node = build_graph_for_route(route)
#         path = a_star_search(G, start_node, goal_node)

#         if path:
#             total_cost = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
#         else:
#             total_cost = float('inf')  

 
#         visualize_graph(G, path, f"Route {route_index + 1} (Cost: {total_cost:.2f}m)", axes[route_index])


#         if total_cost < best_route_cost:
#             best_route_cost = total_cost
#             best_route_path = path
#             best_route_index = route_index
#             best_graph = G

#     print(f"Best route index: {best_route_index}, Cost: {best_route_cost:.2f} meters")
#     print("Best route path:")
#     for step in best_route_path:
#         print(step)

#     plt.show()


# find_best_route_and_visualize(json_data)
