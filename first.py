import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, box
import math
from queue import PriorityQueue, Queue

# === Load Shapefile ===
roads = gpd.read_file("mongolia-251015-free.shp", layer="gis_osm_roads_free_1")

# === Filter for Ulaanbaatar ===
ub_bbox = box(106.81, 47.88, 107.01, 47.96)
roads = roads[roads.intersects(ub_bbox)]
print(f"Filtered to {len(roads)} Ulaanbaatar roads")

# === Build Graph (manually) ===
graph = {}
def add_edge(p1, p2, dist):
    if p1 not in graph: graph[p1] = []
    if p2 not in graph: graph[p2] = []
    graph[p1].append((p2, dist))
    graph[p2].append((p1, dist))

def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

for geom in roads.geometry:
    if isinstance(geom, LineString):
        coords = list(geom.coords)
        for i in range(len(coords)-1):
            p1, p2 = coords[i], coords[i+1]
            add_edge(p1, p2, distance(p1, p2))

print(f"Graph built with {len(graph)} nodes")

# === Pathfinding algorithms ===
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

def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        visited.add(node)
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
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

# === Define start and goal points ===
start = min(graph.keys(), key=lambda p: distance(p, (106.90, 47.92)))  # near center
goal = min(graph.keys(), key=lambda p: distance(p, (106.93, 47.92)))   # slightly east

print("Start:", start)
print("Goal:", goal)

# === Run algorithms ===
path_bfs = bfs(start, goal)
path_dfs = dfs(start, goal)
path_dijkstra, dist = dijkstra(start, goal)

print(f"BFS path length: {len(path_bfs) if path_bfs else 'N/A'}")
print(f"DFS path length: {len(path_dfs) if path_dfs else 'N/A'}")
print(f"Dijkstra path length: {len(path_dijkstra) if path_dijkstra else 'N/A'}, Distance: {dist:.4f}")

# === Visualization ===
roads.plot(color="lightgray", linewidth=0.5)
plt.xlim(106.81, 107.01)
plt.ylim(47.88, 47.96)

# Draw Dijkstra path (most optimal)
if path_dijkstra:
    xs, ys = zip(*path_dijkstra)
    plt.plot(xs, ys, color="blue", linewidth=2, label="Dijkstra Path")

# Start and End
plt.scatter(start[0], start[1], color="red", s=30, label="Start")
plt.scatter(goal[0], goal[1], color="green", s=30, label="Goal")

plt.title("Ulaanbaatar Road Pathfinding")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()
