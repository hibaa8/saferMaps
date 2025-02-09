import heapq
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import numpy as np
from .RouteGraph import RouteGraph


class RoutePlanner:
    def __init__(self, crime_data):
        self.crime_data = crime_data

    def get_crime_coordinates(self, crime):
        if "latitude" in crime and "longitude" in crime:
            return float(crime["latitude"]), float(crime["longitude"])
        if "lat_lon" in crime and "coordinates" in crime["lat_lon"]:
            coordinates = crime["lat_lon"]["coordinates"]
            return float(coordinates[1]), float(coordinates[0])
        if "geocoded_column" in crime and "coordinates" in crime["geocoded_column"]:
            coordinates = crime["geocoded_column"]["coordinates"]
            return float(coordinates[1]), float(coordinates[0])
        return None

    def crime_density(self, node):
        node_lat, node_lng = node
        crime_count = 0
        threshold_distance = 1000  # meters

        for crime in self.crime_data:
            crime_coords = self.get_crime_coordinates(crime)
            if crime_coords:
                crime_lat, crime_lng = crime_coords
                crime_location = (crime_lat, crime_lng)
                if geodesic(node, crime_location).meters <= threshold_distance:
                    crime_count += 1

        return crime_count

    def compute_heuristic(self, current, goal):
        distance_heuristic = geodesic(current, goal).meters
        crime_heuristic = self.crime_density(current) * 100  # Heavily penalize crime-dense areas
        return distance_heuristic + crime_heuristic

    def a_star_search(self, graph, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        reached = {start: {"cost": 0, "parent": None}}
        g_score = {node: float('inf') for node in graph.nodes}
        g_score[start] = 0
        f_score = {node: float('inf') for node in graph.nodes}
        f_score[start] = self.compute_heuristic(start, goal)

        while open_set:
            current_f_score, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                total_path_f_score = 0

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
                    h_score = self.compute_heuristic(neighbor, goal)
                    f_score[neighbor] = tentative_g_score + h_score
                    reached[neighbor] = {"cost": tentative_g_score, "parent": current}
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None, float('inf')  # No path found

    def visualize_graph(self, graph, path, title, ax):
        pos = nx.spring_layout(graph, seed=42)
        edge_labels = nx.get_edge_attributes(graph, 'weight')

        node_colors = ['green' if node in path else 'skyblue' for node in graph.nodes]
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color=node_colors, edge_color='gray', arrows=True, ax=ax)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d:.2f}m" for (u, v, d) in graph.edges(data='weight')}, font_size=8, ax=ax)
        ax.set_title(title)

    def find_best_routes(self, json_data):
        route_scores = []
        # for route_index, route in enumerate(json_data["routes"]):
        #     route_graph = RouteGraph(route)
        #     path, total_f_score = self.a_star_search(route_graph.graph, route_graph.start_node, route_graph.goal_node)
        #     if path:
        #         total_distance = sum(route_graph.graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        #         total_crime = sum(self.crime_density(node) for node in path)
        #     else:
        #         total_distance = total_crime = total_f_score = float('inf')
        #     route_scores.append((route_index, path, total_distance, total_crime, total_f_score, route_graph.graph))
        for route_index, route in enumerate(json_data["routes"]):
            route_graph = RouteGraph(route)
            path, total_f_score = self.a_star_search(route_graph.graph, route_graph.start_node, route_graph.goal_node)
            
            if path:
                total_distance = sum(route_graph.graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
                total_crime = sum(self.crime_density(node) for node in path)
            else:
                total_distance = total_crime = total_f_score = float('inf')

            # Store route index and f_score
            route_scores.append((route_index, total_f_score))

        # Sort routes by f_score and get the indices of the best 2
        sorted_route_indices = [route_index for route_index, _ in sorted(route_scores, key=lambda x: x[1])[:2]]

        # Retrieve the original routes corresponding to the best 2 indices
        best_routes = [json_data["routes"][index] for index in sorted_route_indices]

        return best_routes
            # Append route details to route_scores
            # route_scores.append({
            #     "route_index": route_index,
            #     "path": path,
            #     "total_distance": total_distance,
            #     "total_crime": total_crime,
            #     "f_score": total_f_score,
            #     "route_graph": route_graph.graph,
            #     "encoded_polyline": route.get("polyline", {}).get("encodedPolyline", None)
            # })


        # Sort the routes based on the f_score and select the top 2
        # route_scores.sort(key=lambda x: x[4])  # Sort by f_score
        # best_routes = route_scores[:2]  # Top 2 routes
        # return best_routes

        # Visualization
        # fig, axes = plt.subplots(1, len(best_routes), figsize=(15, 5))
        # axes = np.atleast_1d(axes)

        # for i, (route_index, path, total_distance, total_crime, total_f_score, graph) in enumerate(best_routes):
        #     self.visualize_graph(graph, path, f"Route {route_index + 1}\nDistance: {total_distance:.2f}m\nCrime: {total_crime}\nTotal f_score: {total_f_score:.2f}", axes[i])

        #     print(f"Route {route_index + 1}: Distance = {total_distance:.2f} meters, Crime Density = {total_crime}, f_score = {total_f_score:.2f}")

        # plt.show()

        # Return the two best routes
        return [(route[0], route[1], route[4]) for route in best_routes]  # Return (route_index, path, f_score)

