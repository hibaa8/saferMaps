import json
from geopy.distance import geodesic
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from sodapy import Socrata
import math
import heapq

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
              "endLocation": { "latLng": { "latitude": 40.750374, "longitude": -73.991058 } },
              "distanceMeters": 3621,
              "travelMode": "WALK"
            },
            {
              "startLocation": { "latLng": { "latitude": 40.750374, "longitude": -73.991058 } },
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


graph = nx.DiGraph()
data = json.loads(routes_json)

def round_location(lat, lng, precision=5):
    """ Round latitude and longitude to avoid floating-point precision issues. """
    # return (math.trunc(lat * 1000) / 1000), (math.trunc(lng * 1000) / 1000), 
    return round(lat, precision), round(lng, precision)


# "legs":[
#             {
#                "distanceMeters":33337,
#                "duration":"3472s",
#                "staticDuration":"3472s",
#                "polyline":{
#                   "encodedPolyline":"s~`xFlambMeJcApAjBv[~SbAb@`@LzBT~ERfAHlARdAXhChAdBdA`{@xj@pKtIxQdM|CnBhBt@|Ab@dFlAzHvAvBZhAL|DVxSVpC?r\\Yn@MfCu@j@Gl@AnHj@fC\\|@P|C~@pEpBnLvGjBx@pBl@jGzAfA\\hAj@ll@|_@Uh@fAdGyAzD_Bu@nCcMji@qcB^_BRqBrLmxBDsBB}BGwCOoCWoCe@mDc@uBuGaVeOef@sAsEq@wCiA}FmAaIeAoIePczAU{B]sEs@gHSoDG{BGuA?uCHiDNmCNiBPuAf@sCl@aCp@wBzAqDvAsCjCcEzAmBpGeHzCeDxPoR~DuEz@u@rE}ExD}EdBoCjA{B`AoBhK}ZrJoZ`DsKtHkYfIa[l@sBzCqLbNwg@hGmUzGoWrHiYrU}|@r@iCjAqDjDoIrCoF|@{A`CoDfB}BpDgErC}ChFeGhSoU|EwF|[}^tJeLpB{BpCwD|AcCtAiC~@wB`AoCv@yCReAX}BJiBDkCG}BMcBcA_JKyAg@sEaD{PcA^Yv@j@hCnFqAJGnArEj@jDtAzE|@zDb@`Ab@n@h@\\p@JdA?d@KjCwAnUqKf_@kQjL{Ez_@_O`]iMfBe@lBc@nAO~BOjEMjHDrDLv@FtAXdAXpCnAnCxAbCdAtGlBhBVjEXvE?tMFz@D~@X`@\\b@x@lArEb@z@n@r@zD|CpB|@~A\\bADbAAhBUjBa@hC}@`Ae@xIeFbH}EfEiDxCqC`EmEtAcBhAkBv@aB`AuCr@aD^_CLiBHeIM}FSqFOqGFgAL{@V{@^u@j@k@z@g@dAoA`Aq@FN"
#                },
#                "startLocation":{
#                   "latLng":{
#                      "latitude":40.806342699999995,
#                      "longitude":-73.9639078
#                   }
#                },
#                "endLocation":{
#                   "latLng":{
#                      "latitude":40.64362,
#                      "longitude":-73.78944
#                   }
#                },



# def create_graph():
#     graph = nx.DiGraph()

#     data = json.loads(routes_json)


#     for route in data["routes"]:
#         previous_node = None
#         for leg in route["legs"]:
#             for step in leg["steps"]:
#                 if "transitDetails" in step:
#                     transit = step["transitDetails"]["stopDetails"]
#                     departure_stop = transit["departureStop"]
#                     arrival_stop = transit["arrivalStop"]

#                     dep_lat, dep_lng = round_location(
#                         departure_stop["location"]["latLng"]["latitude"],
#                         departure_stop["location"]["latLng"]["longitude"]
#                     )
#                     dep_node = (dep_lat, dep_lng, departure_stop["name"].replace(" ", "").lower())
#                     graph.add_node(dep_node)

#                     #if there is a previous node and its not the same as the departure node
#                     if previous_node and (previous_node[0] != dep_node[0] and previous_node[1] != dep_node[1]):
#                         print(previous_node[2])
#                         print(dep_node[2])
#                         distance_prev_dep = geodesic((previous_node[0], previous_node[1]), (dep_node[0], dep_node[1])).meters
#                         print(f'base distance: {geodesic((previous_node[0], previous_node[1]), (dep_node[0], dep_node[1])).meters}')
#                         # distance_prev_dep = calculate_edge_weight(previous_node, dep_node)
#                         graph.add_edge(previous_node, dep_node, base_weight=distance_prev_dep)


#                     arr_lat, arr_lng = round_location(
#                         arrival_stop["location"]["latLng"]["latitude"],
#                         arrival_stop["location"]["latLng"]["longitude"]
#                     )
#                     arr_node = (arr_lat, arr_lng, arrival_stop["name"].replace(" ", "").lower())
#                     graph.add_node(arr_node)
                    
#                     distance_dep_arr = geodesic((dep_node[0], dep_node[1]), (arr_node[0], arr_node[1])).meters
#                     print(f'base distance: {geodesic((dep_node[0], dep_node[1]), (arr_node[0], arr_node[1])).meters}')
#                     # distance_dep_arr = calculate_edge_weight(dep_node, arr_node)
#                     graph.add_edge(dep_node, arr_node, base_weight=distance_dep_arr)

#                     previous_node = arr_node
#                 else:
#                     dep_lat, dep_lng = round_location(
#                         step["startLocation"]["latLng"]["latitude"],
#                         step["startLocation"]["latLng"]["longitude"]
#                     )
#                     dep_node = (dep_lat, dep_lng, departure_stop["name"].replace(" ", "").lower())
#                     graph.add_node(dep_node)

#                     #if there is a previous node and its not the same as the departure node
#                     if previous_node and (previous_node[0] != dep_node[0] and previous_node[1] != dep_node[1]):
#                         print(previous_node[2])
#                         print(dep_node[2])
#                         distance_prev_dep = geodesic((previous_node[0], previous_node[1]), (dep_node[0], dep_node[1])).meters
#                         print(f'base distance: {geodesic((previous_node[0], previous_node[1]), (dep_node[0], dep_node[1])).meters}')
#                         # distance_prev_dep = calculate_edge_weight(previous_node, dep_node)
#                         graph.add_edge(previous_node, dep_node, base_weight=distance_prev_dep)
                    
#                     arr_lat, arr_lng = round_location(
#                         arrival_stop["endLocation"]["latLng"]["latitude"],
#                         arrival_stop["endLocation"]["latLng"]["longitude"]
#                     )
#                     arr_node = (arr_lat, arr_lng, arrival_stop["name"].replace(" ", "").lower())
#                     graph.add_node(arr_node)
                    
#                     distance_dep_arr = geodesic((dep_node[0], dep_node[1]), (arr_node[0], arr_node[1])).meters
#                     print(f'base distance: {geodesic((dep_node[0], dep_node[1]), (arr_node[0], arr_node[1])).meters}')
#                     # distance_dep_arr = calculate_edge_weight(dep_node, arr_node)
#                     graph.add_edge(dep_node, arr_node, base_weight=distance_dep_arr)

#                     previous_node = arr_node


    # plt.figure(figsize=(8, 6))
    # pos = nx.spring_layout(graph)  
    # nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=8)
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['base_weight']:.2f}m" for u, v, d in graph.edges(data=True)})

    # plt.show()
    # start_node = (40.80772, -73.96411, "116st-columbiauniversity")
    # goal_node = (40.64362, -73.78944, "terminal1")

    # path, expanded, frontier_sizes = a_star(graph, start_node, goal_node)

    # # Display the results
    # print("Optimal Path:", " → ".join([node[2] for node in path]))
    # print("Total Expanded Nodes:", len(expanded))
    # print("Frontier Sizes at Each Iteration:", frontier_sizes)

