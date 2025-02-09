import json
import networkx as nx
import heapq
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
              "endLocation": { "latLng": { "latitude": 40.780374, "longitude": -73.991058 } },
              "distanceMeters": 3621,
              "travelMode": "WALK"
            },
            {
              "startLocation": { "latLng": { "latitude": 40.780374, "longitude": -73.991058 } },
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


def create_graph_for_route(route):
    """Create a graph for a given route."""
    graph = nx.DiGraph()

    for leg in route["legs"]:
        for step in leg["steps"]:
            start_lat, start_lng = step["startLocation"]["latLng"]["latitude"], step["startLocation"]["latLng"]["longitude"]
            end_lat, end_lng = step["endLocation"]["latLng"]["latitude"], step["endLocation"]["latLng"]["longitude"]

            start_node = (start_lat, start_lng)
            end_node = (end_lat, end_lng)

            distance = geodesic((start_lat, start_lng), (end_lat, end_lng)).meters
            graph.add_edge(start_node, end_node, weight=distance)

    return graph


def heuristic(current_node, goal_node):
    """Calculate the straight-line distance (h(n)) between the current node and the goal node."""
    return geodesic(current_node, goal_node).meters


def a_star(graph, start_node, goal_node):
    """Perform A* search on the given graph."""
    frontier = []
    heapq.heappush(frontier, (0, start_node, 0))  # (f(n), node, g(n))
    reached = {start_node: {"cost": 0, "parent": None}}
    total_cost = None

    while frontier:
        f_n, current_node, g_n = heapq.heappop(frontier)

        if current_node == goal_node:
            total_cost = g_n
            path = []
            while current_node:
                path.insert(0, current_node)
                current_node = reached[current_node]["parent"]
            return path, total_cost

        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor]["weight"]
            tentative_g_n = g_n + edge_weight

            h_n = heuristic(neighbor, goal_node)
            f_n = tentative_g_n + h_n

            if neighbor not in reached or tentative_g_n < reached[neighbor]["cost"]:
                reached[neighbor] = {"cost": tentative_g_n, "parent": current_node}
                heapq.heappush(frontier, (f_n, neighbor, tentative_g_n))

    return None, float('inf') 


def find_optimal_route(routes):
    """Find the route with the lowest combined g(n) and h(n) cost."""
    optimal_route = None
    min_total_cost = float('inf')
    optimal_path = []
    route_graphs = []

    for route_index, route in enumerate(routes):
        graph = create_graph_for_route(route)
        route_graphs.append(graph)

        # Define start and goal nodes for A* search
        start_step = route["legs"][0]["steps"][0]["startLocation"]["latLng"]
        end_step = route["legs"][0]["steps"][-1]["endLocation"]["latLng"]
        start_node = (start_step["latitude"], start_step["longitude"])
        goal_node = (end_step["latitude"], end_step["longitude"])

        # Run A* search on the route graph
        path, total_cost = a_star(graph, start_node, goal_node)
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            optimal_route = route
            optimal_path = path

    visualize_routes(route_graphs, optimal_path)
    return optimal_route, optimal_path, min_total_cost


def visualize_routes(graphs, optimal_path):
    plt.figure(figsize=(10, 8))
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink']
    
    for i, graph in enumerate(graphs):
        pos = {node: (node[1], node[0]) for node in graph.nodes()}  # Longitude as x, Latitude as y
        nx.draw(graph, pos, node_color=colors[i % len(colors)], edge_color='gray', with_labels=False, node_size=50)
    
    # Highlight the optimal path
    optimal_edges = list(zip(optimal_path[:-1], optimal_path[1:]))
    nx.draw_networkx_nodes(graphs[0], pos, nodelist=optimal_path, node_color='yellow', node_size=100)
    nx.draw_networkx_edges(graphs[0], pos, edgelist=optimal_edges, edge_color='red', width=2)
    
    plt.title("Visualization of Routes and Optimal Path")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

def main():
    data = json.loads(routes_json)
    optimal_route, optimal_path, min_total_cost = find_optimal_route(data["routes"])

    # Display the optimal path
    print(f"\nOptimal Route Total Cost (g(n) + h(n)): {min_total_cost:.2f} meters")
    print("Optimal Path:")
    for node in optimal_path:
        print(f"  - {node}")


if __name__ == "__main__":
    main()
