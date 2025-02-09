import networkx as nx
import json
from geopy.distance import geodesic
import matplotlib.pyplot as plt

routes_json = '''{
  "routes": [
    {
      "legs": [
        {
          "steps": [
            {
              "startLocation": { "latLng": { "latitude": 40.80772, "longitude": -73.96411 } },
              "endLocation": { "latLng": { "latitude": 40.750374, "longitude": -73.991058 } },
              "distanceMeters": 3621,
              "travelMode": "WALK"
            },
            {
              "startLocation": { "latLng": { "latitude": 40.750374, "longitude": -73.991058 } },
              "endLocation": { "latLng": { "latitude": 40.64362, "longitude": -73.78944 } },
              "distanceMeters": 15000,
              "travelMode": "TRANSIT"
            }
          ]
        }
      ]
    },
    {
      "legs": [
        {
          "steps": [
            {
              "startLocation": { "latLng": { "latitude": 40.80772, "longitude": -73.96411 } },
              "endLocation": { "latLng": { "latitude": 40.79818, "longitude": -73.991058 } },
              "distanceMeters": 3621,
              "travelMode": "WALK"
            },
            {
              "startLocation": { "latLng": { "latitude": 40.79818, "longitude": -73.991058 } },
              "endLocation": { "latLng": { "latitude": 40.64362, "longitude": -73.78944 } },
              "distanceMeters": 17000,
              "travelMode": "TRANSIT"
            }
          ]
        }
      ]
    }
  ]
}'''


def round_location(lat, lng, precision=5):
    """ Round latitude and longitude to avoid floating-point precision issues. """
    return round(lat, precision), round(lng, precision)


def create_graph():
    graph = nx.DiGraph()
    data = json.loads(routes_json)

    for route_index, route in enumerate(data["routes"]):
        previous_node = None

        for leg_index, leg in enumerate(route["legs"]):
            for step_index, step in enumerate(leg["steps"]):
                # Parse start and end locations
                start_lat, start_lng = round_location(
                    step["startLocation"]["latLng"]["latitude"],
                    step["startLocation"]["latLng"]["longitude"]
                )
                end_lat, end_lng = round_location(
                    step["endLocation"]["latLng"]["latitude"],
                    step["endLocation"]["latLng"]["longitude"]
                )

                start_node = (start_lat, start_lng)
                end_node = (end_lat, end_lng)

                # Calculate distance as g(n)
                base_distance = geodesic((start_lat, start_lng), (end_lat, end_lng)).meters

                # Add nodes and edges to the graph
                graph.add_node(start_node)
                graph.add_node(end_node)
                graph.add_edge(start_node, end_node, base_weight=base_distance)

                # Connect to previous node if exists
                if previous_node and (previous_node[0] != start_node[0] and previous_node[1] != start_node[1]):
                    graph.add_edge(previous_node, start_node, base_weight=0)

                previous_node = end_node  # Update for the next iteration

    # plt.figure(figsize=(8, 6))
    # pos = nx.spring_layout(graph)  
    # nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=8)
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['base_weight']:.2f}m" for u, v, d in graph.edges(data=True)})

    # plt.show()
    return graph, (40.80772, -73.96411), (40.64362, -73.78944)  # Return start and end nodes


def a_star_search(graph, start, goal):
    """ A* search to find the optimal path from start to goal. """
    import heapq

    frontier = []
    heapq.heappush(frontier, (0, start, 0))  # (f(n), current_node, g(n))

    reached = {start: {"cost": 0, "parent": None}}

    while frontier:
        f_n, current_node, g_n = heapq.heappop(frontier)

        if current_node == goal:
            path = []
            while current_node:
                path.insert(0, current_node)
                current_node = reached[current_node]["parent"]
            return path, g_n  # Return the path and total cost

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)
            base_weight = edge_data["base_weight"]

            tentative_g_n = g_n + base_weight  # Update g(n)

            # Heuristic h(n)
            h_n = geodesic((neighbor[0], neighbor[1]), (goal[0], goal[1])).meters
            f_n = tentative_g_n + h_n  # f(n) = g(n) + h(n)

            if neighbor not in reached or tentative_g_n < reached[neighbor]["cost"]:
                reached[neighbor] = {"cost": tentative_g_n, "parent": current_node}
                heapq.heappush(frontier, (f_n, neighbor, tentative_g_n))

    return None, float('inf')  # Return None if no path is found


def main():
    graph, start_node, end_node = create_graph()
    optimal_path, optimal_cost = a_star_search(graph, start_node, end_node)

    if optimal_path:
        print("Optimal Path:", " → ".join([f"({lat}, {lng})" for lat, lng in optimal_path]))
        print("Total Cost (meters):", optimal_cost)
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
