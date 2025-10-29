import heapq

graph = {
    'a': {'b': 4, 'c': 2, 'g': 7},
    'b': {'a': 4, 'c': 1, 'd': 5},
    'c': {'a': 2, 'b': 1, 'd': 8, 'e': 10, 'h': 3},
    'd': {'b': 5, 'c': 8, 'f': 6},
    'e': {'c': 10, 'f': 2, 'i': 5},
    'f': {'d': 6, 'e': 2, 'j': 3},
    'g': {'a': 7, 'h': 4},
    'h': {'c': 3, 'g': 4, 'i': 6},
    'i': {'e': 5, 'h': 6, 'j': 1},
    'j': {'f': 3, 'i': 1, 'k': 2},
    'k': {'j': 2}
}


def dijkstra(start, goal):
    pq = [(0, start)]
    distances = { node: float('inf') for node in graph }
    parent = {node: None for node in graph}

    distances[start] = 0

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_dist > distances[curr_node]:
            continue

        if curr_node == goal:
            break

        for nei, weight in graph[curr_node].items():
            new_dist = curr_dist + weight
            if new_dist < distances[nei]:
                distances[nei] = new_dist
                parent[nei] = curr_node
                heapq.heappush(pq, (new_dist, nei))

    path = []

    node = goal

    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, distances[goal]

print(dijkstra('a', 'k'))