import json
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import heapq
import numpy as np

class RouteGraph:
    def __init__(self, route):
        self.graph = nx.DiGraph()
        self.start_node, self.goal_node = self._build_graph(route)

    def _build_graph(self, route):
        start_node = (route["legs"][0]["startLocation"]["latLng"]["latitude"],
                      route["legs"][0]["startLocation"]["latLng"]["longitude"])
        previous_node = start_node
        self.graph.add_node(start_node)

        for leg in route["legs"]:
            for step in leg["steps"]:
                end_lat = step["endLocation"]["latLng"]["latitude"]
                end_lng = step["endLocation"]["latLng"]["longitude"]
                end_node = (end_lat, end_lng)

                weight = geodesic(previous_node, end_node).meters
                self.graph.add_edge(previous_node, end_node, weight=weight)
                previous_node = end_node

        goal_node = previous_node
        return start_node, goal_node