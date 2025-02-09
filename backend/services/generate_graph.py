import json
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import heapq
import random
import numpy as np

import json
from RoutePlanner import RoutePlanner
from RouteGraph import RouteGraph

if __name__ == "__main__":
    with open('data.json', 'r') as file:
        json_data = json.load(file)

    with open('crime_data.json', 'r') as file:
        crime_data = json.load(file)