def create_graph():
    graph = nx.DiGraph()
    data = json.loads(routes_json)

    for route_index, route in enumerate(data["routes"]):
        previous_node = None
        # g_total = 0  # Total cost for g(n) accumulation within a leg

        for leg_index, leg in enumerate(route["legs"]):
            for step in leg["steps"]:
                # Parse start and end locations
                start_lat, start_lng = round_location(
                    step["startLocation"]["latLng"]["latitude"],
                    step["startLocation"]["latLng"]["longitude"]
                )
                end_lat, end_lng = round_location(
                    step["endLocation"]["latLng"]["latitude"],
                    step["endLocation"]["latLng"]["longitude"]
                )

                start_node = (start_lat, start_lng, f"route{route_index}_leg{leg_index}_start")
                end_node = (end_lat, end_lng, f"route{route_index}_leg{leg_index}_end")

                # Calculate distance for g(n) contribution
                base_distance = geodesic((start_lat, start_lng), (end_lat, end_lng)).meters

                # Add step cost to g(n) and create graph edges
                # g_total += base_distance
                graph.add_node(start_node)
                graph.add_node(end_node)
                graph.add_edge(start_node, end_node, base_weight=base_distance)

                # Connect to previous node within the route
                if previous_node:
                    graph.add_edge(previous_node, start_node, base_weight=base_distance)

                previous_node = end_node  # Update for the next iteration

    # plt.figure(figsize=(8, 6))
    # pos = nx.spring_layout(graph)  
    # nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=8)
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['base_weight']:.2f}m" for u, v, d in graph.edges(data=True)})

    # plt.show()
    # Perform A* search
    start_node = (40.80772, -73.96411)
    end_node = (40.64362, -73.78944)
    optimal_path, optimal_cost = a_star_search(graph, start_node, end_node)

    # Display the results
    if optimal_path:
        print("Optimal Path:", " → ".join([node[2] for node in optimal_path]))
        print("Total Cost (meters):", optimal_cost)
    else:
        print("No path found.")


