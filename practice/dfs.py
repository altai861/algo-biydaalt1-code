map_representation = {
    'a': ['b', 'c', 'g'],
    'b': ['a', 'c', 'd'],
    'c': ['a', 'b', 'd', 'e', 'h'],
    'd': ['b', 'c', 'f'],
    'e': ['c', 'f', 'i'],
    'f': ['d', 'e', 'j'],
    'g': ['a', 'h'],
    'h': ['c', 'g', 'i'],
    'i': ['e', 'h', 'j'],
    'j': ['f', 'i', 'k'],
    'k': ['j']
}

def dfs(start, goal):
    q = []
    visited = []
    parent = {}

    visited.append(start)

    q.append(start)
    parent[start] = None

    while len(q) > 0:
        u = q.pop()

        if u == goal:
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            path.reverse()
            return path

        for nei in map_representation[u]:
            if nei not in visited:
                print(nei)
                visited.append(nei)
                q.append(nei)
                parent[nei] = u



print(dfs('a', 'f'))