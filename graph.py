import geopandas as gpd
from shapely.geometry import LineString, box
import math
from queue import PriorityQueue, Queue

ub_bbox = box(106.81, 47.88, 107.01, 47.96)

roads = gpd.read_file("mongolia-251015-free.shp", layer="gis_osm_roads_free_1")
roads = roads[roads.intersects(ub_bbox)]

graph = {}

def add_edge(p1, p2, dist):
    if p1 not in graph: graph[p1] = []
    if p2 not in graph: graph[p2] = []
    graph[p1].append((p2, dist))
    graph[p2].append((p1, dist))

def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def distance_between_nodes(n1, n2):
    for neighbor, w in graph.get(n1, []):
        if neighbor == n2:
            lat_factor = 111_000  
            lon_factor = 111_000 * math.cos(math.radians((n1[1]+n2[1])/2))  
            return math.hypot(w * lon_factor, w * lat_factor) 
    return 0

for geom in roads.geometry:
    if isinstance(geom, LineString):
        coords = list(geom.coords)
        for i in range(len(coords)-1):
            p1, p2 = coords[i], coords[i+1]
            add_edge(p1, p2, distance(p1, p2))


def find_nearest_node(coord):
    return min(graph.keys(), key=lambda p: distance(p, coord))

def bfs(start, goal):
    visited = set()
    queue = Queue()
    queue.put((start, [start]))
    while not queue.empty():
        node, path = queue.get()
        if node == goal:
            return path
        visited.add(node)
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                queue.put((neighbor, path + [neighbor]))
    return None

def dijkstra(start, goal):
    pq = PriorityQueue()
    pq.put((0, start, [start]))
    visited = set()
    while not pq.empty():
        dist, node, path = pq.get()
        if node == goal:
            return path, dist
        if node in visited:
            continue
        visited.add(node)
        for neighbor, w in graph.get(node, []):
            if neighbor not in visited:
                pq.put((dist + w, neighbor, path + [neighbor]))
    return None, float('inf')


def dfs_recursive(start, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path = path + [start]

    if start == goal:
        return path
    
    for neighbor, _ in graph.get(start, []):
        if neighbor not in visited:
            result = dfs(neighbor, goal, visited, path)
            if result is not None:
                return result
    
    return None

def dfs(start, goal, visited=None, path=None):
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None