def a_star_search(graph, start, goal):
    """Performs A* search to find the optimal path from start to goal."""
    frontier = []
    heapq.heappush(frontier, (0, start, 0))  # (f(n), current_node, g(n))
    reached = {start: {"cost": 0, "parent": None}}  # Track the lowest cost to each node
    expanded = []

    while frontier:
        f_n, current_node, g_n = heapq.heappop(frontier)
        expanded.append(current_node)

        if current_node == goal:
            return reconstruct_path(reached, current_node), g_n

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)
            base_weight = edge_data["base_weight"]
            tentative_g_n = g_n + base_weight

            # Calculate heuristic h(n) using geodesic distance
            h_n = geodesic((neighbor[0], neighbor[1]), (goal[0], goal[1])).meters
            f_n = tentative_g_n + h_n  # f(n) = g(n) + h(n)

            # If this path is better or the neighbor is not visited yet
            if neighbor not in reached or tentative_g_n < reached[neighbor]["cost"]:
                reached[neighbor] = {"cost": tentative_g_n, "parent": current_node}
                heapq.heappush(frontier, (f_n, neighbor, tentative_g_n))

    return None, float("inf")  # No path found


def reconstruct_path(reached, current_node):
    """Reconstruct the path from goal to start."""
    path = []
    while current_node:
        path.insert(0, current_node)
        current_node = reached[current_node]["parent"]
    return path


    # Perform A* search
    
    # start_lat = data["routes"][0]["legs"][0]["steps"][0]["startLocation"]["latLng"]["latitude"]
    # start_long = data["routes"][0]["legs"][0]["steps"][0]["startLocation"]["latLng"]["longitude"]
    # start_node = (40.80772, -73.96411)

    # end_lat = data["routes"][0]["legs"][0]["steps"][0]["endLocation"]["latLng"]["latitude"]
    # end_long = data["routes"][0]["legs"][0]["steps"][0]["endLocation"]["latLng"]["latitude"]
    # end_node = (40.64362, -73.78944)

    # path, cost = a_star(graph, start_node, end_node)

    # # Display the results
    # if path:
    #     print("Optimal Path:", " → ".join([node[2] for node in path]))
    #     print("Total Cost (meters):", cost)
    # else:
    #     print("No path found.")


# def a_star(graph, start, goal):
#     """ Performs A* search to find the optimal path from start to goal. """
    
#     # Priority queue for the frontier: (f(n), current_node, g(n))
#     frontier = []
#     heapq.heappush(frontier, (0, start, 0))

#     # Tracking visited nodes with their g(n) costs and parents
#     reached = {start: {"cost": 0, "parent": None}}

#     # Expanded nodes and frontier sizes tracking
#     expanded = []
#     frontier_sizes = []

#     while frontier:
#         f_n, current_node, g_n = heapq.heappop(frontier)
#         expanded.append(current_node)

#         # If goal is reached, reconstruct the path
#         if current_node == goal:
#             path = []
#             while current_node:
#                 path.insert(0, current_node)
#                 current_node = reached[current_node]["parent"]
#             return path

#         # Expand neighbors
#         for neighbor in graph.neighbors(current_node):
#             edge_data = graph.get_edge_data(current_node, neighbor)
#             base_weight = edge_data['base_weight']
#             tentative_g_n = g_n + base_weight  # g(n) update

#             # Calculate heuristic h(n) based on geodesic distance
#             h_n = geodesic((neighbor[0], neighbor[1]), (goal[0], goal[1])).meters
#             f_n = tentative_g_n + h_n  # f(n) = g(n) + h(n)

#             # If this path is better, update and push to frontier
#             if neighbor not in reached or tentative_g_n < reached[neighbor]["cost"]:
#                 reached[neighbor] = {"cost": tentative_g_n, "parent": current_node}
#                 heapq.heappush(frontier, (f_n, neighbor, tentative_g_n))

#         # Track the size of the frontier at this step
#         frontier_sizes.append(len(frontier))

#     # Return empty path if no path is found
#     return []


create_graph()

# def calculate_edge_weight(node1, node2):
#     base_distance = geodesic((node1[0], node1[1]), (node2[0], node2[1])).meters
#     crimes_near_node1 = count_crimes_near_location((node1[0], node1[1]))
#     crimes_near_node2 = count_crimes_near_location((node2[0], node2[1]))
#     crimes_along_edge = count_crimes_along_edge(node1, node2)

#     total_crimes = crimes_near_node1 + crimes_near_node2 + crimes_along_edge
#     crime_factor = total_crimes / 10  

#     return base_distance * (1 + crime_factor)


# def call_security_api():
#     client = Socrata("data.cityofnewyork.us", None)
#     results = client.get("qb7u-rbmr", limit=3)

#     with open('crime.txt', 'a') as file:
#         file.write(results)
    
#     file.close()

# def count_crimes_near_location(crime_data, location, radius_km=0.5):
#     """ Count crimes within a given radius of a location (latitude, longitude). """
#     count = 0
#     for crime in crime_data:
#         crime_location = (crime["latitude"], crime["longitude"])
#         if geodesic(location, crime_location).kilometers <= radius_km:
#             count += 1
#     return count

# def count_crimes_along_edge(node1, node2, radius_km=0.5):
#     """ Count crimes along the edge by checking crimes near the edge's midpoint. """
#     midpoint = (
#         (node1[0] + node2[0]) / 2,
#         (node1[1] + node2[1]) / 2
#     )
#     return count_crimes_near_location(midpoint, radius_km)



# # call_security_api()
# create_graph()

# Process the routes and add nodes/edges
# for route in data["routes"]:
#     previous_node = None
#     for leg in route["legs"]:
#         for step in leg["steps"]:
#             if "transitDetails" in step:
#                 transit = step["transitDetails"]["stopDetails"]
#                 departure_stop = transit["departureStop"]
#                 arrival_stop = transit["arrivalStop"]

#                 # Round locations to merge same stations into one node
#                 dep_lat, dep_lng = round_location(
#                     departure_stop["location"]["latLng"]["latitude"],
#                     departure_stop["location"]["latLng"]["longitude"]
#                 )
#                 dep_node = (dep_lat, dep_lng, departure_stop["name"])

#                 arr_lat, arr_lng = round_location(
#                     arrival_stop["location"]["latLng"]["latitude"],
#                     arrival_stop["location"]["latLng"]["longitude"]
#                 )
#                 arr_node = (arr_lat, arr_lng, arrival_stop["name"])

#                 # Add nodes and edges
#                 graph.add_node(dep_node)
#                 graph.add_node(arr_node)

#                 if previous_node and previous_node[2] != dep_node[2]:
#                     # Add an edge between the previous node and current departure node
#                     distance_prev_dep = geodesic((previous_node[0], previous_node[1]), (dep_node[0], dep_node[1])).meters
#                     graph.add_edge(previous_node, dep_node, base_weight=distance_prev_dep)

#                 # Add an edge between the current departure and arrival nodes
#                 distance_dep_arr = geodesic((dep_node[0], dep_node[1]), (arr_node[0], arr_node[1])).meters
#                 graph.add_edge(dep_node, arr_node, base_weight=distance_dep_arr)

#                 # Update previous node
#                 previous_node = arr_node

# # Draw the graph
# plt.figure(figsize=(10, 8))
# pos = nx.spring_layout(graph)  # Layout for visualization
# nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=8)
# nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['base_weight']:.2f}m" for u, v, d in graph.edges(data=True)})

# plt.show()

# Display graph details
# print("Total number of nodes:", graph.number_of_nodes())
# print("Total number of edges:", graph.number_of_edges())
